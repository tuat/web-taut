all:
	@echo "make env"
	@echo "make deps"

env:
	virtualenv-2.7 --no-site-package venv

deps:
	source venv/bin/activate && pip install -r requirements.txt

server:
	python manager.py runserver
