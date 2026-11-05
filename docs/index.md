# Boardgame Tracker

A board game tracking application that allows you to record game scores, edit past game sessions, and create leagues for leaderboards. The app helps you determine which of your friends is the best board game player through competitive scoring and rankings.

It ships as a **single image**: the FastAPI backend serves both the JSON API (`/api/v1`) and the built React app, so everything lives on one origin and the session cookie never crosses sites.

| Part | What it is | Docs |
| --- | --- | --- |
| `backend/` | FastAPI + SQLModel + SQLite API | [Backend](Backend/index.md) |
| `frontend/` | React + Vite single page app | [Frontend](Frontend/index.md) |
| `Dockerfile` | Multi-stage build of both | [Deployment](deployment.md) |

Setting the project up locally is covered by the `README.md` at the root of the repository.

## To check later for production level application

* [Better security handling of tokens](https://github.com/fastapi/full-stack-fastapi-template/issues/189)
* Request rate limit
