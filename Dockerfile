FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple
ENV UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY app ./app
COPY static ./static

RUN mkdir -p uploads outputs temp

EXPOSE 8001

CMD ["/app/.venv/bin/python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
