.PHONY: install install-dev test lint format clean build help

# Default target
all: install-dev

# Install in development mode, with the ML extra and dev tools
install-dev:
	pip install -e ".[ml,dev]"

# Install in production mode
install:
	pip install .

# Run tests
test:
	pytest -v --cov=dexter

# Run linting
lint:
	flake8 src/dexter/ tests/

# Format code
format:
	black src/dexter/ tests/

# Clean build artifacts
clean:
	rm -rf build/ dist/ src/*.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +

# Build package
build: clean
	python -m build

# Help
help:
	@echo "Available targets:"
	@echo "  install-dev  - Install in editable mode with [ml,dev] extras"
	@echo "  install      - Install the package"
	@echo "  test         - Run tests with coverage"
	@echo "  lint         - Run flake8"
	@echo "  format       - Format code with black"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build sdist and wheel"
