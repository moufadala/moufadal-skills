# Static dashboard publication + browser-state QA

Use this reference when delivering a static HTML/JS dashboard or one-off web app that the user expects to open from Telegram/mobile.

## Lesson

A local artifact path is not a usable product link. For user-facing delivery, verify the exact URL the user will open, not only the file on disk or localhost. If server-side QA passes but the user reports “nothing works”, stop adding more URLs blindly: first split the failure with a tiny static `status.html`/health page, then test the full app with a deterministic reset URL so you can distinguish DNS/network failure from JavaScript/state/product failure.

## Publication checklist

1. **Artifact exists locally**
   - Verify `index.html` and data files exist and parse.
   - If JSON is embedded in `<script type="application/json">`, confirm the raw text parses with `JSON.parse`/`json.loads`.
   - Do not HTML-escape the JSON payload as `&quot;` inside the JSON script tag. Escaping is appropriate for HTML attributes, not for application/json content.

2. **Serve it somewhere reachable**
   - Start or identify an HTTP server.
   - Test localhost only as a backend check, not as final proof.
   - Test the public URL from the runtime/network path the user will use.
   - If DNS is dual-stack, check A and AAAA records and test both IPv4 and IPv6; a stale AAAA can make an otherwise valid IPv4 service fail for some mobile clients.
   - If a direct port works locally but times out publicly, treat it as an exposure/firewall/routing issue, not an app bug.
   - Prefer one canonical URL in the handoff. If a fallback URL is necessary, label it clearly and avoid flooding the user with several “maybe” links.

3. **Avoid silently pointing at an old public artifact**
   - If an old dashboard already exists at a nice URL, compare its served HTML/data with the newly generated artifact before telling the user to use it.
   - A public route returning `200` is not proof that it serves the current build.

4. **Temporary tunnel is acceptable when labeled**
   - For fast user validation, a quick Cloudflare tunnel can publish a local server without firewall/Traefik mutation.
   - Label it clearly as temporary/non-production.
   - Keep the server/tunnel process IDs visible when useful.
   - Still plan a durable route afterward: Traefik, nginx, systemd service, or existing dashboard static directory with correct ownership.

## Browser-state QA checklist

Generated dashboards often persist filters in `localStorage`. QA must test both fresh and dirty sessions.

1. Clear/preset state explicitly:
   - Run `localStorage.clear(); location.reload()` or use a cache-busting URL before fresh-state QA.
   - For user-facing recovery links, add a deterministic reset parameter such as `?reset=1` that clears the app's persisted state before bootstrapping. Do not make the user manually clear browser data from Telegram/mobile.
   - Then verify default counts and visible cards.

2. Test reset/clear actions as user flows:
   - Click `Tout effacer` / reset buttons.
   - Assert DOM state and localStorage state: filters unchecked, numeric inputs empty, search empty, visible count expected.
   - Do not rely only on a visual snapshot.

3. If a click appears not to work:
   - Inspect the loaded handler with `document.querySelector('#button').onclick?.toString()`.
   - Compare loaded HTML/JS against the local source to catch stale cache/tunnel/server issues.
   - Trigger `document.querySelector('#button').click()` to distinguish browser-tool ref staleness from an app bug.

4. Test real value flows:
   - Example: clear filters → search `Moufia` → assert nonzero result count and first card text.
   - Click a card → assert modal opens and source link/photo URL are populated.
   - Re-check console/page errors after interaction.

## User-facing recovery when the user says “nothing works”

Do not answer defensively with “it works here” or dump multiple URLs. Reproduce from the outside, then simplify the user path.

1. Re-test the exact public URLs with HTTP and browser tooling.
2. Create or expose a tiny `/status.html` page on the same host that proves DNS/TLS/reverse-proxy/static serving independent of the heavy JS app.
3. Provide **one** canonical link first, ideally including `?reset=1` for a clean state. Put alternate/legacy links only in the technical notes.
4. If `/status.html` works but `/` does not, debug app JS/cache/state/assets. If `/status.html` fails, debug DNS/TLS/reverse proxy/network before touching UI code.
5. Include a screenshot or browser snapshot of the canonical link, not just curl output.

## Common root causes

- Local build updated but public route serves an older root-owned copy.
- Public port closed even though localhost returns `200 OK`.
- JSON embedded into HTML escaped for attributes instead of raw JSON script content.
- Reset handler calls a generic save function that re-reads stale DOM values and reintroduces old filters.
- Default state uses keys that do not match filter keys (`types` vs `property_type`, `sources` vs `source_site`).
- Post-build processors rewrite embedded JSON from only the main data file and silently drop secondary datasets (e.g. `suspects`).
- Mobile parity/local-state dashboards have an expanded reference: `references/mobile-static-dashboard-parity-and-local-state.md`.

## Acceptance wording

A final delivery should include:

- Public URL the user can open.
- Whether the URL is temporary or durable.
- Exact checks performed: HTTP status, data count, console errors, key interactions.
- Known limitations and the next durable publication step.
