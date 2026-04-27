PYTHON     = python3
MAIN       = a_maze_ing.py
CONFIG     = config.txt
PKG_NAME   = mazegen
PKG_SRC    = mazegenerator.py

.PHONY: all install run debug lint lint-strict clean build help

all: help

## install: Install project dependencies
install:
	$(PYTHON) -m pip install flake8 mypy poetry

## run: Generate and display the maze
run:
	$(PYTHON) $(MAIN) $(CONFIG)

## debug: Run the main script in debug mode using pdb
debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

## lint: Run flake8 and mypy with standard flags
lint:
	flake8 .
	mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

## lint-strict: Run flake8 and mypy with strict flags
lint-strict:
	flake8 .
	mypy . --strict

## build: Build the mazegen pip-installable package (.whl and .tar.gz)
build:
	poetry env use $(PYTHON)
	poetry build

## clean: Remove Python caches and build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info"  -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist"        -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build"       -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

## help: Show this help message
help:
	@echo ""
	@echo "  A-Maze-ing — available targets:"
	@echo ""
	@grep -E '^## ' Makefile | sed 's/## /  make /'
	@echo ""
