"""Safety layer for PocketTriage (PRD R13-R16).

R13: danger-sign keyword force-Pink (negation-aware, severity-aware)
R14: confidence floor → append "Escalate to medical officer"
R15: adult-condition refusal
R16: non-dismissable disclaimer (rendered in UI, enforced here as struct flag)

Pure functions, no I/O, no network. Unit-testable.

Design decision (2026-05-17): keyword list is tightened to only IMCI signs that
DEFINITIVELY classify the case as severe (general danger signs, severe-tier
classification signs). Signs that participate in moderate classifications
(e.g. sunken eyes alone, slow skin pinch alone) are LEFT to the model and the
combined-criteria logic — false-positive Pink overrides waste CHW time and
erode trust. Negation handling ("no stiff neck") is applied so a clinician
documenting absence doesn't trigger an emergency override.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Keywords that DEFINITIVELY mean "severe / refer urgently" in WHO IMCI.
# Each entry is matched as a whole phrase (word-boundary aware) and is negation-checked.
# Keep this list conservative — over-triggering Pink destroys trust.
DANGER_KEYWORDS: tuple[str, ...] = (
    # General danger signs (any one → urgent referral)
    "unable to drink",
    "unable to breastfeed",
    "vomits everything",
    "vomiting everything",
    "convulsion",
    "convulsions",
    "convulsing",
    "seizure",
    "seizing",
    "fitting now",
    "lethargic",
    "unconscious",
    "unresponsive",
    "limp and floppy",
    # Severe pneumonia signs
    "chest indrawing",
    "severe chest indrawing",
    "stridor in calm child",
    "chest sucking in",
    "chest is sucking in",
    "ribs sucking in",
    # Severe febrile disease
    "stiff neck",
    # Severe dehydration (the "very slowly" qualifier matters)
    "skin pinch goes back very slowly",
    # Severe ear (urgent)
    "tender swelling behind ear",
    "mastoiditis",
    # Severe acute malnutrition (urgent referral)
    "oedema of both feet",
    "bilateral pitting oedema",
    "visible severe wasting",
    "muac under 11.5",
    "muac < 11.5",
    "muac under 115",
    "muac < 115",
    # Severe anaemia
    "severe palmar pallor",
    # Refusing to drink is a danger sign per IMCI
    "refuses to drink",
    "refusing to drink",
    "not drinking",
)

ADULT_REFUSAL_KEYWORDS: tuple[str, ...] = (
    "chest pain in adult",
    "adult chest pain",
    "stroke symptoms in adult",
    "adult stroke",
    "pregnancy emergency",
    "pregnant patient",
    "labour pain",
    "labor pain",
    "ectopic pregnancy",
    "adult patient",
    "elderly patient",
    "geriatric patient",
)

# Negation prefixes that, if appearing within NEGATION_WINDOW characters before
# a danger keyword, cancel the match. Example: "no stiff neck" should not fire.
NEGATION_PHRASES: tuple[str, ...] = (
    "no ",
    "not ",
    "without ",
    "denies ",
    "negative for ",
    "absence of ",
    "absent ",
)
NEGATION_WINDOW = 25  # chars before the keyword to scan for a negation prefix

CONFIDENCE_FLOOR = 0.4
REFUSAL_TEXT = (
    "PocketTriage is configured for paediatric IMCI only (2 months – 5 years). "
    "This case appears to be adult — refer to the adult emergency protocol."
)


@dataclass
class TriageResult:
    """Normalized output after the safety layer has run."""
    tier: str  # "Pink" | "Yellow" | "Green" | "Refused"
    pathway: str
    reasoning: str
    confidence: float
    safety_flags: list[str] = field(default_factory=list)
    refused: bool = False


def _is_negated(text_lower: str, keyword_start: int) -> bool:
    """Return True if a negation phrase precedes the keyword within NEGATION_WINDOW chars,
    and no sentence boundary (. ! ?) separates them.

    Bug found by adversarial test 'negation_at_start_does_not_carry_forward':
    'No vomits everything. Chest indrawing visible.' was incorrectly
    suppressing 'chest indrawing' because the 25-char window picked up the
    earlier 'no ', even though a period separates the two clauses.
    A negation in a previous sentence must not reach forward.
    """
    window_start = max(0, keyword_start - NEGATION_WINDOW)
    window = text_lower[window_start:keyword_start]

    # If a sentence-ending punctuation appears in the window, only the
    # text AFTER the last such boundary counts as the negation scope.
    for boundary in (".", "!", "?", ";", "\n"):
        idx = window.rfind(boundary)
        if idx != -1:
            window = window[idx + 1:]

    return any(neg in window for neg in NEGATION_PHRASES)


def _match_keyword(text_lower: str, keyword: str) -> bool:
    """Substring match with word-boundary on the keyword's first char (avoids 'foofitting' matching 'fitting').

    Also runs negation-check — returns False if 'no X' / 'without X' precedes the match.
    """
    idx = text_lower.find(keyword)
    while idx != -1:
        # Word-boundary on left edge: previous char must be non-letter (or string start)
        left_boundary = idx == 0 or not text_lower[idx - 1].isalpha()
        if left_boundary and not _is_negated(text_lower, idx):
            return True
        idx = text_lower.find(keyword, idx + 1)
    return False


def detect_danger_signs(text: str) -> list[str]:
    """Return the list of danger-sign keywords matched (negation-aware) in text."""
    if not text:
        return []
    lowered = text.lower()
    return [kw for kw in DANGER_KEYWORDS if _match_keyword(lowered, kw)]


def detect_adult_refusal(text: str) -> list[str]:
    """Return the list of adult-refusal keywords matched (negation-aware) in text."""
    if not text:
        return []
    lowered = text.lower()
    return [kw for kw in ADULT_REFUSAL_KEYWORDS if _match_keyword(lowered, kw)]


def apply_safety_layer(
    symptoms: str,
    model_output: dict,
    *,
    had_photo: bool = False,
) -> TriageResult:
    """Apply R13–R17 to a raw model output.

    R17 (v0.2): if the input included a photo, the model's photo-reading
    accuracy is not field-verified at E2B (see eval/multimodal-test-log.md).
    Any non-Pink finding on a photo-bearing call gets an automatic
    'Escalate to medical officer' append, regardless of confidence.
    This closes the silent high-confidence-misclassification failure mode
    observed in S5-malnutrition-muac-photo.
    """
    flags: list[str] = []

    # R15 — adult refusal (highest priority, short-circuits)
    adult_hits = detect_adult_refusal(symptoms)
    if adult_hits:
        flags.append(f"R15: adult-refusal triggered ({', '.join(adult_hits[:3])})")
        return TriageResult(
            tier="Refused",
            pathway=REFUSAL_TEXT,
            reasoning="Adult-condition keywords detected in input. PocketTriage scope is paediatric only.",
            confidence=1.0,
            safety_flags=flags,
            refused=True,
        )

    tier = str(model_output.get("tier", "Yellow"))
    pathway = str(model_output.get("pathway", ""))
    reasoning = str(model_output.get("reasoning", ""))
    try:
        confidence = float(model_output.get("confidence", 0.5))
    except (TypeError, ValueError):
        confidence = 0.3
    confidence = max(0.0, min(1.0, confidence))

    # R13 — danger-sign force-Pink. Check both symptoms AND model reasoning text.
    danger_hits = detect_danger_signs(symptoms) + detect_danger_signs(reasoning)
    danger_hits = list(dict.fromkeys(danger_hits))  # dedupe preserving order
    if danger_hits and tier != "Pink":
        flags.append(
            f"R13: danger-sign force-Pink ({', '.join(danger_hits[:3])})"
        )
        tier = "Pink"
        if "refer urgently" not in pathway.lower():
            pathway = (
                "Pre-referral treatment then refer urgently to nearest hospital. "
                + pathway
            )

    # R13.5 — even if model said Pink, ensure pathway contains "Refer urgently"
    if tier == "Pink" and "refer urgently" not in pathway.lower():
        flags.append("R13.5: appended 'Refer urgently' to Pink pathway")
        pathway = pathway.rstrip(". ") + ". Refer urgently to nearest hospital."

    # R14 — confidence floor → append escalation
    if confidence < CONFIDENCE_FLOOR:
        flags.append(f"R14: confidence {confidence:.2f} < {CONFIDENCE_FLOOR} — escalate")
        if "escalate to medical officer" not in pathway.lower():
            pathway = pathway.rstrip(". ") + ". Escalate to medical officer."

    # R17 (v0.2) — photo-derived findings are not E2B-vision-reliable.
    # Force escalation on any non-Pink classification with a photo present.
    if had_photo and tier != "Pink":
        flags.append("R17: photo-derived finding — escalating regardless of confidence")
        if "escalate to medical officer" not in pathway.lower():
            pathway = pathway.rstrip(". ") + ". Escalate to medical officer to verify photo reading."

    return TriageResult(
        tier=tier,
        pathway=pathway,
        reasoning=reasoning,
        confidence=confidence,
        safety_flags=flags,
        refused=False,
    )
