.PHONY: help install install-dev test lint format clean run docker-build docker-run

# Default target
help:
	@echo "YouTube Script Agent - Available Commands"
	@echo "=========================================="
	@echo "install          Install production dependencies"
	@echo "install-dev      Install development dependencies"
	@echo "test             Run all tests with coverage"
	@echo "test-unit        Run unit tests only"
	@echo "test-integration Run integration tests only"
	@echo "lint             Run linting checks"
	@echo "format           Auto-format code"
	@echo "type-check       Run type checking with mypy"
	@echo "clean            Remove build artifacts"
	@echo "run              Run the agent (requires args)"
	@echo "docker-build     Build Docker image"
	@echo "docker-run       Run in Docker container"
	@echo "setup-hooks      Install pre-commit hooks"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev,docs]"
	pre-commit install

# Testing
test:
	pytest tests/ -v --cov=src/youtube_script_agent --cov-report=html --cov-report=term

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-watch:
	pytest-watch tests/ -v

# Code quality
lint:
	flake8 src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/youtube_script_agent

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Running
run:
	python -m youtube_script_agent $(ARGS)

# Example runs
run-nfl:
	python -m youtube_script_agent --topic nfl

run-multiple:
	python -m youtube_script_agent --run-now --topics nfl nba

run-automate:
	python -m youtube_script_agent --automate --topics nfl nba

# Docker
docker-build:
	docker build -t youtube-script-agent:latest .

docker-run:
	docker-compose up

docker-stop:
	docker-compose down

# Pre-commit hooks
setup-hooks:
	pre-commit install
	pre-commit autoupdate

# Documentation
docs:
	mkdocs serve

docs-build:
	mkdocs build

# Release
release-patch:
	bumpversion patch

release-minor:
	bumpversion minor

release-major:
	bumpversion major

# CI/CD
ci: lint type-check test