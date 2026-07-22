from pydantic import BaseModel, Field


class GenerateSubmitResponse(BaseModel):
    task_ids: list[str] = Field(..., description="已提交的生成任务 ID 列表")


class GenerationTask(BaseModel):
    task_id: str = Field(..., description="生成任务 ID")
    filename: str = Field(..., description="用户上传的 ZIP 文件名")
    zip_path: str = Field(..., exclude=True, description="上传 ZIP 的临时保存路径")
    status: str = Field(default="pending", description="任务状态")
    output_url: str | None = Field(default=None, description="生成结果 ZIP 下载地址")
    error: str | None = Field(default=None, description="失败原因")
