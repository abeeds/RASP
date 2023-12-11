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

#!/bin/sh
# Script to backup production database to JSON files.

. ./common.sh

for collection in "${Collections[@]}"; do
    echo "Restoring $collection"
    $IMP --db=$DB --collection $collection --drop --file $BKUP_DIR/$collection.json
done