# Web-Taut

Sync the tweets in specified twitter lists and output to the custom API interface

# Installation

## Clone the repo into

    git clone https://github.com/zeuxisoo/web-taut.git taut

## Enter app directory

    cd taut

## Create config file

    mv taut/configs/default.py.sample taut/configs/default.py
    mv taut/configs/thumbor.py.sample taut/configs/thumbor.py

## Move program file

    cp thumbor/loaders/twimg.py venv/lib/python2.7/site-packages/thumbor/loaders/twimg.py

## Edit config file

vim taut/configs/default.py

    SECRET_KEY=""
    BROKER_URL=""
    TWITTER={}
    THUMBOR_BASE_URL=""
    THUMBOR_SECURITY_KEY="same as SECURITY_KEY"

vim taut/configs/thumbor.py

    SECURITY_KEY="same as THUMBOR_SECURITY_KEY"

# Migrate Database

    source venv/bin/activate
    alembic upgrade head

# Start task server and run scheudled tasks

Run from the `manager.py` commands

    make task

Run from the celery cli bin

    make task-celery-bin

# Problem

Fix curl-config not found

    apt-get install libcurl4-gnutls-dev

Fix decoder jpeg not available

    apt-get install libjpeg-dev
    pip install -I pillow

Fix assets tag not found

    apt-get install openjdk-7-jre
