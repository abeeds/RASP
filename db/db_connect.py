import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

USER_DB = "RASP"

client = None

MONGO_ID = '_id'

LOCAL_HOST = "localhost"
LOCAL_PORT = 27017


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            password = os.environ.get("GAME_MONGO_PW")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://sa5680:{password}'
                                    + '@rasp.tc1w7vb.mongodb.net/'
                                    + '?retryWrites=true&w=majority')
            # PA recommends these settings:
            # + 'connectTimeoutMS=30000&'
            # + 'socketTimeoutMS=None
            # + '&connect=false'
            # + 'maxPoolsize=1')
            # but they don't seem necessary
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient(LOCAL_HOST, LOCAL_PORT)
            if client is not None:
                print("Connection successful")


def insert_one(collection, doc, db=USER_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


def fetch_one(collection, filt, db=USER_DB):
    """
    Find with a filter and return on the first doc found.
    """
    for doc in client[db][collection].find(filt):
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
        return doc


def fetch_many(collection, filt, db=USER_DB, limit="MAX"):
    """
    Find with a filter and return all.
    """
    ret = []
    if (limit == "MAX"):
        docs = client[db][collection].find(filt)
    else:
        docs = client[db][collection].find(filt).limit(limit)

    for doc in docs:
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
        ret.append(doc)
    return ret


def del_one(collection, filt, db=USER_DB):
    """
    Find with a filter and return on the first doc found.
    """
    client[db][collection].delete_one(filt)


def del_all_in_collection(collection, db=USER_DB):
    """
    Find with a filter and return on the first doc found.
    """
    client[db][collection].delete_many({})


def del_many(collection, filt, db=USER_DB):
    client[db][collection].delete_many(filt)


def update_doc(collection, filters, update_dict, db=USER_DB):
    return client[db][collection].update_one(filters, {'$set': update_dict})


def fetch_all(collection, db=USER_DB):
    ret = []
    for doc in client[db][collection].find():
        ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=USER_DB):
    ret = {}
    for doc in client[db][collection].find():
        del doc[MONGO_ID]
        ret[doc[key]] = doc
    return ret


def update_one(collection, filt, doc, db=USER_DB):
    return client[db][collection].update_one(filt, doc)
