"""PocketTriage — Gradio UI (laptop V1).

Runs Gemma 4 E4B locally via Ollama. Designed to work fully offline:
- No analytics, no telemetry, no external network calls.
- All inference goes to 127.0.0.1:11434 (the local Ollama).
- Patient data is processed in memory and discarded on session end.

Launch:
    ollama serve &   # in a separate terminal (or as a background service)
    ollama pull gemma4:e4b   # one-time
    python app.py
    # then open http://127.0.0.1:7860
"""

from __future__ import annotations

import base64
import io
import logging
import os

import gradio as gr
from PIL import Image

from infer import InferenceError, triage
from safety import TriageResult

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("pockettriage.app")

TIER_BADGE = {
    "Pink": ("🔴 PINK — Severe / Refer Urgently", "#d11d4a"),
    "Yellow": ("🟡 YELLOW — Treat at Facility", "#d8a900"),
    "Green": ("🟢 GREEN — Home Care", "#1f8a3a"),
    "Refused": ("⚫ REFUSED — Out of scope", "#444"),
}

DISCLAIMER = (
    "**PocketTriage is decision-support based on WHO IMCI 2014. "
    "It does NOT replace clinical judgment. "
    "Paediatric only (2 months – 5 years).**"
)

# Set by the HF Space Dockerfile so we can show a "this is the slow shared demo" notice.
# Local runs on Apple Silicon return in 8–11 s; the CPU-only HF Space takes 8–10 min per
# triage. The notice exists so a reviewer doesn't think the UI is broken while waiting.
ON_HF_SPACE = bool(os.environ.get("SPACE_ID")) or os.environ.get("GRADIO_SERVER_NAME") == "0.0.0.0"
SPACE_LATENCY_NOTICE = (
    "> ⏱  **Shared-CPU demo notice.** This Hugging Face Space runs on 2 vCPU with no GPU. "
    "Each triage takes about **8–10 minutes** because Gemma 4 E2B (5 B parameters) runs "
    "entirely on the container's CPU. The product is built for Apple Silicon laptops "
    "(~10 s) and Android phones via LiteRT. For fast eval, follow the README to run "
    "locally — it takes about 15 minutes from a clean clone."
)

EXAMPLE_INPUTS = [
    "11-month-old boy. Cough for 3 days. Breathing 58/min. Chest is sucking in. Restless and refusing to drink.",
    "2-year-old girl. Watery diarrhoea for 2 days, ~6 stools/day, no blood. Restless and irritable. Eyes slightly sunken. Drinks eagerly. Skin pinch slow.",
    "4-year-old boy in malaria-endemic region. Fever 38.8C for 2 days. RDT positive for P. falciparum. No stiff neck. Alert. No danger signs.",
    "3-year-old girl. Runny nose and cough for 2 days. Breathing 32/min. No chest indrawing. Drinking well. Playful. No fever.",
]


def _photo_to_b64(photo: Image.Image | None) -> str | None:
    """Convert a PIL image to base64-encoded JPEG (Ollama format)."""
    if photo is None:
        return None
    buf = io.BytesIO()
    # Downscale to keep tokens manageable on E4B
    max_dim = 768
    img = photo.copy()
    img.thumbnail((max_dim, max_dim))
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def _render_result(result: TriageResult) -> tuple[str, str, str, str]:
    """Format a TriageResult for the Gradio output components.

    Returns: (tier_html, pathway_md, reasoning_md, flags_md)
    """
    label, color = TIER_BADGE.get(result.tier, ("?", "#444"))
    tier_html = (
        f'<div style="background:{color};color:white;padding:14px 18px;'
        f'border-radius:8px;font-size:22px;font-weight:600;">{label}</div>'
    )
    pathway_md = f"### Action\n{result.pathway}"
    reasoning_md = (
        f"### IMCI Reasoning\n{result.reasoning}\n\n"
        f"**Model confidence:** {result.confidence:.2f}"
    )
    if result.safety_flags:
        flags_md = "### Safety Layer\n" + "\n".join(
            f"- {flag}" for flag in result.safety_flags
        )
    else:
        flags_md = "### Safety Layer\nNo overrides applied — model output passed through."
    return tier_html, pathway_md, reasoning_md, flags_md


