from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.router import router


app = FastAPI(title="软著代码生成系统")

ROOT_PATH = Path(__file__).resolve().parent.parent
UPLOAD_DIR = ROOT_PATH / "uploads"
OUTPUT_DIR = ROOT_PATH / "outputs"
STATIC_DIR = ROOT_PATH / "static"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")
app.include_router(router)


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
