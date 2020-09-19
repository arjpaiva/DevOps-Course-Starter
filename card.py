from enum import Enum


class Card:

    def __init__(self, card_id, name, status):
        self.id = card_id
        self.title = name
        self.status: Status = status


class Status(Enum):
    TODO = "ToDo"
    DOING = "Doing"
    DONE = "Done"


