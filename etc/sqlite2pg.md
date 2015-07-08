# Convert sqlite to postgres

## Read env and enter to script directory

    source venv/bin/activate
    cd etc/

## Drop the exists database if you want to test it

    dropdb 'web_taut'

## Create the database again

    createdb 'web_taut'

## Migrate the base database structure

    alembic upgrade head

## Install deps for pgloader

    brew install freetds

## Ran the pgloader to convert sqlite

    pgloader sqlite2pg.load
