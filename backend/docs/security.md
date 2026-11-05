# Authentication and security

## Session cookie

`POST /api/v1/players/login/access-token` checks the credentials and answers `204` with the JWT in a cookie (`access_token`):

- `HttpOnly`: not readable from JavaScript;
- `SameSite=Strict`: never sent on a cross-site request;
- `Secure`: only sent over https. It defaults to `true` unless `ENV=dev`, so local http development works without configuration. Set `COOKIE_SECURE` to override.

`POST /logout` deletes the cookie. The attributes of both calls come from the same helper so that the browser always matches the cookie to clear.

## Cross-site requests

`SameSite` does not stop another site from submitting a form that signs the visitor in as the attacker (login CSRF). State-changing endpoints (signup, login, logout, game creation) therefore also use the `verify_origin` dependency:

- if the request has an `Origin` (or `Referer`) header, its host must be the host the request was sent to, or be listed in `ALLOWED_ORIGINS`; otherwise the answer is `403`;
- requests without these headers (curl, server to server) are let through: they are not browser cross-site requests.

`ALLOWED_ORIGINS` is a JSON list, for example `ALLOWED_ORIGINS='["https://app.example.com"]'`. It is only needed if the frontend is served from another origin than the API.

## Secret key

`SECRET_KEY` signs the JWT, which is the session. Outside `ENV=dev` the application refuses to start while it still has its development default, so a deployment cannot silently ship a publicly known key.
