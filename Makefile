.PHONY: install install-dev test lint format clean build docs

# Default target
all: install-dev

# Install in development mode
install-dev:
	python install_dev.py

# Install in production mode
install:
	pip install -e .

# Run tests
test:
	pytest tests/ -v --cov=src/dexter

# Run linting
lint:
	flake8 src/dexter/ tests/
	mypy src/dexter/

# Format code
format:
	black src/dexter/ tests/
	isort src/dexter/ tests/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build package
build: clean
	python -m build

# Build documentation
docs:
	cd docs && make html

# Run all checks
check: lint test

# Install pre-commit hooks
install-hooks:
	pre-commit install

# Update dependencies
update-deps:
	pip install --upgrade -r requirements.txt

# Show package info
info:
	python -c "import dexter; print(f'Dexter version: {dexter.__version__}')"

# Help
help:
	@echo "Available targets:"
	@echo "  install-dev  - Install in development mode"
	@echo "  install      - Install in production mode"
	@echo "  test         - Run tests with coverage"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black and isort"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build package"
	@echo "  docs         - Build documentation"
	@echo "  check        - Run linting and tests"
	@echo "  info         - Show package information"
