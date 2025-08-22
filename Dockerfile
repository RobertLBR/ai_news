FROM ghcr.io/astral-sh/uv:debian-slim
ADD . /usr/src/app

WORKDIR /usr/src/app
RUN uv sync
CMD ["uv run", "backend/server.py"]
