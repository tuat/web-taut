all:
	@echo "make env"
	@echo "make deps"

env:
	virtualenv-2.7 --no-site-package venv

deps:
	source venv/bin/activate && pip install -r requirements.txt

server:
	python manager.py runserver

database:
	alembic upgrade head

redis:
	redis-server /usr/local/etc/redis.conf

task:
	python manager.py runtask --name=all

task-celery-bin:
	celery worker -E -l INFO -A manager.celery -B

event-celery-bin:
	celery events -A manager.celery

thumb:
	thumbor -p 8888 -c ./taut/configs/thumbor.py

clean: clean-pyc

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
