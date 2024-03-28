import pytest

import db.db_connect as dbc

TEST_DB = dbc.USER_DB
TEST_COLLECT = 'test_collect'
TEST_COLLECT_MANY = 'test_collect_many'
# can be used for field and value:
TEST_NAME = 'test'
UPDATE = 'Update'
SAMPLE_DOCS = [
    {TEST_NAME: TEST_NAME},
    {TEST_NAME: TEST_NAME},
    {TEST_NAME: TEST_NAME}
]


@pytest.fixture(scope='function')
def temp_rec():
    dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT].insert_one({TEST_NAME: TEST_NAME})
    # yield to our test function
    yield
    dbc.client[TEST_DB][TEST_COLLECT].delete_one({TEST_NAME: TEST_NAME})


@pytest.fixture(scope='function')
def temp_collection():
    dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT_MANY].insert_many(SAMPLE_DOCS)
    yield dbc.client[TEST_DB][TEST_COLLECT_MANY]
    dbc.client[TEST_DB].drop_collection(TEST_COLLECT_MANY)


def test_fetch_one(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})
    assert ret is not None


def test_fetch_one_not_there(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: 'not a field value in db!'})
    assert ret is None


def test_update_doc(temp_rec):
    dbc.update_doc(TEST_COLLECT, {TEST_NAME: TEST_NAME}, {TEST_NAME: UPDATE})
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: UPDATE})
    assert ret is not None


def test_del_all_in_collection(temp_collection):
    assert temp_collection.count_documents({}) == 3
    dbc.del_all_in_collection(TEST_COLLECT_MANY)
    assert temp_collection.count_documents({}) == 0
