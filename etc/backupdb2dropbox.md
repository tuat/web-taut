# Backup database to dropbox

## Copy script and edit configuation

    cp backupdb2dropbox.sh.sample backupdb2dropbox.sh

    vim backupdb2dropbox.sh

        POSTGRES_USER="POSTGRES_USER"
        POSTGRES_PASS="POSTGRES_PASS"
        POSTGRES_DB="POSTGRES_DB"

        DROPBOX_PATH="/Backup/Domain/example.com"

## Setup dropbox uploader

    curl "https://raw.githubusercontent.com/andreafabrizi/Dropbox-Uploader/master/dropbox_uploader.sh" -o dropbox_uploader.sh
    bash dropbox_uploader.sh

Steps

    1. Dropbox API app
    2. Files and datastores
    3. Yes My app only needs access to files it creates
    4. Enter "app key" and "app secret"
    5. Enter "a" for App folder Permission
    6. Open given url to get access token
    7. Completed

## Test script

    bash backupdb2dropbox.sh

## Add crontab

    crontab -e -u user

    00 3 * * * cd /path/to/app/etc && bash backupdb2dropbox.sh
