# claude-design — extracted workflow reference

Extracted from `/opt/data/skills/creative/claude-design/SKILL.md` during pass `20260703T045015Z`.
Read this reference when the user request reaches this detailed workflow area.

## React Guidance for Standalone HTML

Use plain HTML/CSS/JS by default.

Use React only when:

- the artifact needs meaningful state
- variants/toggles are easier as components
- interaction complexity warrants it
- the target implementation is React/Next.js and fidelity matters

If using React from CDN in standalone HTML:

- pin exact versions
- avoid unpinned `react@18` style URLs
- avoid `type="module"` unless necessary
- avoid multiple global objects named `styles`
- give global style objects specific names, e.g. `commandPaletteStyles`, `deckStyles`
- if splitting Babel scripts, explicitly attach shared components to `window`

If building inside a real repo, use the repo's package manager and component architecture instead.

## Deck Rules

For slide decks, use a fixed-size canvas and scale it to fit the viewport.

Default slide size: 1920×1080, 16:9.

Requirements:

- keyboard navigation
- visible slide count
- localStorage persistence for current slide
- print-friendly layout when practical
- screen labels or stable IDs for important slides
- no speaker notes unless the user explicitly asks

Do not hand-wave a deck as markdown bullets. Create a designed artifact if asked for a deck.

Use 1–2 background colors max unless the brand system requires more.

Keep slides sparse. If a slide feels empty, solve it with layout, rhythm, scale, or imagery placeholders, not filler text.

## Prototype Rules

For interactive prototypes:

- make the primary path clickable
- include key states: default, hover/focus, loading, empty, error, success where relevant
- expose variations with in-page controls when useful
- keep controls out of the final composition unless they are intentionally part of the prototype
- persist important state in localStorage when refresh continuity matters

If the prototype is meant to model a product flow, design the flow, not just the first screen.

## Variation Rules

When exploring, default to at least three options:

1. **Conservative** — closest to existing patterns / lowest risk
2. **Strong-fit** — best interpretation of the brief
3. **Divergent** — more novel, useful for discovering taste boundaries

Variations can explore:

- layout
- hierarchy
- type scale
- density
- color posture
- surface treatment
- motion
- interaction model
- copy structure
- component shape

Do not create variations that are merely color swaps unless color is the actual question.

When the user picks a direction, consolidate. Do not leave the project as a pile of options forever.

## Tweakable Designs in CLI/API Mode

The hosted Claude Design edit-mode toolbar does not exist here.

Still preserve the idea: when useful, add in-page controls called `Tweaks`.

A good `Tweaks` panel can control:

- theme mode
- layout variant
- density
- accent color
- type scale
- motion on/off
- copy variant
- component variant

Keep it small and unobtrusive. The design should look final when tweaks are hidden.

Persist tweak values with localStorage when helpful.

## Content Discipline

Do not add filler content.

Every element must earn its place.

Avoid:

- fake metrics
- decorative stats
- generic feature grids
- unnecessary icons
- placeholder testimonials
- AI-generated fluff sections
- invented content that changes strategy or claims
- owner-facing or agent-facing meta copy in the customer-visible artifact, e.g. “landing page”, “site”, “V2/V3”, “this section explains”, “effect wow”, or explanations of the design strategy. Convert the intent into customer-facing value instead.

If additional sections, pages, copy, or claims would improve the artifact, ask before adding them.

When copy is necessary but not final, mark it as draft or placeholder.

### Marketing homepage vs menu/catalog

For premium marketing pages—especially artisan food, pâtisserie, restaurants, beauty, craft, and boutique services—the homepage should sell desire, trust, and brand posture. Do not dump a full menu, price list, or product catalog into the landing unless the brief explicitly asks for ecommerce-first browsing. Use a separate menu/catalog/pricing page and make the homepage link to it clearly.

Default pattern:
- Homepage: hero, emotional promise, real imagery, a small non-priced editorial glimpse, brand/process proof, and clear CTAs.
- Menu/catalog page: product names, descriptions, prices, variants, availability, and order CTA.
- QA: verify homepage visible text contains no internal/meta terms and no accidental prices; click the menu/catalog CTA and verify details live there.

See `references/marketing-landing-homepage-vs-menu.md` for the checklist and examples.

### Comparing landing-page variants

When the user asks to see a variant (for example a more direct/commercial version versus a premium/editorial version), do not overwrite the canonical page just to demonstrate the idea. Publish a separate preview URL or artifact, keep the visual system mostly stable, change the copy/CTA posture, and verify it as a real page. See `references/landing-variant-preview-workflow.md` for the repeatable workflow and QA checklist.

