# Vite app publication under a clean HTTPS host while preserving subpath assets

Use this when a Vite/React static build was compiled with a non-root `base`, e.g. `base: '/miham/'`, but the user wants a clean public host such as `https://miham.example/`.

## Problem signature

- The public root `https://host/` returns `index.html` with HTTP 200.
- Browser page is blank or empty.
- Console may be quiet at first, but JS/CSS/image assets are referenced under `/miham/...`.
- `https://host/assets/...` works or the static container serves a folder directly, but `https://host/miham/assets/...` returns 404.

This is not a React bug. The Vite build is doing what it was told: all assets are rooted under `/miham/`.

## Durable fix pattern

Mount the **parent directory** of the subpath into nginx, not the subpath directory itself, and make nginx serve the subpath index at `/`.

Example filesystem:

```text
/opt/data/artifacts/morning-brief/
  miham/
    index.html
    assets/index-xxx.js
    assets/index-xxx.css
    images/logo.png
```

Docker/Traefik static container should mount:

```bash
-v /opt/hermes/data/artifacts/morning-brief:/usr/share/nginx/html:ro
```

Nginx config:

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location = / {
        try_files /miham/index.html =404;
    }

    location = /status.html {
        add_header Content-Type text/html;
        return 200 '<!doctype html><html><body>OK app</body></html>';
    }

    location /miham/ {
        try_files $uri $uri/ /miham/index.html;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## QA gate

After publication, verify both the clean root and the build base path:

```bash
HOST='miham.example.com'
curl -L -sS -o /tmp/root.html -w 'HTTP %{http_code} %{size_download} %{content_type}\n' "https://$HOST/"
curl -L -sS -o /tmp/sub.html  -w 'HTTP %{http_code} %{size_download} %{content_type}\n' "https://$HOST/miham/"
python3 - <<'PY'
from pathlib import Path
import re, subprocess, sys
html = Path('/tmp/root.html').read_text(errors='ignore')
paths = re.findall(r'/(miham/(?:assets|images)/[^"\']+)', html)
for p in paths[:20]:
    url = 'https://miham.example.com/' + p
    r = subprocess.run(['curl','-L','-sS','-o','/dev/null','-w','%{http_code} %{size_download} %{content_type}', url], text=True, capture_output=True)
    print(p, r.stdout.strip())
    if not r.stdout.startswith('200 '): sys.exit(1)
PY
```

Then open the exact clean URL in the browser tool and check:

- user-visible content is rendered, not just `index.html` returned;
- critical links/CTAs are present;
- JS console has zero blocking errors;
- screenshot/visual check confirms the intended design, not a stale build.

## Pitfalls

- Mounting `/.../miham` directly to `/usr/share/nginx/html` while `index.html` references `/miham/assets/...` produces 404s for runtime assets.
- Testing only `curl https://host/` is insufficient; the HTML can be 200 while the app is blank.
- If the Docker daemon sees host paths differently from Hermes, prove the Docker-visible path first with a throwaway `docker run -v ... test -s /check/index.html`.
