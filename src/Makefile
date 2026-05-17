# ==============================================================================
#  Makefile — File Handling Terminal Tool
#  Run everything from the project root. No cd required.
#
#  Usage:
#    make          → show this help menu
#    make run      → launch the full app via main.py
#    make pdf      → run pdf actions entry point
#    make copy     → run copy_files script
#    make zip      → run zip_files script
#    make rename   → run rename_files script
#    make encrypt  → run encrypt_files script
#    make organize → run organize_files script
#    make docx     → run convertDocx script
#    make folder   → run create_folder script
#    make test-pdf → run pdf test suite
#    make install  → install dependencies
#    make clean    → remove __pycache__ and .pyc files
#    make lint     → run ruff linter (if available)
#    make fmt      → run ruff formatter (if available)
# ==============================================================================

# ------------------------------------------------------------------------------
# Python interpreter — auto-detects: uv > .venv > python3
# ------------------------------------------------------------------------------
UV        := $(shell command -v uv 2>/dev/null)
VENV_PY   := .venv/bin/python

ifdef UV
  PY      := uv run python
  RUN     := uv run
else ifneq ($(wildcard $(VENV_PY)),)
  PY      := $(VENV_PY)
  RUN     := $(VENV_PY)
else
  PY      := python3
  RUN     := python3
endif

# ------------------------------------------------------------------------------
# Project layout
# ------------------------------------------------------------------------------
SRC                := src
SCRIPTS            := $(SRC)/scripts
FILES_OPS          := $(SCRIPTS)/files_operations_scripts
FOLDERS_OPS        := $(SCRIPTS)/folders_operation_scripts
PDF_DIR            := $(FILES_OPS)/pdf_actions
DOCX_DIR           := $(FILES_OPS)/docx_actions
PDF_TESTS          := $(PDF_DIR)/pdf_tests

# ------------------------------------------------------------------------------
# Entry points
# Conventions:
#   GROUP_ENTRY = the aggregator / sub-entry-point for that group
#   Add a new GROUP_ENTRY here as you build new ones
# ------------------------------------------------------------------------------
MAIN_ENTRY         := $(SRC)/main.py

# Existing sub-entry point
PDF_ENTRY          := $(PDF_DIR)/main_pdf_actions.py

# Future sub-entry points (uncomment + fill in as you build them)
# FILES_ENTRY      := $(FILES_OPS)/main_files_operations.py
# FOLDERS_ENTRY    := $(FOLDERS_OPS)/main_folders_operations.py
COPY_SCRIPT        := $(FILES_OPS)/copy_files.py

# Individual scripts (no sub-entry-point yet)
ZIP_SCRIPT         := $(FILES_OPS)/zip_files.py
RENAME_SCRIPT      := $(FILES_OPS)/rename_files.py
ENCRYPT_SCRIPT     := $(FILES_OPS)/encrypt_files.py
ORGANIZE_SCRIPT    := $(FILES_OPS)/organize_files.py
DOCX_SCRIPT        := $(DOCX_DIR)/convertDocx.py
CREATE_FOLDER      := $(FOLDERS_OPS)/create_folder.py
DELETE_FOLDER      := $(FOLDERS_OPS)/delete_folder.py
DELETE_FOLDERS     := $(FOLDERS_OPS)/delete_folders.py
PDF_TEST_SCRIPT    := $(PDF_TESTS)/test_pdf_actions.py

# PYTHONPATH so every script can resolve `src.*` imports from the root
export PYTHONPATH  := $(CURDIR)