## Anti-Slop Rules

Avoid common AI design sludge:

- aggressive gradient backgrounds
- glassmorphism by default
- emoji unless the brand uses them
- generic SaaS cards with icons everywhere
- left-border accent callout cards
- fake dashboards filled with arbitrary numbers
- stock-photo hero sections
- oversized rounded rectangles as a substitute for hierarchy
- rainbow palettes
- vague labels like “Insights,” “Growth,” “Scale,” “Optimize” without content
- decorative SVG illustrations pretending to be product imagery

Minimal is not automatically good. Dense is not automatically cluttered. Choose intentionally.

## Typography

Use the existing type system if one exists.

If not, choose type deliberately based on the artifact:

- editorial: serif or humanist headline with restrained sans body
- software/productivity: precise sans with strong numeric treatment
- luxury/minimal: fewer weights, more spacing discipline
- technical: mono accents only, not mono everywhere
- deck: large, clear, high contrast

Avoid overused defaults when a stronger choice is appropriate.

If using web fonts, keep the number of families and weights low.

Use type as hierarchy before adding boxes, icons, or color.

## Color

Use brand/design-system colors first.

If no palette exists:

- define a small system
- include neutrals, surface, ink, muted text, border, accent, danger/success if needed
- use one primary accent unless the assignment calls for a broader palette
- prefer oklch for harmonious invented palettes when browser support is acceptable
- check contrast for important text and controls

Do not invent lots of colors from scratch.

## Layout and Composition

Design with rhythm:

- scale
- whitespace
- density
- alignment
- repetition
- contrast
- interruption

Avoid making every section the same card grid.

For product UIs, prioritize speed of comprehension over decoration.

For marketing surfaces, make one idea land per section.

For dashboards, avoid “data slop.” Only show data that helps the user decide or act.

### News / monitoring dashboard rules

When designing a veille, news-monitoring, RSS, media-monitoring, or current-events dashboard:

- Treat it as a working surface, not a decorative landing page.
- If the user says it must be “livrable maintenant”, stop framing it as draft/pre-prod and ship a self-contained artifact with working controls and verified interactions.
- Every item/card must be action-capable: the title/card should be clickable or the card must include an obvious “open source” link to the original page.
- Avoid ambiguous nested clicks. Prefer a selectable feed item that opens a reader/details pane, with a separate explicit “open source” link inside the reader. Do not make the whole feed card an external link if the card also needs to reveal details.
- Put a short “why this matters / 1-minute summary” behind a click, drawer, details panel, or right-side reader so the user can scan without losing the feed.
- Include the basic expected controls before visual polish: search, source/type filters, priority/relevance view, date/source sorting where useful, and visible source provenance.
- Use real source URLs from the collected data; never ship a feed UI where items cannot take the user to the original article.
- Research familiar product patterns first when the class is common: Feedly/Inoreader/Netvibes/Swello/Talkwalker/Mention-style monitoring surfaces usually imply feeds, folders/categories, filters, source links, saved views, alerts, and reader panes.
- Do not clone an unrelated brand reference. If the user references another prior design/site, extract the intended principle (e.g. “we used the full design toolkit and researched references”), not the literal visual style, unless they explicitly ask for a clone.

See `references/news-monitoring-dashboard-ux.md` for condensed field notes from a session where a decorative first pass was corrected into a real monitoring dashboard.

## Motion

When the artifact is a local watch/brief/dashboard for a non-dev user, treat it as an editorial decision surface, not an ops dashboard.

- Do **not** default to a dark/SaaS/admin aesthetic. Use dark mode only if the user asks or the product context requires it.
- Start with a **“1-minute summary”** or executive brief before the feed.
- Prioritize and deduplicate items before rendering; never dump a uniform wall of cards.
- Use progressive disclosure: show title/source/reason first, then reveal longer summaries or evidence on click.
- Include concrete buckets like “À faire bientôt”, “À surveiller”, and “Sources testées” when useful.
- For the user's MIAM-style preference, use a clear, warm, editorial visual language: cream/light background, generous spacing, human typography such as Montserrat when appropriate, restrained color, and strong scan hierarchy.
- See `references/brief-dashboard-miam-style.md` for the session-derived pattern and verification checklist.
- When the user asks “what are the new items?” from an existing generated brief and wants it “in an HTML page”, use the concise extraction pattern in `references/brief-extraction-html-page.md`: parse only the requested new cards, classify noise honestly, and ship a mobile-readable standalone HTML summary with source links and verification.

