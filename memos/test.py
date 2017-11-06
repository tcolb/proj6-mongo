import nose
import random
from pymongo import MongoClient

import config
CONFIG = config.configuration()


MONGO_CLIENT_URL = "mongodb://{}:{}@{}:{}/{}".format(
    CONFIG.DB_USER,
    CONFIG.DB_USER_PW,
    CONFIG.DB_HOST,
    CONFIG.DB_PORT,
    CONFIG.DB)


try:
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, CONFIG.DB)
    collection = db.memos
except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)


def test_add():
    document_count = collection.count()
    collection.insert({"type": "test_memo", "date": "testing date", "text": "testing text"})

    print("Testing add: had {} documents, now have {}".format(document_count, collection.count()))
    assert collection.count() == (document_count + 1)

def test_delete():
    document_count = collection.count()
    documents = collection.find({"type": "test_memo"})
    collection.delete_one(documents[random.randrange(documents.count())])

    print("Testing delete: had {} documents, now have {}".format(document_count, collection.count()))
    assert collection.count() == (document_count - 1)

if __name__ == "__main__":
    test_add()
    test_add()
    test_add()

    test_delete()
    test_delete()
    test_delete()
