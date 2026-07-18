# Pre-wakeup clickable HTML report index — 2026-06-29

## Trigger / user requirement

Moufadal asked that at wake-up around **07:00 Réunion time**, all reports and research results be delivered as **complete, exhaustive, clickable HTML**, not as scattered Telegram logs or raw file paths.

This is a class-level reporting requirement for overnight / long-running research, benchmarks, code-review, immo, Graphify, or other agent work that writes artifacts under `/opt/data/artifacts`.

## Durable pattern

1. Do not paste long logs into Telegram.
2. Generate a mobile-readable HTML index before the user wakes up.
3. Index recent artifacts from `/opt/data/artifacts` over a bounded window, normally last 24h.
4. Include HTML, Markdown converted to HTML, PDF, JSON, TXT, and log evidence where safe.
5. Copy indexed files into a web-served mirror so all links work from Android.
6. Send only a short Telegram message with:
   - latest clickable report URL;
   - dated archive URL;
   - artifact count;
   - category summary;
   - explicit limits if any.
7. Keep public mirror bounded with retention, e.g. 7 days, because overnight research can create thousands of files.

## Implementation used in this session

Script created:

```bash
/opt/data/scripts/prewake_html_report_index.py --hours 24 --keep-days 7
```

Cron created:

```text
name: prewake-html-reports-0700-reunion
schedule: 0 3 * * *  # 07:00 Réunion
script: prewake_html_report_index.py --hours 24 --keep-days 7
no_agent: true
```

Public HTTPS mirror chosen after QA:

```text
https://immo.148.230.103.174.sslip.io/morning-reports/latest.html
https://immo.148.230.103.174.sslip.io/morning-reports/<YYYY-MM-DD>/index.html
```

Local live mirror:

```text
/opt/data/artifacts/morning-brief-live/research/latest.html
/opt/data/artifacts/morning-brief-live/research/<YYYY-MM-DD>/index.html
```

## Important pitfall found

The Morning Brief local watchdog served `/opt/data/artifacts/morning-brief-live` on `127.0.0.1:8091`, but the public `http://148.230.103.174:8091` endpoint still exposed the legacy root-owned `/opt/data/artifacts/morning-brief` directory. That made local QA pass while the public `/research/latest.html` returned 404.

Do not assume local `127.0.0.1` and public IP serve the same directory. Always verify the exact public URL that will be sent to Telegram.

When the public 8091 path is root-owned or stale, publish the wake-up index under an already verified HTTPS static app path instead of fighting permissions mid-run.

## QA gates before saying ready

Run these checks or their equivalents:

```bash
PYTHONDONTWRITEBYTECODE=1 /opt/data/scripts/prewake_html_report_index.py --hours 24 --keep-days 7
curl -fsS -I https://immo.148.230.103.174.sslip.io/morning-reports/latest.html
python3 - <<'PY'
import re, urllib.request, ssl
base='https://immo.148.230.103.174.sslip.io/morning-reports/'
ctx=ssl.create_default_context()
html=urllib.request.urlopen(base+'latest.html', context=ctx, timeout=30).read().decode('utf-8','ignore')
hrefs=re.findall(r"<a href='([^']+)'", html)
print('href_count', len(hrefs))
assert hrefs
r=urllib.request.urlopen(base+hrefs[0], context=ctx, timeout=30)
print('first_href_status', r.status, r.headers.get('content-type'))
assert r.status == 200
PY
```

Also check disk pressure:

```bash
df -h /opt/data
```

If usage is high, report it as a real limitation and keep the mirror retention bounded.

## Reporting shape

Final Telegram should be short and operational:

- Verdict: scheduled and verified / partially blocked.
- Where to click: latest HTML URL + dated archive.
- What is included: artifact count and categories.
- Proof: public HTTP status and internal-link check.
- Limits: source directory coverage and disk pressure.
- Reprise / rollback commands.