## Motion

Use motion as discipline, not theater.

Good motion:

- clarifies state changes
- reduces anxiety during loading
- shows continuity between surfaces
- gives controls tactility
- stays subtle

Bad motion:

- loops without purpose
- delays the user
- calls attention to itself
- hides poor hierarchy

Respect `prefers-reduced-motion` for non-trivial animation.

## Images and Icons

Use real supplied imagery when available.

If an asset is missing:

- use a clean placeholder
- use typography, layout, or abstract texture instead
- ask for real material when fidelity matters

Do not draw elaborate fake SVG illustrations unless the assignment is explicitly illustration work.

Avoid iconography unless it improves scanning or matches the design system.

## Source-Code Fidelity

When recreating or extending a UI from a repo:

1. inspect the repo tree
2. identify the actual UI source files
3. read theme/token/global style/component files
4. lift exact values where appropriate
5. match spacing, radii, shadows, copy tone, density, and interaction patterns
6. only then design or modify

Do not build from memory when source files are available.

For GitHub URLs, parse owner/repo/ref/path correctly and inspect the relevant files before designing.

## Reading Documents and Assets

Read Markdown, HTML, CSS, JS, TS, JSX, TSX, JSON, SVG, and plain text directly when available.

For DOCX/PPTX/PDF, use available local extraction tools if present. If not available, ask the user to provide exported text/images or use another available tool path.

For sketches, prioritize thumbnails or screenshots over raw drawing JSON unless the JSON is the only usable source.

## Copyright and Reference Models

Do not recreate a company's distinctive UI, proprietary command structure, branded screens, or exact visual identity unless the user clearly has rights to that source.

It is acceptable to extract general design principles:

- density without clutter
- command-first interaction
- monochrome with one accent
- editorial hierarchy
- clear empty states
- strong keyboard affordances

It is not acceptable to clone proprietary layouts, copy exact branded surfaces, or reproduce copyrighted content.

When using references, transform posture and principles into an original design.

## Verification

Before final response, verify as much as the environment allows.

Minimum:

- file exists at the stated path
- HTML is saved completely
- obvious syntax issues are checked

Better:

- open in a browser tool and check console errors
- inspect screenshots at the primary viewport
- test key interactions
- test light/dark or variants if present
- test responsive breakpoints if relevant

### Designed course / PDF deliverables

When the user asks for a “cours”, report, deck, or beautiful PDF:

- Do not answer only in chat. Produce a durable artifact: usually `artifacts/<topic>/course.html` plus `course.pdf`.
- Treat the HTML as the designed source of truth, then export PDF from it with Playwright/Chromium using `print_background: true`.
- Include a short verification record in the final response: exact paths, file sizes, and what was actually rendered/exported.
- If vision/screenshot verification fails because of the current provider/config, say so explicitly, but still verify existence and export success by filesystem/tool output.
- For long research + PDF tasks, prefer launching the work in a separate background/job session with logs so the main messaging conversation stays responsive.

If verification is limited by environment, say exactly what was and was not verified.

Never say “done” if the file was not actually written.

## Final Response Format

Keep final responses short.

Include:

- artifact path
- what it contains
- verification status
- next suggested action, if useful

Example:

```text
Created: /path/to/Prototype.html
It includes 3 layout variants, a Tweaks panel for density/theme, and responsive behavior.
Verified: file exists and opened cleanly in browser, no console errors.
Next: pick the strongest direction and I’ll tighten copy + motion.
```

## Portable Opening Prompt Pattern

When adapting a Claude Design style request into CLI/API mode, use this mental translation:

```text
You are running in CLI/API mode, not hosted Claude Design. Ignore references to hosted-only tools or preview panes. Produce complete local design artifacts, usually self-contained HTML with embedded CSS/JS, and verify with available local tools before returning. Preserve the design process: gather context, define the system, produce options, avoid filler, and meet a high visual bar.
```

## Pitfalls

- Do not paste hosted tool schemas into a skill. They cause fake tool calls.
- Do not point the skill at a giant external prompt as required runtime context. That creates drift.
- Do not strip the design doctrine while removing tool plumbing.
- Do not over-ask when the user already gave enough direction.
- Do not under-ask for high-fidelity work with no brand context.
- Do not produce generic SaaS layouts and call them designed.
- Do not claim browser verification unless it actually happened.
