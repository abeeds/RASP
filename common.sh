#!/bin/bash
# common code for bkup.sh and restore.sh

BACKUP_DIR="$PWD/backups"
DB_NAME="RASP"

# sets connection string based on CLOUD_MONGO var
# set to cloud with export CLOUD_MONGO=1
getDbString() {
    if [ "$CLOUD_MONGO" = "1" ]; then
        CONNECTION_STRING="mongodb+srv://sa5680:$GAME_MONGO_PW@rasp.tc1w7vb.mongodb.net/?retryWrites=true&w=majority"
    else
        CONNECTION_STRING="mongodb://localhost:27017"
    fi
}