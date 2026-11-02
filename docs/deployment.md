# Deployment

## The image

The root `Dockerfile` has two stages:

1. **frontend**: `npm ci && npm run build` produces the static app.
2. **runtime**: installs the backend with `uv` (pinned version, `--frozen`), copies the static app to `/app/static` and starts `fastapi run` on port `8080`.

The container runs as the unprivileged user `app` (uid `10001`). `/data` is created and owned by that user before `VOLUME`, so a fresh named volume is writable and holds the SQLite database.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `ENV` | `dev` | Anything but `dev` is production: `COOKIE_SECURE` defaults to `true` and `SECRET_KEY` becomes mandatory. The image sets `prod`. |
| `SECRET_KEY` | dev-only value | Signs the JWT stored in the session cookie. **Required** outside `dev`: the app refuses to start with the default. |
| `COOKIE_SECURE` | `ENV != dev` | Set to `false` only if the app is served over plain http. |
| `ALLOWED_ORIGINS` | `[]` | JSON list of extra origins allowed to call state-changing endpoints (see [security](Backend/security.md)). |
| `DATABASE_URL` | `sqlite:///boardgame_tracker.db` | The image sets `sqlite:////data/boardgame_tracker.db`. |
| `STATIC_DIR` | unset | Directory of the built frontend. When unset, only the API is served. |

## Releases

Releases are driven by [release-please](https://github.com/googleapis/release-please) from conventional commits on `master`:

- every push to `master` updates a release pull request (changelog and version bump);
- merging it creates the `vX.Y.Z` tag and pushes `ghcr.io/jeremynadal33/boardgame-tracker:X.Y.Z` and `:latest`;
- the **Release snapshot** workflow can be started by hand to push a development build (`X.Y.Z.devN-gSHA`).

## Homelab

The image runs on the homelab behind Traefik, which terminates TLS. The stack lives in the homelab repository (`catalog/boardgame-tracker`, enabled per environment in `envs/<env>/boardgame-tracker`).

- **Routing**: Traefik labels come from the shared `router_labels` helper, the container joins the `traefik-frontend` network and listens on `8080`.
- **Forwarded headers**: `FORWARDED_ALLOW_IPS=*` is set so that redirects built by the app keep the `https` scheme. This is safe because the container is only reachable through the Traefik network.
- **Secrets**: `SECRET_KEY` comes from a GitHub secret of the homelab repository, injected by its CD workflow.
- **Data**: the named volume mounted on `/data` holds the database.
- **Versions**: production pins an explicit image tag, `latest` is rejected by the homelab CI.

## Documentation site

This site is built with MkDocs (Material theme, `monorepo` plugin to include `backend/docs` and `frontend/docs`).

- Pull requests that touch the docs run `mkdocs build --strict`: a broken link or a missing page fails the build.
- Pushes to `master` publish the site to GitHub Pages.

To preview locally:

```bash
uv run --group docs mkdocs serve -a 127.0.0.1:8001
```
