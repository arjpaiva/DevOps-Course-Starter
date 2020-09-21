from card import Card
from card import Status
from datetime import datetime
from typing import List


class ViewModel:

    def __init__(self, items: List[Card]):
        self._items = items

    @property
    def items(self):
        return self._items

    def items_by_type(self, status: Status) -> List[Card]:
        todo_items = []
        for item in self._items:
            if item.status == status:
                todo_items.append(item)
        return todo_items

    def get_completed_items(self) -> List[Card]:
        items = self.items_by_type(Status.DONE)
        if len(items) <= 5:
            return items

        items_completed_today = []
        for item in items:
            if datetime.today().day == item.last_modified.day:
                items_completed_today.append(item)

        return items_completed_today
