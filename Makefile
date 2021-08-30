PWD=$(shell pwd)
PORT := 8080
REGION := fr-par
REGISTRY_ENDPOINT := rg.$(REGION).scw.cloud
REGISTRY_NAMESPACE := funcscwcommentsmappingrunfr6bt
IMAGE_NAME := comments_mapping
VERSION := latest
TAG := $(REGISTRY_ENDPOINT)/$(REGISTRY_NAMESPACE)/$(IMAGE_NAME):$(VERSION)

build:
	docker build -t python-mapping . --compress --tag $(TAG)

run:
	docker run -it -e PORT=$(PORT) -p $(PORT):$(PORT) --rm $(TAG)

push:
	docker push $(TAG)

deploy:
	@make build
	@make push

login:
	docker login $(REGISTRY_ENDPOINT) -u userdoesnotmatter -p $(TOKEN)

start:
	@make build
	docker run --rm -v ${PWD}/dist:/comments_mapping/dist python-mapping

test:
	pytest $(find ./**/*.py) --cov=${PWD} --cov-fail-under=90 --cov-report term-missing

lint:
	pylint ./**/*.py

dep:
	pip install pylint
	pip install -r requirements.txt

dep3:
	pip3 install pylint
	pip3 install -r requirements.txt
