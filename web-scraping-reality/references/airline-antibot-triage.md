# Airline anti-bot triage notes — French Bee / Amadeus pattern

Session-derived class pattern for airline scraping when browser automation hits anti-bot or protocol errors.

## Key lesson

Do not assume all airline blocks are CAPTCHA/browser problems. Classify the obstacle per site and push one source end-to-end.

For French Bee-like flows, a browser `ERR_HTTP2_PROTOCOL_ERROR` did not mean the source was unusable. `curl_cffi` with browser impersonation could fetch the French Bee/Drupal pages and submit the reservation form, generating a dynamic Amadeus `ENC` redirect. The remaining block was on the final Amadeus/Akamai hop (`Pardon Our Interruption`).

## Reusable workflow

1. **HTTP-first probe**
   - Use `curl_cffi.requests.Session()` with Chrome impersonation.
   - Fetch the public booking page.
   - Save HTML, response headers, cookies, title, and redirect chain.

2. **Parse forms fully**
   - Use BeautifulSoup to list all forms, inputs, selects, hidden fields, and full options.
   - Do not truncate options when airport codes may be deep in a select list.

3. **Replay origin-site POST**
   - Preserve session cookies.
   - POST realistic booking fields.
   - Disable blind redirects initially (`allow_redirects=False`).
   - Capture 302 `Location` fully.

4. **Classify the next hop**
   - If redirect points to Amadeus `plnext/.../Override.action?...ENC=...`, origin-site form generation is solved.
   - If the follow shows `Pardon Our Interruption`, classify the remaining obstacle as Amadeus/Akamai, not the origin site.

5. **Escalate in order**
   - Exact headers/cookies/referrer/sec-fetch reproduction.
   - `curl_cffi` impersonation variants.
   - Open the generated `Override.action` URL in persistent CDP/nodriver/headful Chrome.
   - Compare HTTP vs browser headers/cookies.
   - Only then consider residential/mobile proxy or commercial unlocker.

## Evidence to save

- Generated `Override.action` URL with dynamic `ENC` (redact if needed).
- Request/response headers and cookies for GET booking page, POST form, redirect response, and Amadeus follow.
- Screenshot/title/body excerpt of final block page.
- A report stating which layer is solved and which layer remains blocked.

## Pitfall

Avoid broad parallel skimming. The user expects one promising source pushed end-to-end before broadening. For airline sites, maintain a per-site matrix: accessible layer, blocker layer, evidence files, next experiment, and stop condition.
