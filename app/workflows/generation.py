from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
import logging
import shutil

from app.tools.zip_tool import find_specification_docx, read_docx, unzip
from app.workflows.agent import code_agent_workflow
from app.workflows.build_code_docx import build_code_docx_workflow


OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "outputs"
logger = logging.getLogger("uvicorn.error")


def generate_archive(zip_path: str, output_name: str, update_stage: Callable[[str], None]) -> str:
    with TemporaryDirectory() as workspace:
        logger.info("正在解压上传材料：%s", output_name)
        update_stage("extracting")
        unzip(zip_path, workspace)
        specification_text = read_docx(find_specification_docx(workspace))

        logger.info("正在启动 Deep Agent：%s", output_name)
        update_stage("generating")
        code_agent_workflow(specification_text, workspace)

        logger.info("正在填充 Word 并打包：%s", output_name)
        update_stage("packaging")
        shutil.rmtree(Path(workspace) / ".deep_agent_skills", ignore_errors=True)
        now = datetime.now()
        output_directory = f"{now:%Y_%m_%d_%H_%M_%S}_{now.microsecond // 10000:02d}"
        output_zip = OUTPUT_DIR / output_directory / output_name
        output_url = build_code_docx_workflow(workspace, str(output_zip))
        logger.info("生成完成：%s", output_url)
        return output_url
