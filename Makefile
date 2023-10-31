SHELL := /bin/bash

PYTHON_PATH := $(shell which python3.11)

VENV_PATH ?= ./.venv_metrics
VENV_PYTHON := $(VENV_PATH)/bin/python

SOURCES := frontend backend migrations config

DEV_ENV_FILE := .env-dev
DEV_COMPOSE_FILE := docker-compose.dev.yml

ALEMBIC_CONFIG := alembic.ini

NAMESPACE := metrics

############### INSTALL ###############

install-deps-dev:
	@echo -e "Install development dependencies\n"
	$(VENV_PYTHON) -m pip install \
		-Ur ./requirements-dev.txt

install-deps:
	@echo -e "Install dependencies for frontend\n"
	$(VENV_PYTHON) -m pip install \
		-Ur ./requirements.txt

	@echo -e "Install dependencies for backend\n"
	$(VENV_PYTHON) -m pip install \
		-Ur ./backend/requirements.txt

############### ENV ###############

env-create-empty:
	@echo -e "Create virtual environment\n"
	virtualenv --python=$(PYTHON_PATH) $(VENV_PATH)

	@echo "Activate virtual environment\n"
	source $(VENV_PATH)/bin/activate

env-create: env-create-empty install-deps install-deps-dev

############### FORMAT AND LINT ###############

format:
	@echo -e "############### ISORT ###############\n"
	$(VENV_PYTHON) -m isort ${SOURCES}
	@echo -e "############### BLACK ###############\n"
	$(VENV_PYTHON) -m black --skip-magic-trailing-comma ${SOURCES}

check-lint:
	echo -e "############### FLAKE ###############\n" ; \
	$(VENV_PYTHON) -m flake8 ${SOURCES}; \
	FLAKE8_EXIT_CODE=$$? ; \
	\
	echo -e "############### BLACK ###############\n" ; \
	$(VENV_PYTHON) -m black --check --diff ${SOURCES}; \
	BLACK_EXIT_CODE=$$? ; \
	\
	echo -e "############### ISORT "###############\n ; \
	$(VENV_PYTHON) -m isort --check --diff ${SOURCES}; \
	ISORT_EXIT_CODE=$$? ; \
	\
	if [ $$FLAKE8_EXIT_CODE != 0 ] || [ $$BLACK_EXIT_CODE != 0 ] || [ $$ISORT_EXIT_CODE != 0 ]; then \
		exit 1 ; \
	else \
		exit 0 ; \
	fi

############### DEBUG #################

run-frontend:
	$(VENV_PYTHON) -m streamlit run frontend/main.py

run-backend:
	$(VENV_PYTHON) -m backend.main

dev-compose-up:
	docker-compose --env-file $(DEV_ENV_FILE) -f $(DEV_COMPOSE_FILE) up -d --build

dev-compose-down:
	docker-compose --env-file $(DEV_ENV_FILE) -f $(DEV_COMPOSE_FILE) down

dev-compose-push: dev-compose-up
	docker-compose --env-file $(DEV_ENV_FILE) -f $(DEV_COMPOSE_FILE) push

helm-install:
	helm install -f helm/values.yaml metrics helm --namespace ${NAMESPACE}

helm-uninstall:
	helm uninstall metrics --namespace ${NAMESPACE}

helm-upgrade:
	helm upgrade -f helm/values.yaml metrics helm --namespace ${NAMESPACE}

############### DATABASE ###############

include ${DEV_ENV_FILE}

db-migrate:
	POSTGRES_NAME=${POSTGRES_NAME} \
	POSTGRES_HOST=${POSTGRES_HOST} \
	POSTGRES_USER=${POSTGRES_USER} \
	POSTGRES_PORT=${POSTGRES_PORT} \
	POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
	alembic -c ${ALEMBIC_CONFIG} upgrade head

db-downgrade:
	POSTGRES_NAME=${POSTGRES_NAME} \
	POSTGRES_HOST=${POSTGRES_HOST} \
	POSTGRES_USER=${POSTGRES_USER} \
	POSTGRES_PORT=${POSTGRES_PORT} \
	POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
	alembic -c ${ALEMBIC_CONFIG} downgrade -1

db-revision:
	POSTGRES_NAME=${POSTGRES_NAME} \
	POSTGRES_HOST=${POSTGRES_HOST} \
	POSTGRES_USER=${POSTGRES_USER} \
	POSTGRES_PORT=${POSTGRES_PORT} \
	POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
	alembic -c ${ALEMBIC_CONFIG} revision --autogenerate -m ${NAME}