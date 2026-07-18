# Static real-estate dashboard: residential/non-commercial quality layer

## When to use

Use this when publishing or QAing a real-estate dashboard sourced from scraped listings where commercial/non-residential pollution can enter the dataset.

## Pattern

1. **Separate DB-wide audit from product export.**
   - DB-wide gate counts all active rows and classifies `residential_candidate`, `suspect_non_residential`, and `unknown`.
   - Product export may be stricter: active + has usable photo + rent sanity + non-commercial classifier.
2. **Use conservative commercial detection.**
   - Strong signals in title/type/URL: `local commercial`, `local professionnel`, `local médical`, `bureaux`, `box`, `parking`, `garage`, `terrain`, `entrepôt`, `garde-meuble`.
   - Long descriptions are noisy; only reject on explicit commercial phrases, not incidental words like parking, bureau/home office, or `agent commercial`.
3. **Do not overclaim.**
   - If the classifier only excludes obvious commercial suspects, label the UI `résidentielle / non commerciale` or `non commerciale`, not `100% résidentiel`.
4. **Keep dashboard counts explainable.**
   - Report: DB active rows, active rows with image, product export count, default visible count, scenario counts.
5. **Public QA before delivery.**
   - Build static app.
   - Run data audit comparing JSON export against DB rules.
   - Refresh/cache images if used.
   - Verify public URL via curl/DNS and browser/CDP: console errors, visible counters, search/filter behavior, modal/source link, first images loaded.
   - Capture a screenshot artifact.

## VPS-specific implementation notes observed

- Existing nginx/Traefik static dashboard can serve updated bind-mounted files without recreating the Docker container; avoid `docker rm -f` unless the container itself must change.
- Docker daemon paths differ from Hermes paths on this VPS: Hermes `/opt/data/...` corresponds to host `/opt/hermes/data/...` for Docker volume sources.

## Acceptance evidence

A completed patch should include paths/logs for:

- build output;
- JSON/data audit output;
- photo cache report if images are used;
- public QA log for both canonical and compatibility hostnames;
- browser console/interaction result;
- screenshot path;
- handoff markdown with limitations.
