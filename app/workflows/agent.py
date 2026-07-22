import logging
from pathlib import Path
import shutil

from app.config.settings import settings
from deepagents import FilesystemPermission, create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain_deepseek import ChatDeepSeek
from langgraph.errors import GraphRecursionError


SKILLS_SOURCE_DIR = Path(__file__).resolve().parent.parent / "skills"
SKILL_DIRECTORY_NAME = ".deep_agent_skills"
logger = logging.getLogger("uvicorn.error")


def code_agent_workflow(specification_text: str, workspace_path: str) -> None:
    workspace = Path(workspace_path).resolve()
    skill_directory = workspace / SKILL_DIRECTORY_NAME
    shutil.copytree(SKILLS_SOURCE_DIR, skill_directory)
    logger.info("Deep Agent Skill 已载入，准备调用模型")
    model = ChatDeepSeek(
        model=settings.deepseek_model,
        api_key=settings.deepseek_api_key,
        base_url=settings.deepseek_base_url,
        temperature=settings.deepseek_temperature,
    )
    agent = create_deep_agent(
        model=model,
        backend=FilesystemBackend(root_dir=str(workspace), virtual_mode=True),
        skills=[f"/{SKILL_DIRECTORY_NAME}/"],
        permissions=[
            FilesystemPermission(
                operations=["write"],
                paths=["/*.py"],
                mode="allow",
            ),
            FilesystemPermission(
                operations=["write"],
                paths=["/**"],
                mode="deny",
            ),
        ],
        system_prompt=(
            "你是软件代码生成负责人。完整软件说明书在用户消息中。"
            "先读取 software-code-generation Skill，再严格按该 Skill 完成代码工程。"
            "只能在工作区根目录创建和修改 Python 模块，不能修改上传材料或 Skill。"
        ),
    )
    try:
        agent.invoke(
            {"messages": [{"role": "user", "content": f"完整软件说明书：\n{specification_text}"}]},
            {"recursion_limit": 80, "run_name": "software_code_generation"},
        )
    except GraphRecursionError as exc:
        raise ValueError("代码生成超过 80 个执行轮次仍未完成，请调整生成 Skill") from exc
    logger.info("Deep Agent 已返回")
