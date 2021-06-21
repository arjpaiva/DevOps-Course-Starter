from datetime import datetime


class List:

    def __init__(self, list_id, name, last_modified, cards=None):
        if cards is None:
            cards = []

        self.id = list_id
        self.title = name
        self.cards = cards
        self.last_modified: datetime = datetime.strptime(last_modified, '%Y-%m-%dT%H:%M:%S.%fZ')

    def __str__(self):
        return self.id + " " + self.title + " " + str(self.last_modified) + " " + str(self.cards)
