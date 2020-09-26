import json

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


def test_index_page(monkeypatch, client):
    def fake_get(*args, **kwargs):
        cards = [generate_one_card_json('apples')]
        return MockResponse(200, cards)

    monkeypatch.setattr(requests, 'get', fake_get)
    response = client.get('/')
    response_html = response.data

    assert 'apples' in response_html.decode("utf-8")
    assert 'TODO' in response_html.decode("utf-8")


def test_add_item_when_item_already_exists_should_redirect(monkeypatch, client):
    def fake_get(*args, **kwargs):
        cards = [generate_one_card_json('apples')]
        return MockResponse(200, json.dumps(cards))

    title = 'apples'
    monkeypatch.setattr(requests, 'get', fake_get)
    response = client.post('/', data=dict(title=title))
    response_html = response.data

    assert f'A card with the title {title} already exists.' in response_html.decode("utf-8")


def test_add_item_when_item_is_empty_should_redirect(monkeypatch, client):
    def fake_get(*args, **kwargs):
        cards = [generate_one_card_json('apples')]
        return MockResponse(200, json.dumps(cards))

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
    {"id": "5f6f106d896a36281f955273",
    "checkItemStates": [],
    "closed": false,
    "dateLastActivity": "2020-09-26T09:57:01.995Z",
    "desc": "",
    "descData": {
        "emoji": {}
    },
    "dueReminder": null,
    "idBoard": "5f510df850a84370bf556755",
    "idList": "5f510df87d0a156d2b3fd79c",
    "idMembersVoted": [],
    "idShort": 25,
    "idAttachmentCover": null,
    "idLabels": [],
    "manualCoverAttachment": false,
    "name": "<title_name>",
    "pos": 81920,
    "shortLink": "SOchELNj",
    "isTemplate": false,
    "dueComplete": false,
    "due": null,
    "email": null,
    "labels": [],
    "shortUrl": "https://trello.com/c/SOchELNj",
    "start": null,
    "url": "https://trello.com/c/SOchELNj/25-apples",
    "cover": {
        "idAttachment": null,
        "color": null,
        "idUploadedBackground": null,
        "size": "normal",
        "brightness": "light"
    },
    "idMembers": [],
    "badges": {
        "attachmentsByType": {
            "trello": {
                "board": 0,
                "card": 0
            }
        },
        "location": false,
        "votes": 0,
        "viewingMemberVoted": false,
        "subscribed": false,
        "fogbugz": "",
        "checkItems": 0,
        "checkItemsChecked": 0,
        "checkItemsEarliestDue": null,
        "comments": 0,
        "attachments": 0,
        "description": false,
        "due": null,
        "dueComplete": false,
        "start": null
    },
    "subscribed": false,
    "idChecklists": [],
    "attachments": [],
    "stickers": [],
    "limits": {}}
    '''
    return card.replace('<title_name>', title).replace('\n', '').replace(' ', '')



