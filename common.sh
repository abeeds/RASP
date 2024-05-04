#!/bin/sh
# Some common shell stuff.

echo "Importing from common.sh"

DB=RASP
USER=sa5680
CONNECT_STR="mongodb+srv://rasp.tc1w7vb.mongodb.net/"
if [ -z $DATA_DIR ]
then
    DATA_DIR="$PWD/db"
fi
BKUP_DIR=$DATA_DIR/bkup

# may cause errors if mongodb database tools are not installed
# once installed, run which mongoexport for the path
EXP=/usr/bin/mongoexport
IMP=/usr/bin/mongoimport

if [ -z $GAME_MONGO_PW ]
then
    echo "You must set GAME_MONGO_PW in your env before running this script."
    exit 1
fi

declare -a Collections=("users" "chat rooms" "messages")