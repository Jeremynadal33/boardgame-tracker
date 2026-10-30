from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


def mount_frontend(app: FastAPI, static_dir: Path, api_prefix: str) -> None:
    """Serve the built single page app: hashed assets, then index.html for any other route."""
    static_dir = static_dir.resolve()
    index_file = static_dir / "index.html"
    api_path = api_prefix.strip("/")

    app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_frontend(full_path: str) -> FileResponse:
        if full_path == api_path or full_path.startswith(f"{api_path}/"):
            raise HTTPException(status_code=404, detail="Not Found")

        requested_file = (static_dir / full_path).resolve()
        if requested_file.is_file() and requested_file.is_relative_to(static_dir):
            return FileResponse(requested_file)
        return FileResponse(index_file)
