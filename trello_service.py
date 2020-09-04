import requests
import configparser
import board as b
import logging

config = configparser.ConfigParser()
config.read('.cfg')
trello = config['TRELLO']


def get_cards():
    all_cards_url = 'https://api.trello.com/1/boards/{0}/cards'.format(trello['BOARD_ID'])

    response = requests.get(all_cards_url, params={'key': trello['KEY'], 'token': trello['TOKEN']})

    if response.status_code != 200:
        logging.error('While trying to get all cards for board [{0}] - status code {1}'
                      .format(trello['BOARD_ID'], response.status_code))
        return []

    card_json = response.json()

    cards = []
    for card_json in card_json:
        status = 'Not Started' if card_json['idList'] == trello['NOT_STARTED_LIST_ID'] else 'Completed'

        card = b.Card(card_json['id'], card_json['name'], status)
        cards.append(card)

    return cards


def create_card(card_title):
    logging.debug('Create card with title [{}]'.format(card_title))
    create_card_url = 'https://api.trello.com/1/cards'

    response = requests.post(create_card_url, params={'key': trello['KEY'],
                                                      'token': trello['TOKEN'],
                                                      'idList': trello['NOT_STARTED_LIST_ID'],
                                                      'name': card_title})

    if response.status_code != 200:
        logging.error('While trying to create card with title [{0}] - status code {1}'
                      .format(card_title, response.status_code))


def update_card(card_id):
    logging.debug('Update status from \'Not Started\' to \'Completed\' of the card with id [{}]'.format(card_id))

    update_card_url = 'https://api.trello.com/1/cards/{0}'.format(card_id)
    response = requests.put(update_card_url, params={'key': trello['KEY'],
                                                     'token': trello['TOKEN'],
                                                     'idList': trello['COMPLETED_LIST_ID']})

    if response.status_code != 200:
        logging.error('While trying to update card with id [{0}] - response status code {1}'
                      .format(card_id, response.status_code))


def delete_card(card_id):
    logging.debug('Delete card with id [{0}]'.format(card_id))
    delete_card_url = 'https://api.trello.com/1/cards/{0}'.format(card_id)

    response = requests.delete(delete_card_url, params={'key': trello['KEY'], 'token': trello['TOKEN']})

    if response.status_code != 200:
        logging.error('While trying to delete card with id [{0}] - response status code {1}'
                      .format(card_id, response.status_code))


def archive_all_card():
    logging.debug('Archive all cards from the board')
    url = 'https://api.trello.com/1/lists/{0}/archiveAllCards'
    archive_card_url_not_started_list = url.format(trello['NOT_STARTED_LIST_ID'])
    archive_card_url_completed = url.format(trello['COMPLETED_LIST_ID'])

    response_not_started = requests.post(archive_card_url_not_started_list,
                                         params={'key': trello['KEY'], 'token': trello['TOKEN']})

    if response_not_started.status_code != 200:
        logging.error('While trying to archive all card - response status code {0}'
                      .format(response_not_started.status_code))

    response_completed = requests.post(archive_card_url_completed,
                                       params={'key': trello['KEY'], 'token': trello['TOKEN']})

    if response_completed.status_code != 200:
        logging.error('While trying to archive all card - response status code {0}'
                      .format(response_completed.status_code))
