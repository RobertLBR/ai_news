FROM ghcr.io/astral-sh/uv:debian-slim
ADD . /usr/src/app

WORKDIR /usr/src/app
RUN cd /usr/src/app/backend && uv sync
CMD ["uv run", "server.py"]
