import asyncio
from pathlib import Path
from tempfile import NamedTemporaryFile
import uuid

from fastapi import HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from app.api.schemas import GenerationTask
from app.workflows.generation import generate_archive


MAX_CONCURRENT_GENERATIONS = 5
_generation_semaphore = asyncio.Semaphore(MAX_CONCURRENT_GENERATIONS)


_tasks: dict[str, GenerationTask] = {}


async def submit_generation_files(files: list[UploadFile]) -> list[str]:
    if not files:
        raise HTTPException(status_code=400, detail="请至少上传一个 ZIP 文件")
    if any(not (file.filename or "").lower().endswith(".zip") for file in files):
        raise HTTPException(status_code=400, detail="仅支持 ZIP 格式的上传文件")

    task_ids: list[str] = []
    for file in files:
        task_id = uuid.uuid4().hex
        output_name = Path(file.filename or "生成结果.zip").name
        with NamedTemporaryFile(suffix=".zip", delete=False) as temp_file:
            while chunk := await file.read(1024 * 1024):
                temp_file.write(chunk)
            zip_path = temp_file.name
        await file.close()
        _tasks[task_id] = GenerationTask(task_id=task_id, filename=output_name, zip_path=zip_path)
        asyncio.create_task(_run_generation(task_id))
        task_ids.append(task_id)
    return task_ids


def get_generation_status(task_id: str) -> GenerationTask:
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="生成任务不存在")
    return task


async def _run_generation(task_id: str) -> None:
    task = _tasks[task_id]
    try:
        async with _generation_semaphore:
            task.status = "in_progress"
            task.stage = "extracting"
            task.output_url = await run_in_threadpool(
                generate_archive,
                task.zip_path,
                task.filename,
                lambda stage: setattr(task, "stage", stage),
            )
            task.status = "completed"
            task.stage = "completed"
    except Exception as exc:
        task.status = "failed"
        task.stage = "failed"
        task.error = str(exc) or "生成失败"
    finally:
        Path(task.zip_path).unlink(missing_ok=True)
