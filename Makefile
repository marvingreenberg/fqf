SERVICE_NAME   := fqf2026
GCP_PROJECT    ?= $(shell gcloud config get-value project 2>/dev/null)
GCP_REGION     ?= us-central1
GCP_REPOSITORY := container-images
GCP_IMAGE      := $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT)/$(GCP_REPOSITORY)/$(SERVICE_NAME)

.PHONY: help setup check-prereqs setup-api setup-ui build build-api build-ui test test-api test-ui \
        lint lint-api lint-ui format format-api format-ui dev dev-firestore clean \
        build-image docker-run deploy e2e

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Setup ──────────────────────────────────────────────────────────────
setup: check-prereqs setup-api setup-ui ## Install all dependencies

check-prereqs: ## Check development prerequisites
	@./scripts/check_prerequisites.sh

setup-api: ## Install Python dependencies
	uv venv --clear
	uv sync --all-extras

setup-ui: ## Install frontend dependencies
	pnpm --dir ui install

# ── Build ──────────────────────────────────────────────────────────────
build: build-api build-ui ## Build all packages

build-api: ## Build Python package
	uv build

build-ui: ## Build SvelteKit frontend
	pnpm --dir ui build

# ── Test ───────────────────────────────────────────────────────────────
test: test-api test-ui ## Run all tests

test-api: ## Run Python tests with coverage
	uv run pytest

test-ui: ## Run frontend unit tests
	pnpm --dir ui test

# ── Lint ───────────────────────────────────────────────────────────────
lint: lint-api lint-ui ## Run all linters

lint-api: ## Lint Python code
	uv run black --check src tests
	uv run isort --check src tests
	uv run mypy src

lint-ui: ## Lint frontend code
	pnpm --dir ui lint

# ── Format ─────────────────────────────────────────────────────────────
format: format-api format-ui ## Format all code

format-api: ## Format Python code
	uv run black src tests
	uv run isort src tests

format-ui: ## Format frontend code
	pnpm --dir ui format

# ── Dev ────────────────────────────────────────────────────────────────
# Uses in-memory storage by default — no Firestore needed for local dev.
# Use `make dev-firestore` to run against the local Firestore emulator instead.
dev: ## Start API + UI dev servers with hot reload, open browser
	@trap 'kill -9 0 2>/dev/null; wait 2>/dev/null' EXIT; \
	  uv run uvicorn fqf.api.app:create_app --factory --reload --port 8000 & \
	  sleep 1; kill -0 $$! 2>/dev/null || { echo "ERROR: API server failed to start"; exit 1; }; \
	  pnpm --dir ui dev & \
	  for i in 1 2 3 4 5 6 7 8 9 10; do curl -s http://localhost:5173 >/dev/null 2>&1 && break; sleep 1; done; \
	  open http://localhost:5173; \
	  wait

dev-firestore: ## Start dev with Firestore emulator
	@echo "Starting Firestore emulator..."
	@FIRESTORE_EMULATOR_HOST=localhost:8081 gcloud beta emulators firestore start --host-port=localhost:8081 &
	@sleep 3
	@trap 'kill 0 2>/dev/null; wait 2>/dev/null' EXIT; \
	  FIRESTORE_EMULATOR_HOST=localhost:8081 uv run uvicorn fqf.api.app:create_app --factory --reload --port 8000 & \
	  sleep 1; kill -0 $$! 2>/dev/null || { echo "ERROR: API server failed to start"; exit 1; }; \
	  pnpm --dir ui dev & \
	  for i in 1 2 3 4 5 6 7 8 9 10; do curl -s http://localhost:5173 >/dev/null 2>&1 && break; sleep 1; done; \
	  open http://localhost:5173; \
	  wait

# ── Docker ─────────────────────────────────────────────────────────────
build-image: ## Build Docker image locally
	docker buildx build \
	  -t $(SERVICE_NAME):latest \
	  -t $(GCP_IMAGE):latest \
	  .

docker-run: build-image ## Build and run locally
	docker run --rm -p 8000:8000 \
	  -e GCP_PROJECT=$(GCP_PROJECT) \
	  $(SERVICE_NAME):latest

# ── Deploy ─────────────────────────────────────────────────────────────
deploy: build-image ## Build, push, and deploy to Cloud Run
	docker push $(GCP_IMAGE):latest
	gcloud run deploy $(SERVICE_NAME) \
	  --image=$(GCP_IMAGE):latest \
	  --region=$(GCP_REGION) \
	  --project=$(GCP_PROJECT) \
	  --port=8000 \
	  --memory=512Mi \
	  --cpu=1 \
	  --min-instances=0 \
	  --max-instances=3 \
	  --service-account=fqf-SA@$(GCP_PROJECT).iam.gserviceaccount.com \
	  --allow-unauthenticated

# ── E2E ────────────────────────────────────────────────────────────────
e2e: ## Run E2E tests
	pnpm --dir ui exec playwright test

# ── Clean ──────────────────────────────────────────────────────────────
clean: ## Remove build artifacts
	rm -rf dist/ build/ *.egg-info .mypy_cache .pytest_cache htmlcov .coverage
	rm -rf ui/build ui/.svelte-kit
