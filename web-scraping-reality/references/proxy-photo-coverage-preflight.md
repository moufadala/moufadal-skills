# Proxy/mobile preflight + photo coverage gates

Use this reference when a scraping run depends on the user's mobile/Tailscale exit node or when the deliverable is a photo-complete real-estate dataset.

## Mandatory proxy preflight before anti-bot conclusions

If a run will use the VPS mobile proxy/Tailscale path, do **not** start by interpreting HTTP 403/503, CAPTCHA, resets, or missing data as site anti-bot. First:

1. Ask/verify the unavoidable user-side action: Tailscale must be **ON** on the phone and the expected exit node active.
2. Smoke the direct IP and the SOCKS path separately.
3. For Playwright/CDP, pass the proxy explicitly at browser launch (`socks5://127.0.0.1:1055` in this VPS setup). Do not rely on `ALL_PROXY` alone.
4. Only after the proxy smoke passes should you classify a site as blocked, fragile, or anti-bot protected.

User correction that triggered this: if the phone Tailscale is OFF, several sites can look blocked even though the run setup is wrong. This is a first-class precondition, not a minor reminder.

## Photo completeness is not `image_url IS NOT NULL`

For photo-driven real-estate outputs, a non-empty `image_url` is only a first pass. A valid listing photo gate should reject:

- SVG/UI assets (`.svg`, chevrons, social/share icons)
- logos, favicons, agency marks, sprites
- placeholders / blank / no-photo / default avatars
- DPE badges or non-property media
- broken URLs, 404/403 that are not resolvable with the correct source referer

Recommended QA:

1. Count active listings with missing `image_url`.
2. Sample or fully check image URLs with HTTP HEAD/GET.
3. Require content type like `image/jpeg`, `image/png`, or `image/webp` for “real photo” status.
4. Verify visible cards in browser: `img.complete && img.naturalWidth > 0`.
5. If an image is broken and a detail page has multiple unrelated recommendation images, do **not** inject a likely-wrong fallback; classify or deactivate the listing instead.

## Product rule distinction

Keep separate:

- **Database truth**: all scraped/known listings and their raw fields.
- **Active presentation set**: listings that pass product gates such as real photo availability.
- **Exception/secondary set**: no-photo or blocked-source listings that should not silently disappear if the user wants opportunity tracking.

For photo-first dashboards, prefer an explicit hybrid product rule: main results show only photo-valid listings; secondary review section tracks no-photo/broken/blocked listings.