import json

import pytest
import app
from dotenv import load_dotenv, find_dotenv
import requests


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

    # @pytest.fixture
    # def mock_get_requests(requests_mock):
    #     requests_mock.get('http://test.com', text='data')
    #     print('bananas')


class MockResponse(object):

    # Faking the requests.Response.json() method
    @staticmethod
    def json():
        # return json.loads(self.text)
        cards = '''
    def __init__(self):
        [{"id": "5f6f106d896a36281f955273",
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
          "name": "apples",
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
          "limits": {}}]
        '''.replace('\n', '').replace(' ', '')

        return json.loads(cards)

    @staticmethod
    def status_code():
        return 200


def test_index_page(monkeypatch, client):
    def fake_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, 'get', fake_get)
    response = client.get('/')
    response_html = response.data

    assert 'apples' in response_html.decode("utf-8")
    assert 'TODO' in response_html.decode("utf-8")
