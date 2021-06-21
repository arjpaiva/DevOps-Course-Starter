from pymongo import MongoClient
from bson.objectid import ObjectId
from card import Card, Status
from datetime import timezone, datetime
import logging
import os

client = MongoClient(
    "mongodb+srv://ritadevops:ritadevops@cluster0.qs8y5.mongodb.net/todo_db?retryWrites=true&w=majority")


def get_collections():
    database_name = os.getenv('DATABASE_NAME')
    print('database_name' + str(database_name))
    db = client[database_name]
    return db


def create_card(card_title):
    card = {
        'title': card_title,
        'list_id': os.getenv('TODO_LIST_ID'),
        'last_modified': datetime.now(tz=timezone.utc)
    }

    result = get_collections().card.insert_one(card)

    print('RESULT: ' + str(result.inserted_id))


def get_cards():
    cards = []
    for card_json in get_collections().card.find():
        if card_json is not None:
            status = from_list_id_to_status(card_json['list_id'])
            card = Card(card_json['_id'], card_json['title'], status, card_json['last_modified'])
            cards.append(card)

    return cards


def update_card(card_id):
    print("UPDATING CARD ID: " + str(card_id))
    logging.debug(f'Update status from {Status.TODO} to {Status.DOING} of the card with id [{card_id}]')

    card = get_card(card_id)
    list_id = get_next_status_list_id(card.status)
    get_collections().card.update_one({'_id': ObjectId(card_id)}, {'$set': {'list_id': list_id}})


def get_card(card_id):

    card_json = get_collections().card.find_one(ObjectId(card_id))
    status = from_list_id_to_status(card_json['list_id'])
    card = Card(card_json['_id'], card_json['title'], status, card_json['last_modified'])
    return card


def delete_card(card_id):
    get_collections().card.delete_one({'_id': ObjectId(card_id)})


def delete_all_cards():
    get_collections().card.drop()


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