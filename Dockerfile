# Stage 1: Build frontend
FROM node:22-slim AS frontend
WORKDIR /app/ui
RUN corepack enable && corepack prepare pnpm@latest --activate
COPY ui/package.json ui/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY ui/ ./
RUN pnpm build

# Stage 2: Build backend + bundle
FROM python:3.11-slim AS backend
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY --from=frontend /app/ui/build ./src/fqf/static/
# setuptools-scm needs a version when no .git is present
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0
RUN uv pip install --system .
EXPOSE 8000
CMD ["uvicorn", "fqf.api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
