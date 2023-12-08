#!/bin/bash
# creates a backup of the db

# contains getDbString
source common.sh

TIMESTAMP=$(date +%Y%m%d%H%M%S)

# get connection string then create dump
getDbString
mongodump --uri "$CONNECTION_STRING" --db "$DB_NAME" --out "$BACKUP_DIR"

if [ $? -eq 0 ]; then
  echo "Backup successful. Backup stored in: $BACKUP_DIR"
else
  echo "Backup failed."
fi