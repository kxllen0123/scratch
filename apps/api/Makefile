.PHONY: help build run stop clean test lint

# Variables
IMAGE_NAME = code-sentinel-api
CONTAINER_NAME = code-sentinel-api
PORT = 8000

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build Docker image
	docker build -t $(IMAGE_NAME):latest .

run: ## Run container
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):8000 \
		-e ENVIRONMENT=dev \
		$(IMAGE_NAME):latest

run-compose: ## Run with docker-compose
	docker-compose up -d

stop: ## Stop container
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

stop-compose: ## Stop docker-compose
	docker-compose down

logs: ## Show container logs
	docker logs -f $(CONTAINER_NAME)

logs-compose: ## Show docker-compose logs
	docker-compose logs -f

shell: ## Open shell in container
	docker exec -it $(CONTAINER_NAME) /bin/bash

test: ## Run tests in container
	docker run --rm $(IMAGE_NAME):latest pytest

clean: ## Remove container and image
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME):latest || true

rebuild: clean build ## Rebuild image from scratch

dev: ## Run development server locally
	uv run python main.py

install: ## Install dependencies locally
	uv venv
	uv pip install -r requirements.txt

test-local: ## Run tests locally
	uv run pytest

lint: ## Run linting
	uv run ruff check .

format: ## Format code
	uv run ruff format .
