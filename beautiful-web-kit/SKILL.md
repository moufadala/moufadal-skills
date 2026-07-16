---
name: beautiful-web-kit
version: "1.0.0"
license: MIT
description: >-
  Build genuinely beautiful, "wow-in-a-demo" single-file web pages that run inside
  a strict-CSP Artifact (one self-contained HTML file, inline CSS/JS, zero CDN,
  works on mobile). Use whenever the user asks for a landing page, hero section,
  portfolio, product/marketing page, deck, or any web UI that should look premium
  (Linear / Vercel / Stripe / Aceternity / Godly tier) — and it must ship as a
  shareable link, not a built React app. Reproduces GSAP/Framer-style effects by
  HAND (animated aurora hero, gradient-text shimmer, scroll reveals, glass cards,
  bento grid, marquee, hover lift+glow) because libraries/CDNs are blocked in this
  environment. For a real deployed site that needs React/Tailwind/shadcn, say so
  and route to a build scaffold instead (that is a different, heavier path).
---

# beautiful-web-kit

Make web pages that impress *immediately in a demo*, under the real constraint of
a strict-CSP Artifact: **one HTML file, all CSS/JS inline, no external requests
(no CDN, no web fonts, no remote images), must work on a phone and be shareable as
a link.** You reproduce the "wow" of Aceternity/Godly by hand — you do not import
libraries.

## Two layers — pick the right one first

- **Layer 1 (this skill): now, zero install, ships as an Artifact link.** Inline
  HTML/CSS/JS. ~90% of demo "wow" (animated heroes, reveals, hovers, gradients,
  patterns, marquee) is achievable and often *better* because it is hand-cut and
  loads instantly. Missing: heavy 3D, physics timelines, morphing → that is Layer 2.
- **Layer 2: later, real deployed sites.** Vite + React + Tailwind + Framer Motion
  + shadcn, where Aceternity components actually run. Needs Node + build + hosting.
  If the user truly needs this, **say it plainly and stop** — do not fake it inside
  an Artifact.

**Never import a library or CDN in Layer 1.** shadcn (React) and GSAP-the-library
do not load here. Reproduce the *effect*, not the dependency.

## Non-negotiable constraints (the CSP reality)

1. Single `.html`, all styles in one `<style>`, all script in one `<script>`. No
   external `src`/`href` to other hosts. No `@import` from the web.
2. **Fonts:** system font stack only (`system-ui, -apple-system, "Segoe UI",
   Roboto, Helvetica, Arial, sans-serif`) OR a base64 font embedded inline. Never a
   Google Fonts link. For rich display typography as an *image*, generate it with
   the `prompt-to-design` skill and inline the PNG as a data URI.
3. **Images:** no remote images. Use CSS gradients/SVG you generate inline, or a
   base64 data URI. Decorative art → generate with `prompt-to-design`.
4. **Mobile-first & responsive:** relative units, `clamp()` for type, flexbox/grid,
   `max-width:100%` on media. The page body must never scroll sideways; wide blocks
   (tables, code) scroll inside their own `overflow-x:auto` container.
5. **Accessibility & polish:** honor `@media (prefers-reduced-motion: reduce)` (kill
   or calm animations). Content must be readable with JS disabled (gate reveals so
   they default to *visible*, then animate in — never default to hidden with no JS).
6. **Theme:** unless a single look is intended, style both light and dark via
   `prefers-color-scheme`.

## The effect catalog (hand-cut, copy-and-adapt)

Reach for these instead of a library. Keep motion **calm and premium** — slow eases,
small distances, never flashing. See `references/effects.md` for full snippets.

- **Animated aurora / mesh hero** — 2–3 large blurred radial-gradient blobs on an
  absolutely-positioned layer, drifting with a long `@keyframes` transform loop
  (20–40s), behind `backdrop-filter` content. The signature "premium SaaS" hero.
- **Gradient-text shimmer** — `background: linear-gradient(...)` + `background-clip:
  text; color: transparent`, animate `background-position` for a slow sheen.
- **Scroll reveal** — `IntersectionObserver` adds a class that transitions
  `opacity`/`translateY`. Elements start visible in CSS; JS only *enhances*.
- **Glass cards** — `background: rgba(...)` + `backdrop-filter: blur()` + 1px hairline
  border (`rgba(255,255,255,.1)`) + soft shadow. Hover: lift (`translateY(-4px)`) +
  glow (layered box-shadow in the accent hue).
- **Bento grid** — CSS grid with spanning cells (`grid-column/row: span N`), varied
  tile sizes, one focal tile. The modern "feature wall" layout.
- **Marquee** — duplicate the track, translate `-50%` on a linear infinite loop;
  pause on hover; respect reduced-motion.
- **Micro-interactions** — button sheen on hover, magnetic-ish cursor follow (cheap:
  translate toward pointer within a small range), animated underlines, count-up
  numbers via `requestAnimationFrame`.
- **Generated SVG ornaments** — inline `<svg>` for geometric patterns, arcs, star/
  khatam motifs, dividers. No external icon set; draw or use inline paths.

## Workflow

1. **Clarify the vibe** in one line: reference (Linear/Vercel/Stripe/Apple…), mood,
   accent palette, one hero message, sections needed. If the user pointed to a real
   site's style, also load `popular-web-designs` for its tokens.
2. **Choose palette (3–6 colors)** and one accent. Set them as CSS custom properties
   at `:root` so the whole page is themeable from one place.
3. **Compose structure**: hero → 2–4 sections → footer. One focal element per screen;
   let negative space breathe.
4. **Layer effects** from the catalog — 2–3 signature moves, not ten. Restraint reads
   as premium; clutter reads as cheap.
5. **Generate any imagery** with `prompt-to-design` and inline it as a data URI.
6. **Self-check against the QA gate** below, fix, then present as an Artifact.

## QA gate before you present (all must pass)

- [ ] Single file; no external network request anywhere (no CDN/font/image URL).
- [ ] No horizontal scroll at 360px width; looks right on a phone.
- [ ] Readable with JS off; reveals default to visible.
- [ ] `prefers-reduced-motion` respected; nothing flashes or strobes.
- [ ] Light and dark both acceptable (unless single-look by design).
- [ ] Text contrast passes; tap targets ≥ ~40px.
- [ ] Motion is slow and deliberate — remove anything that feels "busy".

## Complementary skills

- `prompt-to-design` — code-generated PNGs (posters, backgrounds, typographic art)
  to inline as data URIs; fills the "no remote images" gap.
- `popular-web-designs` — real design-system tokens (Stripe, Linear, Vercel…) to
  borrow palette/spacing/type when recreating a known aesthetic.
- `dataviz` — before any chart/KPI tile, for a coherent, accessible visual system.
