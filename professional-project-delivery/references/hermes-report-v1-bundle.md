# Hermes Report V1 bundle

Use this reference with `templates/hermes-report-v1.html` and `scripts/validate_hermes_report_v1.py` when producing evidence-rich static reports.

## Source-map contract

Write a `source-map.json` next to the report with:

```json
{
  "generated_at": "ISO timestamp",
  "scope": "what the report covers",
  "sources_consulted": [
    {"id": "short-id", "title": "...", "url": "...", "status": "consulted|extracted|verified", "theme": "...", "takeaway": "..."}
  ],
  "sources_failed_or_limited": [
    {"url": "...", "status": "failed|limited|search-only", "note": "why it is not proof"}
  ],
  "search_queries_run": ["..."],
  "artifacts": [
    {"path": "/opt/data/...", "type": "html|json|md|log|screenshot", "status": "generated|verified|blocked", "size_bytes": 123, "role": "..."}
  ]
}
```

## Score Hermes V1

- Decision usefulness: 20
- Verifiable evidence: 20
- Provenance clarity: 15
- Scanability/mobile: 15
- Real QA: 15
- Minimal tooling: 10
- Reversibility/next actions: 5

## QA command

```bash
python3 /path/to/professional-project-delivery/scripts/validate_hermes_report_v1.py \
  /opt/data/artifacts/<topic>/report.html \
  --source-map /opt/data/artifacts/<topic>/source-map.json
```

If the VPS convenience copy exists, this equivalent is acceptable:

```bash
python3 /opt/data/templates/hermes-report-v1/validate_report.py \
  /opt/data/artifacts/<topic>/report.html \
  --source-map /opt/data/artifacts/<topic>/source-map.json
```

## Tool-sprawl rule

Do not add React/Vite, Observable, Quarto, Streamlit, Grafana, or W&B just to get tabs/cards. Promote to a heavier stack only when the report has become a durable application with complex state, routing, recurring publication, large data volume, or structured front-end tests.
