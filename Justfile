# Justfile for vault-search-replace

# Default task: list available recipes
default:
    @just --list

# Run setup, test, and package
all: setup test package

# Setup the development environment
setup:
    @echo "Setting up the environment..."
    uv sync

# Run tests
test:
    @echo "Running tests..."
    PYTHONPATH=src uv run pytest tests/test_vault_search_replace.py

# Clean up temporary files
clean:
    @echo "Cleaning up..."
    rm -rf __pycache__ *.pyc .pytest_cache
    find . -name "__pycache__" -exec rm -rf {} +

# Build the package
package:
    @echo "Building the package..."
    uv build
