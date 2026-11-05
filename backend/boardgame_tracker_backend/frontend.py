from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

API_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]


def mount_frontend(app: FastAPI, static_dir: Path, api_prefix: str) -> None:
    """Serve the built single page app: hashed assets, then index.html for any other route."""
    static_dir = static_dir.resolve()
    index_file = static_dir / "index.html"
    # The whole API namespace is reserved (/api/v2/... included), not only the current version
    api_namespace = api_prefix.strip("/").split("/")[0]

    app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

    @app.api_route(
        f"/{api_namespace}/{{rest:path}}",
        methods=API_METHODS,
        include_in_schema=False,
    )
    def unknown_api_route(rest: str) -> None:
        raise HTTPException(status_code=404, detail="Not Found")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_frontend(full_path: str) -> FileResponse:
        if full_path == api_namespace:
            raise HTTPException(status_code=404, detail="Not Found")

        try:
            requested_file = (static_dir / full_path).resolve()
        except ValueError:  # e.g. NUL byte in the path
            return FileResponse(index_file)
        if requested_file.is_file() and requested_file.is_relative_to(static_dir):
            return FileResponse(requested_file)
        return FileResponse(index_file)
