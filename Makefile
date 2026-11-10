# Cyclone — build & run Makefile
# Targets: help run test build serve clean install verify live
PY := env -u PYTHONPATH .venv/bin/python
NODE := node
NPX := npx

.PHONY: help run test build serve clean install verify live lint format
help: ## Show available targets
	@echo "Targets: help run test build serve clean install verify live lint format"

run: ## Start the CYCLONE backend + terminal UI
	$(PY) main.py run

test: ## Run the Python test suite
	$(PY) -m pytest tests -q

build: ## Install the package in editable mode
	$(PY) -m pip install -e .

serve: ## Start the interactive CYCLONE terminal
	$(PY) main.py terminal

clean: ## Remove Python caches and virtualenv
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache .mypy_cache .venv

install: ## Install production requirements
	$(PY) -m pip install -r requirements.txt
	$(PY) -m pip install -r requirements-optional.txt

verify: ## Run the live smoke pipeline
	$(PY) scripts/live_smoke_pipeline.py

live: verify ## Alias for verify

lint: ## Lint Python source
	$(PY) -m ruff check app capabilities connections tasks tools main.py

format: ## Format Python source
	$(PY) -m ruff check --fix app capabilities connections tasks tools main.py

frontend: ## Install Node.js frontend dependencies
	cd apps && $(NPX) install

frontend-build: ## Build the frontend
	cd apps && $(NPX) run build
