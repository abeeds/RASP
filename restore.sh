#!/bin/bash

# contains getDbString
source common.sh

# gets Db connection string
getDbString
mongorestore --uri "$CONNECTION_STRING" --drop --dir "$BACKUP_DIR"

if [ $? -eq 0 ]; then
  echo "Restore successful."
else
  echo "Restore failed."
fi