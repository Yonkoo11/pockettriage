# Design Research — PocketTriage landing

## Product category

Open-source clinical decision-support tool, public-good positioning, on-device privacy story. The landing needs to convince two very different audiences in ≤ 30 seconds each:

- **Hackathon judges** (Google DeepMind, Kaggle community): "this is technically real and ethically grounded, not a vibe-coded prototype"
- **Public-health decision-makers** (WHO, NHM, NPHCDA staff): "this is professional, safe, and free for us to adopt"

Neither audience is impressed by gradient-purple-glow crypto-launch aesthetic. Both respond to editorial typography, real evidence, and restraint.

## Comparables studied (5)

### 1. Linear — linear.app

Category: developer tooling SaaS, but its marketing site is the cleanest editorial SaaS in market.

- **Layout:** narrow centered content column (~720-800px), large quiet hero, big serif/sans display headline, no busy nav. Single accent (their purple), used sparingly.
- **Color:** dark-first but the light mode is masterful — `#FAFAFA` base with a hint of warm cream, body text `#0F0F0F` (not pure black), generous whitespace.
- **Typography:** Inter Display for headlines (-0.04em tracking, weight 500 not 700), Inter for body. Display headlines very large (clamp 48–96px), body modest (16–17px).
- **Key interaction:** quiet — almost no decoration. Subtle hover lift on cards. Section reveal on scroll.
- **Hierarchy:** progressive disclosure. Hero says ONE thing. Sections below answer "but how?" then "but why?" then "but is it real?" — never all four in one viewport.
- **Signature:** restraint. The negative space IS the design.
- **STEAL THIS:** the "headline as a sentence, not a slogan" pattern. Linear writes "Linear is a purpose-built tool for planning and building products." not "Ship faster ✨ AI-powered project management 🚀".

### 2. Stripe Docs / Stripe.com — stripe.com

Category: financial infra, but pioneered editorial light-mode marketing.

- **Layout:** asymmetric. Hero text left, animated code/product visualisation right. Section transitions use depth + parallax sparingly.
- **Color:** `#FFFFFF` to `#F6F9FC` base, indigo accent `#635BFF`, generous use of pure white as a colour (not absence).
- **Typography:** Sohne/Stripe Sans (custom), 18px base, very generous line-height (1.7), display sizes calm (48–64px not 96px).
- **Key interaction:** the famous animated gradient hero, but in light mode it's a soft watercolor effect, not crypto-blob.
- **Signature:** code as a first-class design element. They show actual API calls in the hero.
- **STEAL THIS:** "evidence in the hero" — Stripe shows real code; PocketTriage can show the actual triage card output beside the headline.

### 3. NEJM Catalyst — catalyst.nejm.org

Category: clinical editorial. The aesthetic any health-tech product needs to be at least adjacent to in order to be taken seriously by clinicians.

