from fastapi import APIRouter, File, UploadFile

from app.api.schemas import GenerationTask, GenerateSubmitResponse
from app.workflows.batch_generation import get_generation_status, submit_generation_files


router = APIRouter(tags=["软著代码生成"])


@router.post("/generate", response_model=GenerateSubmitResponse)
async def generate(files: list[UploadFile] = File(..., description="软著材料 ZIP 文件")) -> GenerateSubmitResponse:
    return GenerateSubmitResponse(task_ids=await submit_generation_files(files))


@router.get("/generate/{task_id}", response_model=GenerationTask)
async def generate_status(task_id: str) -> GenerationTask:
    return get_generation_status(task_id)
