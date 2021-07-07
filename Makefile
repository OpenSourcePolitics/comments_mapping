PWD=$(shell pwd)

build:
	docker build -t python-mapping . --compress

start:
	@make build
	docker run --rm -v ${PWD}/dist:/comments_mapping/dist python-mapping

lint:
	pylint ./**/*.py

dep:
	pip install pylint
	pip install -r requirements.txt

dep3:
	pip3 install pylint
	pip3 install -r requirements.txt
