SHELL := /bin/bash

PYTHON_PATH := $(shell which python3.11)

VENV_PATH ?= ./.venv_metrics
VENV_PYTHON := $(VENV_PATH)/bin/python


install-deps-dev:
	@echo -e "Install development dependencies\n"
	$(VENV_PYTHON) -m pip install \
		-Ur ./requirements-dev.txt

install-deps:
	@echo -e "Install dependencies for ${SOURCE}\n"
	$(VENV_PYTHON) -m pip install \
		-Ur ./requirements.txt

env-create-empty:
	@echo -e "Create virtual environment\n"
	virtualenv --python=$(PYTHON_PATH) $(VENV_PATH)

	@echo "Activate virtual environment\n"
	source $(VENV_PATH)/bin/activate

env-create: env-create-empty install-deps install-deps-dev

format:
	@echo -e "############### ISORT ###############\n"
	$(VENV_PYTHON) -m isort frontend
	@echo -e "############### BLACK ###############\n"
	$(VENV_PYTHON) -m black --skip-magic-trailing-comma frontend

check-lint:
	echo -e "############### FLAKE ###############\n" ; \
	$(VENV_PYTHON) -m flake8 frontend; \
	FLAKE8_EXIT_CODE=$$? ; \
	\
	echo -e "############### BLACK ###############\n" ; \
	$(VENV_PYTHON) -m black --check --diff frontend; \
	BLACK_EXIT_CODE=$$? ; \
	\
	echo -e "############### ISORT "###############\n ; \
	$(VENV_PYTHON) -m isort --check --diff frontend; \
	ISORT_EXIT_CODE=$$? ; \
	\
	if [ $$FLAKE8_EXIT_CODE != 0 ] || [ $$BLACK_EXIT_CODE != 0 ] || [ $$ISORT_EXIT_CODE != 0 ]; then \
		exit 1 ; \
	else \
		exit 0 ; \
	fi


run:
	$(VENV_PYTHON) -m streamlit run frontend/main.py
