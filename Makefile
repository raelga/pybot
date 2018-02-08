VENV_DIR      := .venv
VENV_RUN      := . $(VENV_DIR)/bin/activate

IMAGE_NAME    := 'pybot'

DOCKER_BUILD	:= docker build . -t $(IMAGE_NAME)

DOCKER_RUN_DIRS	  := -v "$(CURDIR):/usr/src/pybot" -w /usr/src/pybot
DOCKER_RUN_FLAGS  := -it --rm --name pybot $(DOCKER_RUN_DIRS) $(IMAGE_NAME)
DOCKER_RUN 		    := docker run $(DOCKER_RUN_FLAGS)

PYTHON_LINT       := pep8 --max-line-length=120 --exclude=$(VENV_DIR),dist .

PYBOT_TELEGRAM    := bin/pybot telegram

usage:            ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

setup-venv:       ## Setup virtualenv
	(test `which virtualenv` || pip install virtualenv || sudo pip install virtualenv)
	(test -e $(VENV_DIR) || virtualenv -p python3 $(VENV_DIR))
	($(VENV_RUN) && pip install --upgrade pip)
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

docker-build:     ## Build the docker image for running pybot
	$(DOCKER_BUILD)

docker-telegram:  ## Run with telegram adapter in the docker container
	$(DOCKER_RUN) $(PYBOT_TELEGRAM)

docker-bash:      ## Run bash in the docker container
	$(DOCKER_RUN) bash

docker-lint:      ## Run pep8 in the docker container
	$(DOCKER_RUN) $(PYTHON_LINT)

docker-clean:     ## Remove the docker image
	docker rmi $(IMAGE_NAME)
