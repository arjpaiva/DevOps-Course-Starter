import json
import mongomock

import pytest
import app
import requests
from dotenv import load_dotenv, find_dotenv


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()
    #
    #     # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


class MockResponse(object):
    def __init__(self, status_code, body_content):
        self._status_code = status_code
        self._body_content = body_content

    def json(self):
        cards_with_json = json.loads(json.dumps(self._body_content))
        cards = []
        for card_json in cards_with_json:
            cards.append(json.loads(card_json))
        return cards

    @property
    def status_code(self):
        return self._status_code


@mongomock.patch(servers=('mongodb+srv://ritadevops:ritadevops@cluster0.qs8y5.mongodb.net/todo_db',))
def test_index_page(monkeypatch, client):
    collection = mongomock.MongoClient().db.collection
    obj1 = {'_id': '1', 'title': 'banana', 'list_id': '123', 'last_modified': datetime.now(tz=timezone.utc)}
    collection.insert(obj1)

    monkeypatch.setattr(requests, 'get', fake_get)
    response = client.get('/')
    response_html = response.data

    assert 'apples' in response_html.decode("utf-8")
    assert 'TODO' in response_html.decode("utf-8")


def test_add_item_when_item_already_exists_should_redirect(monkeypatch, client):
    def fake_get(*args, **kwargs):
        cards = [generate_one_card_json('apples')]
        return MockResponse(200, cards)

    title = 'apples'
    monkeypatch.setattr(requests, 'get', fake_get)
    response = client.post('/', data=dict(title=title))
    response_html = response.data

    assert f'A card with the title {title} already exists.' in response_html.decode("utf-8")


def test_add_item_when_item_is_empty_should_throw_exception(monkeypatch, client):

    response = client.post('/', data=dict(title=''))
    response_html = response.data

    assert 'Title can not be empty' in response_html.decode("utf-8")


def test_add_item_does_not_exists_should_create_new(monkeypatch, client):
    def fake_get(*args, **kwargs):
        cards = [generate_one_card_json('apples')]
        return MockResponse(200, cards)

    title = 'banana'
    monkeypatch.setattr(requests, 'get', fake_get)
    response = client.post('/', data=dict(title=title))
    response_html = response.data

    assert 'Redirecting...' in response_html.decode("utf-8")


def generate_one_card_json(title):
    card = '''
    {"_id": "5f6f106d896a36281f955273",
    "title": "buy banana",
    "list_id": "60d089a7b247209949ab303a"
    "last_modified": "1624287133767"
    '''
    return card.replace('<title_name>', title).replace('\n', '').replace(' ', '')



# {"_id":{"$oid":"60d0a79d3cff04357666f3ee"},"title":"banana","list_id":"60d089a7b247209949ab303a","last_modified":{"$date":{"$numberLong":"1624287133767"}}}