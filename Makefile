# **************************************************************************** #
#                                   CONFIG                                     #
# **************************************************************************** #

AUTHOR              = ichbab & ykouiri
PROJECT_NAME        = A_maze_ing
PROJECT_START_DATE  = 2025

PYTHON              = python3
UV                  = uv
MAIN                = a_maze_ing.py
CONFIG              = config.txt

# COLORS
YELLOW              = \033[0;33m
CYAN                = \033[0;36m
GREEN               = \033[0;32m
RESET               = \033[0m

.PHONY: install sync run debug flake8 mypy mypy-strict lint lint-strict clean re build

install:
	@echo "$(YELLOW)╔════════════════════════════════════════════════════════════════╗$(RESET)"
	@echo "$(YELLOW)║                                                                ║$(RESET)"
	@echo "$(YELLOW)║  44  44    2222    $(GREEN)Created by $(AUTHOR)$(YELLOW)                 ║$(RESET)"
	@echo "$(YELLOW)║  44  44   22  22   Project: $(CYAN)$(PROJECT_NAME)$(YELLOW)                         ║$(RESET)"
	@echo "$(YELLOW)║  444444      22    Started in: $(CYAN)$(PROJECT_START_DATE)$(YELLOW)                            ║$(RESET)"
	@echo "$(YELLOW)║      44     22                                                 ║$(RESET)"
	@echo "$(YELLOW)║      44   222222                                               ║$(RESET)"
	@echo "$(YELLOW)║                                                                ║$(RESET)"
	@echo "$(YELLOW)╚════════════════════════════════════════════════════════════════╝$(RESET)"
	@echo
	@echo "$(CYAN)[Installation]$(RESET) Synchronizing uv..."
	@$(UV) sync

sync:
	@$(UV) sync

run:
	@$(UV) run $(PYTHON) $(MAIN) $(CONFIG)

debug:
	@$(UV) run $(PYTHON) -m pdb $(MAIN) $(CONFIG)

flake8:
	@$(UV) run flake8 --exclude .venv

mypy:
	@$(UV) run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

mypy-strict:
	@$(UV) run mypy . --strict

lint: flake8 mypy

lint-strict: flake8 mypy-strict

clean:
	@rm -rf __pycache__ .mypy_cache .pytest_cache dist build *.egg-info .venv
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm uv.lock

re: clean install

build:
	@rm -rf dist build
	@$(UV) build