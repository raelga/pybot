#!/usr/bin/env make
.PHONY: usage setup-env lint telegram \
	win-setup-venv win-telegram win-cleanup \
	container-build container-telegram container-bash container-lint container-clean

VENV_DIR := .venv
VENV_RUN := . $(VENV_DIR)/bin/activate

CONTAINER_IMAGE  := 'pybot'
CONTAINER_ENGINE ?= $(which docker)
CONTAINER_BUILD  := $(CONTAINER_ENGINE) build . -t $(CONTAINER_IMAGE)

CONTAINER_RUN_DIRS  := -v "$(CURDIR):/usr/src/pybot" -w /usr/src/pybot
CONTAINER_RUN_FLAGS := -it --rm --name pybot $(CONTAINER_RUN_DIRS) $(CONTAINER_IMAGE)
CONTAINER_RUN       := $(CONTAINER_ENGINE) run $(CONTAINER_RUN_FLAGS)

PYTHON_LINT       := pep8 --max-line-length=120 --exclude=$(VENV_DIR),dist .

PYBOT_TELEGRAM    := bin/pybot telegram

usage:            ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

setup-venv:       ## Setup virtualenv
	(test `which virtualenv` || python3 -m pip install --upgrade virtualenv)
	(test -e $(VENV_DIR) || python3 -m venv $(VENV_DIR))
	($(VENV_RUN) && python3 -m pip install --upgrade pip)
	(test ! -e requirements.txt || ($(VENV_RUN) && pip install -r requirements.txt))

clean:
	rm -rf $(VENV_DIR)

lint:             ## Run code linter to check code style
	($(VENV_RUN); $(PYTHON_LINT))

telegram:         ## Run pybot with the telegram adapter
	($(VENV_RUN); exec $(PYBOT_TELEGRAM))

win-setup-venv:	  ## Setup virtualenv in windows
	pip install virtualenv
	virtualenv .venv
	.venv\Scripts\activate
	pip install --upgrade pip
	pip install -r requirements.txt

win-telegram:     ## Run pybot with the telegram adapter in windows
	.venv\Scripts\activate
	python bin\pybot telegram

win-cleanup:      ## Remove .venv dir
	rmdir /s /q .venv

container-build:     ## Build the container image for running pybot
	$(CONTAINER_BUILD)

container-telegram:  ## Run with telegram adapter in the container container
	$(CONTAINER_RUN) $(PYBOT_TELEGRAM)

container-bash:      ## Run bash in the container container
	$(CONTAINER_RUN) bash

container-lint:      ## Run pep8 in the container container
	$(CONTAINER_RUN) $(PYTHON_LINT)

container-clean:     ## Remove the container image
	$(CONTAINER_ENGINE) rmi $(CONTAINER_IMAGE)
