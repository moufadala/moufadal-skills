# Marketing landing pages: homepage vs menu/catalog

Session-derived lesson from a pâtisserie landing redesign.

## Core rule

For premium marketing homepages, the homepage should sell the desire and the brand posture; detailed transactional lists belong in a dedicated menu/catalog/pricing surface unless the brief explicitly asks for ecommerce-first browsing.

## When this applies

- Artisan food, bakery, pâtisserie, restaurants, beauty, craft, luxury, boutique services.
- User asks for a landing page to impress, reassure, or “bluff” someone.
- The product list has many items/prices and risks looking like a flyer, spreadsheet, or takeaway menu.

## Recommended structure

Homepage:
- Hero with one clear emotional promise and real imagery.
- A small non-priced “selection” or editorial glimpse, if useful.
- Brand/atelier/process section.
- CTA to `Menu`, `Order`, `WhatsApp`, booking, or inquiry.
- Motion and micro-interactions that support polish without delaying the user.

Dedicated menu/catalog page:
- Product names, descriptions, prices, variants, packs, availability.
- Direct order CTA.
- Clear grouping and scannable cards/lists.

## Copy discipline

Never expose owner-facing or agent-facing meta text in the customer page:
- Avoid phrases like “landing page”, “site”, “V2/V3”, “this section explains”, “not a card in bulk”, “designed to impress”, “effect wow”.
- Convert internal intent into customer-facing value: taste, occasion, craft, trust, ordering simplicity.

## QA checklist

Before shipping a premium landing:
- Search visible text for meta terms: `landing`, `site`, `V2`, `V3`, `page d’accueil`, `effet waouh`, `objectif`, `carte posée`.
- Verify homepage does not expose prices unless pricing is intentionally part of the primary value proposition.
- Click the menu/catalog CTA and verify product/pricing details live there.
- Check console errors and inspect the primary viewport visually.
- If motion is promised, verify the project actually uses a motion layer (CSS, GSAP, Motion/Framer, Lenis, etc.) and respects `prefers-reduced-motion`.
