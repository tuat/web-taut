all:
	@echo "make env"
	@echo "make deps"

env:
	virtualenv-2.7 --no-site-package venv

deps:
	source venv/bin/activate && pip install -r requirements.txt

server:
	python manager.py runserver

redis:
	redis-server /usr/local/etc/redis.conf

task:
	python manager.py runtask --name=all

thumb:
	thumbor -p 8888 -c ./taut/configs/thumbor.py

clean: clean-pyc

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