- **Layout:** newspaper / journal — wide content column, generous margins, single serif display headline, byline, abstract. Side rail for related links.
- **Color:** pure editorial — `#FFFFFF` background, `#1B1B1B` body, `#A91E2E` for one specific accent (it's literally the colour of arterial blood, used for callouts and Section markers).
- **Typography:** old-style serif body (Georgia / Mercury / Adelle), sans-serif sub-display, real ALL-CAPS small-tracking section labels. Body 18–20px, line-height 1.6.
- **Hierarchy:** clear journal article shape — Abstract → Methods → Results → Discussion → References.
- **Signature:** TIME signature — every article has a date, a byline, a citation block. It feels real because it lives in academic time.
- **STEAL THIS:** treat the landing as an article. PocketTriage HAS evidence — the airplane-mode log, the 4/4 IMCI eval, the safety architecture. Lay it out like a clinical brief.

### 4. WHO Digital Health Atlas — digitalhealthatlas.org

Category: actual category sibling. This is where PocketTriage might end up registered.

- **Layout:** functional, not pretty. Card grid for projects, big filter chips on the left.
- **Color:** WHO blue `#0093D0` on white. Restrained.
- **Typography:** Roboto, undistinguished.
- **WHAT DOESN'T WORK:** the site looks like a 2018 government portal. PocketTriage should look better than this but stay in the same colour family (institutional blue / white / a single warm accent) so it doesn't read as "tech-bro disrupts healthcare".

### 5. Anthropic — anthropic.com

Category: AI product landing, recent (2024-2026). Most current example of an editorial-restraint AI brand.

- **Layout:** dead-centered column, very narrow (~640px text width), oversized serif display, single accent (their cream/clay tone).
- **Color:** off-white `#F5F1ED` (warm paper), body `#181818`, accent `#CC785C` (terracotta — natural, not synthetic).
- **Typography:** Tiempos Headline (serif display, weight 400 not bold), Styrene (sans body). Display sizes huge (clamp 56–112px) but always weight 400 — confidence, not shouting.
- **Signature:** absence of UI elements in hero. No CTA in the first viewport. Just text.
- **STEAL THIS:** the "serif display weight 400" trick. Bold serif display screams; regular-weight serif at the same large size whispers competence.

---

## Design Research Brief — synthesised direction

### Common patterns (table stakes — must include)

- Light-mode background, off-white or warm paper (`#F8F6F1` to `#FCFCFA`), never pure white
- Editorial typography: serif OR weight-400 display sans, never weight-800 trendy "AI" sans
- A single accent colour with a real reason. Not "looks nice"
- Body text 18–20px, line-height 1.55–1.7, max-width 65ch
- Quiet motion: hover lifts 1–2px, transitions 150–200ms ease-out
- "Evidence in the hero" — show the product output, not a hero illustration

### Differentiation opportunities (where we can stand out)

- **Lay it out like a clinical brief.** Abstract → Evidence → Architecture → Safety → Distribution. No marketing-page card-grid section repeated 5×.
- **Use the IMCI tier colours (Pink / Yellow / Green) sparingly as the only "decorative" colour.** These are domain-meaningful, not chosen for aesthetics. Pink and Yellow appear behind the safety section, Green behind the "Run locally" section.
- **Show the actual triage card output as the hero "evidence".** Not a screenshot — render it in real HTML in the hero. Reviewers see what the product produces in their first 5 seconds.

### Stolen elements

- From **Linear**: headline-as-sentence pattern, narrow content column, restraint
- From **Stripe**: evidence-in-the-hero (real product output beside the headline)
- From **NEJM**: clinical-brief section structure, real serif body, ALL-CAPS small-tracking section labels with a single accent rule
- From **Anthropic**: weight-400 serif display, warm-paper background, no CTA in first viewport
- From **WHO DHA**: enough institutional-blue / white restraint that it doesn't read as "tech-bro disrupts healthcare"

### Anti-patterns (must avoid)

- Card grid of 3 identical "feature cards" with icon + heading + sentence
- Stats row of 3-4 numbers in boxes ("4 SCENARIOS · 17 SAFETY TESTS · 0 NETWORK PACKETS · APACHE 2.0")
- Heroicons outline icons used decoratively
- Color-coded words in headlines (`<span class="text-cyan">offline</span>`)
- Self-certifying badges ("Privacy-First", "Open Source", "Safe")
- Generic CTAs ("Try it now", "Get started", "Launch app") — use the actual action ("Try a triage scenario", "Read the airplane-mode log")
- Purple/blue gradient blobs, mesh gradients, glass cards
- Pure white background or pure black body text
- More than one accent colour in the chrome (the IMCI tier colours are content, not chrome)
- Transplant test failure: if you can swap "PocketTriage" for "[any other AI product]" and the design still works, kill it

### Constraints driven by content

- Must show: hero pitch + tier output, airplane-mode evidence, architecture, safety design (with the actual R13–R16 rules visible), distribution outreach (named contacts), "run locally" code block, repo + Space links
- Mobile: judges check on phones too. Single column at < 720px. Hero card scales down but stays legible.
- Accessibility: contrast 4.5:1 body, 7:1 for headlines. The IMCI tier colours must have non-colour cues (icon + text), because someone reviewing this on a colour-blind setup must still know which tier is which.
