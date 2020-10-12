import requests
from card import Card, Status
import logging
import os


def create_board(board_name):
    create_board_url = f'https://api.trello.com/1/boards/'
    response = requests.post(create_board_url,
                             params={'key': os.getenv('TRELLO_KEY'), 'token': os.getenv('TOKEN'), 'name': board_name})

    if response.status_code != 200:
        logging.error(
            f'While trying to create board with name [{os.getenv("BOARD_ID")}] - status code {response.status_code}')
        return None

    board_json = response.json()
    return board_json['id']


def delete_board():
    delete_board_url = f'https://api.trello.com/1/boards/{os.getenv("BOARD_ID")}'
    response = requests.delete(delete_board_url, params={'key': os.getenv('TRELLO_KEY'), 'token': os.getenv('TOKEN')})

    if response.status_code != 200:
        logging.error(
            f'While trying to delete board with name [{os.getenv("BOARD_ID")}] - status code {response.status_code}')
        return None


def get_lists_per_board():
    all_lists_per_board_url = f'https://api.trello.com/1/boards/{os.getenv("BOARD_ID")}/lists'

    response = requests.get(all_lists_per_board_url,
                            params={'key': os.getenv('TRELLO_KEY'), 'token': os.getenv('TOKEN')})
    if response.status_code != 200:
        logging.error('While trying to get all cards for board [{0}] - status code {1}'
                      .format(os.getenv('BOARD_ID'), response.status_code))

    lists = response.json()
    list_status_to_id = {}
    for board_list in lists:
        status = list_name_to_status(board_list['name'])
        list_status_to_id[status] = board_list['id']

    return list_status_to_id


def get_cards():
    all_cards_url = f'https://api.trello.com/1/boards/{os.getenv("BOARD_ID")}/cards'

    response = requests.get(all_cards_url, params={'key': os.getenv('TRELLO_KEY'), 'token': os.getenv('TOKEN')})

    if response.status_code != 200:
        logging.error('While trying to get all cards for board [{0}] - status code {1}'
                      .format(os.getenv('BOARD_ID'), response.status_code))
        return []

    card_json = response.json()

    cards = []
    for card_json in card_json:
        status = from_list_id_to_status(card_json['idList'])
        card = Card(card_json['id'], card_json['name'], status, card_json['dateLastActivity'])
        cards.append(card)

    return cards


def get_card(card_id):
    card_id_url = f'https://api.trello.com/1/cards/{card_id}'
    get_card_response = requests.get(card_id_url, params={'key': os.getenv('TRELLO_KEY'), 'token': os.getenv('TOKEN')})

    if get_card_response.status_code != 200:
        logging.error('While trying to get all cards for board [{0}] - status code {1}'
                      .format(os.getenv('BOARD_ID'), get_card_response.status_code))
        return None

    card_json = get_card_response.json()
    status = from_list_id_to_status(card_json['idList'])
    card = Card(card_json['id'], card_json['name'], status, card_json['dateLastActivity'])

    return card


def create_card(card_title):
    logging.debug('Create card with title [{}]'.format(card_title))
    create_card_url = 'https://api.trello.com/1/cards'

    response = requests.post(create_card_url, params={'key': os.getenv('TRELLO_KEY'),
                                                      'token': os.getenv('TOKEN'),
                                                      'idList': os.getenv('TODO_LIST_ID'),
                                                      'name': card_title})

    if response.status_code != 200:
        logging.error('While trying to create card with title [{0}] - status code {1}'
                      .format(card_title, response.status_code))


def update_card(card_id):
    logging.debug(f'Update status from {Status.TODO} to {Status.DOING} of the card with id [{card_id}]')
    card = get_card(card_id)
    # list_id = trello['DONE_LIST_ID'] if card.status == Status.TODO else trello['TODO_LIST_ID']
    list_id = get_next_status_list_id(card.status)
    if list_id is None:
        return

    update_card_url = f'https://api.trello.com/1/cards/{card_id}'
    response = requests.put(update_card_url, params={'key': os.getenv('TRELLO_KEY'),
                                                     'token': os.getenv('TOKEN'),
                                                     'idList': list_id})

    if response.status_code != 200:
        logging.error('While trying to update card with id [{0}] - response status code {1}'
                      .format(card_id, response.status_code))


def delete_card(card_id):
    logging.debug('Delete card with id [{0}]'.format(card_id))
    delete_card_url = f'https://api.trello.com/1/cards/{card_id}'

    response = requests.delete(delete_card_url, params={'key': os.getenv('TRELLO_KEY'), 'token': os.getenv('TOKEN')})

    if response.status_code != 200:
        logging.error('While trying to delete card with id [{0}] - response status code {1}'
                      .format(card_id, response.status_code))


def archive_all_card():
    logging.debug('Archive all cards from the board')
    url = 'https://api.trello.com/1/lists/{0}/archiveAllCards'
    archive_card_url_not_started_list = url.format(os.getenv('TODO_LIST_ID'))
    archive_card_url_completed = url.format(os.getenv('DONE_LIST_ID'))

    response_not_started = requests.post(archive_card_url_not_started_list,
                                         params={'key': os.getenv('TRELLO_KEY'), 'token': os.getenv('TOKEN')})

    if response_not_started.status_code != 200:
        logging.error('While trying to archive all card - response status code {0}'
                      .format(response_not_started.status_code))

    response_completed = requests.post(archive_card_url_completed,
                                       params={'key': os.getenv('TRELLO_KEY'), 'token': os.getenv('TOKEN')})

    if response_completed.status_code != 200:
        logging.error('While trying to archive all card - response status code {0}'
                      .format(response_completed.status_code))


def get_next_status_list_id(current_status: Status):
    if current_status == Status.TODO:
        return os.getenv('DOING_LIST_ID')
    elif current_status == Status.DOING:
        return os.getenv('DONE_LIST_ID')
    else:
        return None


def from_list_id_to_status(list_id):
    if list_id == os.getenv('TODO_LIST_ID'):
        return Status.TODO
    elif list_id == os.getenv('DOING_LIST_ID'):
        return Status.DOING
    else:
        return Status.DONE


def list_name_to_status(list_name):
    if list_name == 'To Do':
        return Status.TODO
    elif list_name == 'Done':
        return Status.DONE
    else:
        return Status.DOING
