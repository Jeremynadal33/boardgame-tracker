# Frontend

React single page app built with Vite and TypeScript, using React Router and CSS modules. There is no state or UI library: the pages call the API through a small `fetch` wrapper.

## Project structure

```ini
frontend/src/
├── main.tsx # Mounts the app
├── App.tsx # Routes and providers
├── api/
│   ├── client.ts # request(): fetch wrapper, ApiError, 401 handler
│   ├── auth.ts # login, logout, signup, current player
│   └── games.ts # list and create games
├── auth/
│   ├── AuthContext.tsx # Current player + login/signup/logout
│   ├── RequireAuth.tsx # Route guard
│   └── initials.ts # Avatar initials
├── components/ # Button, Card, Field, Modal, NavBar, UserMenu, layouts
├── pages/ # Home, Login, Signup, Games, AddGameModal
├── styles/
│   ├── tokens.css # Colors, radii, spacing
│   └── global.css
└── test/ # Vitest setup and fetch mock
```

## Dev server

`vite` proxies `/api` to `http://localhost:8000`, so the app talks to the backend on its own origin exactly like in production. Run the backend first, then `npm run dev`.

## Authentication

The session is an `HttpOnly` cookie set by the backend, so the app never sees the token. `AuthProvider` asks `/players/me` once at startup to know who is logged in.

- Every login, signup and logout bumps a generation counter: a slower response to an older request (for example the startup check answering `401` after a successful login) is ignored instead of overwriting the newer state.
- Any `401` from the API (other than that startup check) signs the player out, and `RequireAuth` sends them back to `/login`.
- Logout always clears the player locally, even if the request fails.

## Conventions

- **Colors** come from `tokens.css`. Text colors must keep a 4.5:1 contrast on the page surfaces (WCAG AA); `--color-text-muted` and `--color-label` were darkened for that reason.
- **Modal** is a native `<dialog>` opened with `showModal()`: it traps the focus, inerts the page, scrolls when taller than the viewport and closes on Escape or a click on the backdrop. jsdom does not implement `showModal`, so `src/test/setup.ts` provides a minimal stand-in.
- **Tests** (`npm run test:ci`) render the whole `<App />` with `fetch` mocked by `mockApi`, which accepts handlers returning a promise to reproduce races.
