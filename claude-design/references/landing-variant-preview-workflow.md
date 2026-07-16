# Landing variant preview workflow

Use when a user asks to “show me the variant” or compare a commercial/direct copy direction against the current premium/artisanal homepage.

## Pattern

1. **Do not replace the canonical page.** Publish a clearly separate preview URL or local artifact so the user can compare variants side by side.
2. **Change one dimension first.** For a “direct commercial” variant, keep the visual system stable and primarily adjust:
   - hero H1/subtitle toward action and benefit;
   - section labels toward decision/order flow;
   - CTAs toward menu/contact;
   - supporting copy toward ease, gifting, sharing, and ordering.
3. **Keep strategic constraints intact.** For premium food/artisan pages, homepage remains desire/trust/CTA; prices and detailed catalog stay on the menu page unless explicitly requested.
4. **Avoid customer-visible meta labels.** A preview can be described in chat, but the page itself should not show “preview”, “variant”, “V4”, “landing page”, “effect wow”, or other agent/design-process labels.
5. **Verify like a real page.** At minimum:
   - preview URL returns HTTP 200;
   - menu/catalog CTA returns HTTP 200;
   - browser console has zero JS errors;
   - homepage visible text has no price-like strings if prices must stay off homepage;
   - homepage visible text has no meta/internal terms.
6. **Give an honest recommendation.** Frame the tradeoff: direct/commercial variants usually improve immediate ordering clarity but can reduce premium/editorial brand posture.

## Useful copy transformation examples

Premium/editorial:
- “Fait à la main. Fait avec l’île.”
- “Chaque pièce commence par une intention simple : faire plaisir avec justesse.”

Direct/commercial:
- “Commandez des douceurs qui font vraiment plaisir.”
- “Des gourmandises artisanales prêtes à offrir, partager ou apporter.”
- “Simple à choisir. Simple à commander. Soigné à recevoir.”

## Publishing note

If the production build/output directory is not writable or should not be touched, create a separate static preview directory/container or local artifact rather than forcing changes into production. Ensure served HTML/CSS files are readable by the web server (e.g. not `0600` when served by nginx).