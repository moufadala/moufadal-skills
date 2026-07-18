# Durable Python dependencies for Hermes gateway image-generation skills — 2026-07-16

## Context

Moufadal asked to make two already-installed image-generation skills executable from the live Hermes runtime without touching other services:

- Level 1 / `prompt-to-design`: code-rendered images via Pillow; imports `Design` from `/opt/data/skills/media/level-1-image-generator/lib`.
- Level 3 / `cf-image`: Cloudflare Flux wrapper; runs `python3 generate.py ...` from `/opt/data/skills/media/level-3-image-generator` and reads `.env` by walking upward from cwd. Never print or copy that `.env`.

The live container was `hermes-gateway`, image tag `nousresearch/hermes-agent:v2026.7.1`, with `/opt/data` bind-mounted from host `/opt/hermes/data` and Docker socket available. The running terminal `python3` resolved to `/usr/bin/python3`, while a clean `docker run --entrypoint python3 <image>` used `/opt/hermes/.venv/bin/python3`. This mismatch is the key durable-image pitfall.

## Pattern that worked

1. Classify as Yellow/production-affecting: limited to `hermes-gateway`; no stop/restart/recreate of other containers.
2. Snapshot before mutation:
   ```bash
   docker commit --pause=false hermes-gateway nousresearch/hermes-agent:v2026.7.1-pre-image-deps-<TS>
   docker tag sha256:<original-image-id> nousresearch/hermes-agent:v2026.7.1-original-<TS>
   ```
3. Install into the running container as root, because the live runtime user could not write `/usr/local/lib/python3.13/dist-packages` and PEP 668 blocked normal system installs:
   ```bash
   docker exec -u root hermes-gateway uv pip install \
     --system --python /usr/bin/python3.13 --break-system-packages --only-binary=:all: \
     pillow==12.3.0 numpy==2.5.1 python-dotenv==1.2.2 requests==2.34.2
   docker exec -u root hermes-gateway uv pip install \
     --python /opt/hermes/.venv/bin/python3 --only-binary=:all: \
     pillow==12.3.0 numpy==2.5.1 python-dotenv==1.2.2 requests==2.34.2
   ```
4. Build a clean durable image from the original tag rather than relying only on `docker commit` of the mutated live layer:
   ```Dockerfile
   FROM nousresearch/hermes-agent:v2026.7.1-original-<TS>
   RUN uv pip install --system --python /usr/bin/python3.13 --break-system-packages --only-binary=:all: \
       pillow==12.3.0 numpy==2.5.1 python-dotenv==1.2.2 requests==2.34.2 \
    && uv pip install --python /opt/hermes/.venv/bin/python3 --only-binary=:all: \
       pillow==12.3.0 numpy==2.5.1 python-dotenv==1.2.2 requests==2.34.2
   ```
5. Tag the durable image for future recreate without restarting now:
   ```bash
   docker build -t nousresearch/hermes-agent:v2026.7.1-image-deps-<TS> .
   docker tag nousresearch/hermes-agent:v2026.7.1-image-deps-<TS> nousresearch/hermes-agent:v2026.7.1
   ```

## Verification commands

Use both Python entrypoints for image durability:

```bash
docker run --rm --entrypoint python3 nousresearch/hermes-agent:v2026.7.1-image-deps-<TS> \
  -c "import PIL,numpy,dotenv,requests,sys; print(sys.executable); print(PIL.__version__, numpy.__version__, requests.__version__)"

docker run --rm --entrypoint /usr/bin/python3 nousresearch/hermes-agent:v2026.7.1-image-deps-<TS> \
  -c "import PIL,numpy,dotenv,requests,sys; print(sys.executable); print(PIL.__version__, numpy.__version__, requests.__version__)"
```

Then run the skill smoke tests from the live runtime:

```bash
python3 -c "import sys; sys.path.insert(0,'/opt/data/skills/media/level-1-image-generator/lib'); from render import Design; d=Design('1:1'); d.fill((238,238,232)); d.write(0.5,0.52,'OK',role='display',weight='bold',size=90,color=(30,30,30),align='center'); d.save('/tmp/l1_test.png'); print('L1 OK')"

cd /opt/data/skills/media/level-3-image-generator && \
python3 generate.py "a single red circle, flat vector, white background" -o /tmp/l3_test.jpg
```

If Cloudflare returns a moderation error for the exact prompt, do not conclude dependencies failed. Re-run with a bland alternate prompt such as:

```bash
python3 generate.py "simple blue square, flat vector, white background" -o /tmp/l3_test_alt.jpg
```

A successful alternate prompt proves the wrapper, deps, `.env` loading, and API path execute; the original failure is provider moderation.

## Pitfalls

- `docker commit` of the live container captures the writable layer and may accidentally include runtime state. Prefer a clean Dockerfile build from the original image for the durable artifact, and keep the commit as rollback/snapshot only.
- Installing only into `/usr/bin/python3.13` can pass live Hermes tests but fail clean image smoke tests because `docker run --entrypoint python3` may resolve to `/opt/hermes/.venv/bin/python3`.
- Installing only into the venv can pass clean image defaults but fail the live terminal runtime when it uses `/usr/bin/python3`.
- Do not print, copy, or commit `/opt/data/skills/media/level-3-image-generator/.env`; `/opt/data` should remain a runtime bind mount and not be part of the image build context.
- Retagging `nousresearch/hermes-agent:v2026.7.1` changes what a future compose recreate will use, but the currently running container still shows the old image id until it is deliberately recreated.

## Rollback

```bash
docker tag nousresearch/hermes-agent:v2026.7.1-original-<TS> nousresearch/hermes-agent:v2026.7.1
```

If the live container itself must be rolled back, recreate only `hermes-gateway` from that tag with explicit user approval; do not restart unrelated services.
