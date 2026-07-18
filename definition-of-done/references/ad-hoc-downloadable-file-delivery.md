# Ad-hoc downloadable file delivery — proof checklist

Use this when Moufadal asks for a specific local artifact to be downloadable at a raw URL like `http://IP:PORT/file.txt`.

## Do not mark done until

1. Locate the exact source file and record its size.
2. Serve it with a durable process if the link must stay available:
   - Prefer a small Docker/nginx container for raw public port publishing.
   - On this VPS, remember Docker bind mounts resolve on the host side: files visible to Hermes under `/opt/data/...` are mounted from `/opt/hermes/data/...`.
3. Verify from the public URL, not only localhost:
   - `curl -I --max-time 10 URL` returns `200 OK`.
   - `curl URL -o /tmp/...` downloads the expected byte count.
   - `sha256sum` of downloaded file matches source.
4. Name the serving container/process in the final response.
5. Provide an exact rollback command.

## Pitfall

A Python `http.server` that works on `127.0.0.1` can still be unreachable publicly depending on firewall/container/network path. Treat public timeout as not done. Use Docker port publishing or the existing Traefik/static-publication path, then re-test the exact external URL.

## Minimal Docker pattern

```bash
NAME=network-audit-file-server
FILE_DIR=/opt/hermes/data/artifacts

docker rm -f "$NAME" 2>/dev/null || true
docker run -d --name "$NAME" --restart unless-stopped \
  -p 0.0.0.0:9999:80 \
  -v "$FILE_DIR:/usr/share/nginx/html:ro" \
  nginx:alpine
```

Verification:

```bash
URL='http://148.230.103.174:9999/network-architecture-audit-20260701.txt'
curl -sS -I --max-time 10 "$URL"
curl -sS --max-time 15 "$URL" -o /tmp/downloaded.txt
wc -c /tmp/downloaded.txt /opt/data/artifacts/network-architecture-audit-20260701.txt
sha256sum /tmp/downloaded.txt /opt/data/artifacts/network-architecture-audit-20260701.txt
```

Rollback:

```bash
docker rm -f network-audit-file-server
```