def run_triage(symptoms: str, photo: Image.Image | None):
    """Gradio click handler."""
    if not symptoms or not symptoms.strip():
        return (
            '<div style="background:#444;color:white;padding:14px;border-radius:8px;">'
            "Please enter a symptom description."
            "</div>",
            "",
            "",
            "",
        )
    try:
        photo_b64 = _photo_to_b64(photo)
        result = triage(symptoms, photo_b64=photo_b64)
        return _render_result(result)
    except InferenceError as e:
        log.exception("inference error")
        return (
            '<div style="background:#444;color:white;padding:14px;border-radius:8px;">'
            f"Model unavailable: {str(e)[:200]}"
            "</div>",
            "",
            "",
            "",
        )
    except Exception as e:  # noqa: BLE001 — top-level UI handler
        log.exception("unexpected error")
        return (
            '<div style="background:#444;color:white;padding:14px;border-radius:8px;">'
            f"Unexpected error: {type(e).__name__}: {str(e)[:200]}"
            "</div>",
            "",
            "",
            "",
        )


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="PocketTriage", theme=gr.themes.Soft()) as ui:
        gr.Markdown("# PocketTriage")
        gr.Markdown(
            "Offline WHO IMCI triage for community health workers. "
            "Runs Gemma 4 E2B/E4B locally — no internet required."
        )
        if ON_HF_SPACE:
            gr.Markdown(SPACE_LATENCY_NOTICE)
        gr.Markdown(DISCLAIMER)
        with gr.Row():
            with gr.Column(scale=1):
                symptoms = gr.Textbox(
                    label="Patient presentation",
                    placeholder=(
                        "Age + sex + chief complaint + duration + vitals + danger signs.\n"
                        "Example: 11-month-old boy. Cough 3 days. Breathing 58/min. "
                        "Chest indrawing. Refuses to drink."
                    ),
                    lines=6,
                    max_length=1000,
                )
                photo = gr.Image(
                    label="Optional photo (e.g. rash, oedema, MUAC tape)",
                    type="pil",
                    height=200,
                )
                with gr.Row():
                    submit_btn = gr.Button("Triage", variant="primary")
                    clear_btn = gr.Button("Clear")
                gr.Examples(
                    examples=[[ex, None] for ex in EXAMPLE_INPUTS],
                    inputs=[symptoms, photo],
                    label="Tap an example",
                )
            with gr.Column(scale=1):
                tier_out = gr.HTML(label="Tier")
                pathway_out = gr.Markdown()
                reasoning_out = gr.Markdown()
                flags_out = gr.Markdown()
        gr.Markdown(
            "---\n"
            "*PocketTriage v0.1 · Gemma 4 E4B on-device · "
            "[GitHub](https://github.com/yonkoo11/pockettriage) · "
            "Apache 2.0*"
        )
        submit_btn.click(
            run_triage,
            inputs=[symptoms, photo],
            outputs=[tier_out, pathway_out, reasoning_out, flags_out],
        )
        clear_btn.click(
            lambda: ("", None, "", "", "", ""),
            outputs=[symptoms, photo, tier_out, pathway_out, reasoning_out, flags_out],
        )
    return ui


if __name__ == "__main__":
    ui = build_ui()
    # Default to localhost for the privacy-sensitive on-device run. The HF Space
    # entrypoint sets GRADIO_SERVER_NAME=0.0.0.0 so the Space proxy can reach
    # the container; everywhere else this stays bound to loopback.
    ui.queue(max_size=4).launch(
        server_name=os.environ.get("GRADIO_SERVER_NAME", "127.0.0.1"),
        server_port=int(os.environ.get("GRADIO_SERVER_PORT", "7860")),
        show_error=True,
        share=False,
    )
