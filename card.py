from enum import Enum
from datetime import datetime


class Card:

    def __init__(self, card_id, name, status, last_modified):
        self.id = card_id
        self.title = name
        self.status: Status = status
        self.last_modified: datetime = datetime.strptime(last_modified, '%Y-%m-%dT%H:%M:%S.%fZ')

    def __str__(self):
        return self.id + " " + self.title + " " + self.status.value + " " + str(self.last_modified)


class Status(Enum):
    TODO = "ToDo"
    DOING = "Doing"
    DONE = "Done"


