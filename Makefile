ifeq (, $(ENV))
	ENV := development
	env := development
else ifeq (test, $(ENV))
	env := testing
else
	env := $(ENV)
endif

app := aarau

# -- installation

setup:
	pip install -e '.[${env}]' -c constraints.txt
.PHONY: setup

setup-force:
	pip install --upgrade --force-reinstall -e '.[${env}]' -c constraints.txt
.PHONY: setup-force

update:
	pip install --upgrade -e '.[${env}]' -c constraints.txt
.PHONY: update

# -- database

db-init:
	ENV=$(ENV) ${app}_manage 'config/${env}.ini#${app}' db init
.PHONY: db-init

db-migrate:
	ENV=$(ENV) ${app}_manage 'config/${env}.ini#${app}' db migrate
.PHONY: db-migrate

db-rollback:
	ENV=$(ENV) ${app}_manage 'config/${env}.ini#${app}' db rollback
.PHONY: db-rollback

db-seed:
	ENV=$(ENV) ${app}_manage 'config/${env}.ini#${app}' db seed
.PHONY: db-seed

db-drop:
	ENV=$(ENV) ${app}_manage 'config/${env}.ini#${app}' db drop
.PHONY: db-drop

db-reset:
	${app}_manage 'config/${env}.ini#${app}' db drop
	${app}_manage 'config/${env}.ini#${app}' db init
	${app}_manage 'config/${env}.ini#${app}' db migrate
ifneq (test, $(ENV))
	${app}_manage 'config/${env}.ini#${app}' db seed
endif
.PHONY: db-reset

# -- application

# server (development)
serve:
	./bin/serve --env development --config config/development.ini --reload
.PHONY: serve

# worker (development)
worker:
	ENV=$(ENV) ${app}_worker 'config/${env}.ini#${app}'
.PHONY: worker

# both, use `bin/start` via honcho. see Procfile
start:
	honcho start
.PHONY: start

# -- testing

test:
	ENV=test py.test -c 'config/testing.ini' -s -q
.PHONY: test

coverage:
	ENV=test py.test -c 'config/testing.ini' -s -q --cov=${app} --cov-report \
	 term-missing:skip-covered
.PHONY: coverage

# -- translation

catalog-extract:
	./bin/linguine extract message
	./bin/linguine extract form
.PHONY: catalog-extract

catalog-compile:
	./bin/linguine compile message en
	./bin/linguine compile form en
.PHONY: catalog-compile

catalog-update:
	./bin/linguine update message en
	./bin/linguine update form en
.PHONY: catalog-update

catalog: | catalog-compile
.PHONY: catalog

# -- utility

check:
	flake8
.PHONY: check

lint:
	pylint test aarau
.PHONY: lint

vet: | check lint
.PHONY: vet

build:
ifeq (, $(shell which gulp 2>/dev/null))
	$(info gulp command not found. run `npm install -g gulp-cli`)
	$(info )
else
	gulp
endif
.PHONY: build

clean:
	find . ! -readable -prune -o -print \
	 ! -path "./.git/*" ! -path "./node_modules/*" ! -path "./venv*" \
	 ! -path "./doc/*" ! -path "./locale/*" ! -path "./tmp/*" \
	 ! -path "./lib/*" | \
	 grep -E "(__pycache__|\.egg-info|\.pyc|\.pyo)" | xargs rm -rf
ifeq (, $(shell which gulp 2>/dev/null))
	$(info gulp command not found. run `npm install -g gulp-cli`)
	$(info )
else
	gulp clean
endif
.PHONY: clean


.DEFAULT_GOAL = coverage
default: coverage
