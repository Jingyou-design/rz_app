from pathlib import Path
import zipfile

from app.tools.word_tool import concat_py_files, fill_new_content
from app.tools.zip_tool import find_specification_docx


OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "outputs"


def build_code_docx_workflow(workspace_path: str, output_path: str) -> str:
    workspace = Path(workspace_path)
    source_files = sorted(workspace.glob("*.py"))
    template_files = [path for path in workspace.rglob("*.docx") if "软件代码" in path.name and not path.name.startswith("~$")]
    form_files = [path for path in workspace.rglob("*.txt") if "系统填报说明" in path.name]
    if not source_files:
        raise FileNotFoundError("未找到生成的 Python 代码文件")
    if not template_files:
        raise FileNotFoundError("未找到软件代码 DOCX 模板")
    if not form_files:
        raise FileNotFoundError("未找到系统填报说明 TXT 文件")

    output_zip = Path(output_path)
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    output_docx = output_zip.with_name("软件代码.docx")
    fill_new_content(str(template_files[0]), str(output_docx), concat_py_files([str(path) for path in source_files]))
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(output_docx, "软件代码.docx")
        archive.write(find_specification_docx(workspace), "软件说明书.docx")
        archive.write(form_files[0], "系统填报说明.txt")
    output_docx.unlink(missing_ok=True)
    return f"/outputs/{output_zip.relative_to(OUTPUT_DIR).as_posix()}"
