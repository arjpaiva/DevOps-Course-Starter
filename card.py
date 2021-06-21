from enum import Enum
from datetime import datetime


class Card:

    def __init__(self, id, name, status, last_modified: datetime):
        self.id = id
        self.title = name
        self.status: Status = status
        self.last_modified: datetime = last_modified

    def __str__(self):
        return str(self.id) + " " + self.title + " " + self.status.value + " " + str(self.last_modified)


class Status(Enum):
    TODO = "ToDo"
    DOING = "Doing"
    DONE = "Done"