# ------------------------------------------------------------------------------
# Default target → help menu
# ------------------------------------------------------------------------------
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo ""
	@echo "  File Handling Terminal Tool"
	@echo "  ─────────────────────────────────────────────"
	@echo "  Interpreter : $(PY)"
	@echo "  PYTHONPATH  : $(PYTHONPATH)"
	@echo ""
	@echo "  ── App ──────────────────────────────────────"
	@echo "  make run           Launch full app (main.py)"
	@echo ""
	@echo "  ── File operations ──────────────────────────"
	@echo "  make pdf           PDF actions entry point"
	@echo "  make copy          Copy files"
	@echo "  make zip           Zip files"
	@echo "  make rename        Rename files"
	@echo "  make encrypt       Encrypt files"
	@echo "  make organize      Organize files"
	@echo "  make docx          DOCX converter"
	@echo ""
	@echo "  ── Folder operations ────────────────────────"
	@echo "  make folder        Create a folder"
	@echo "  make del-folder    Delete a single folder"
	@echo "  make del-folders   Delete multiple folders"
	@echo ""
	@echo "  ── Tests ────────────────────────────────────"
	@echo "  make test-pdf      Run PDF test suite"
	@echo "  make test          Run all tests"
	@echo ""
	@echo "  ── Dev ──────────────────────────────────────"
	@echo "  make install       Install dependencies"
	@echo "  make lint          Lint with ruff"
	@echo "  make fmt           Format with ruff"
	@echo "  make clean         Remove __pycache__ / .pyc"
	@echo ""

# ------------------------------------------------------------------------------
# App entry point
# ------------------------------------------------------------------------------
.PHONY: run
run:
	$(PY) $(MAIN_ENTRY)

# ------------------------------------------------------------------------------
# File operation targets
#
# Pattern: if a group has a sub-entry-point, point to it.
#          If not yet, point directly to the script.
#          When you create main_files_operations.py, swap COPY_SCRIPT
#          for FILES_ENTRY and remove the individual copy/zip/rename/...
#          targets (or keep them as aliases).
# ------------------------------------------------------------------------------
.PHONY: pdf
pdf:
	$(PY) $(PDF_ENTRY)

.PHONY: copy
copy:
	$(PY) $(COPY_SCRIPT)

.PHONY: zip
zip:
	$(PY) $(ZIP_SCRIPT)

.PHONY: rename
rename:
	$(PY) $(RENAME_SCRIPT)

.PHONY: encrypt
encrypt:
	$(PY) $(ENCRYPT_SCRIPT)

.PHONY: organize
organize:
	$(PY) $(ORGANIZE_SCRIPT)

.PHONY: docx
docx:
	$(PY) $(DOCX_SCRIPT)

# ------------------------------------------------------------------------------
# Folder operation targets
# ------------------------------------------------------------------------------
.PHONY: folder
folder:
	$(PY) $(CREATE_FOLDER)

.PHONY: del-folder
del-folder:
	$(PY) $(DELETE_FOLDER)

.PHONY: del-folders
del-folders:
	$(PY) $(DELETE_FOLDERS)

# ------------------------------------------------------------------------------
# Test targets
# ------------------------------------------------------------------------------
.PHONY: test-pdf
test-pdf:
	$(PY) -m pytest $(PDF_TESTS) -v

.PHONY: test
test:
	$(PY) -m pytest $(SCRIPTS) -v

# ------------------------------------------------------------------------------
# Dev / maintenance targets
# ------------------------------------------------------------------------------
.PHONY: install
install:
ifdef UV
	uv sync
else
	pip install -e .
endif

.PHONY: lint
lint:
	$(RUN) ruff check $(SRC)

.PHONY: fmt
fmt:
	$(RUN) ruff format $(SRC)

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "  cleaned."

# ==============================================================================
# HOW TO ADD A NEW SCRIPT GROUP (checklist)
# ==============================================================================
# 1. Create your scripts under src/scripts/<new_group>/
# 2. Add a sub-entry-point, e.g. src/scripts/<new_group>/main_<new_group>.py
# 3. Declare the path here:
#      NEW_ENTRY := $(SCRIPTS)/<new_group>/main_<new_group>.py
# 4. Add a .PHONY target:
#      .PHONY: <new_group>
#      <new_group>:
#          $(PY) $(NEW_ENTRY)
# 5. Add a line to the help menu.
# 6. Import the entry point in src/main.py.
# That's it — no other file needs to change.
# ==============================================================================
