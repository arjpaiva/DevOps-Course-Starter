from card import Card
from card import Status
from datetime import datetime
from typing import List


class ViewModel:

    def __init__(self, items: List[Card]):
        self._items = items
        self._show_all_done_items = len(self.items_by_type(Status.DONE)) <= 5

    @property
    def items(self):
        return self._items

    @property
    def show_all_done_items(self):
        return self._show_all_done_items

    def items_by_type(self, status: Status) -> List[Card]:
        todo_items = []
        for item in self._items:
            if item.status == status:
                todo_items.append(item)
        return todo_items

    def recent_done_items(self) -> List[Card]:

        items = self.items_by_type(Status.DONE)
        if self._show_all_done_items:
            return items

        items_completed_today = []
        for item in items:
            if datetime.today().date() == item.last_modified.date():
                items_completed_today.append(item)

        return items_completed_today

    def older_done_items(self) -> List[Card]:

        items = self.items_by_type(Status.DONE)
        if self._show_all_done_items:
            return []

        items_completed_today = []
        for item in items:
            if datetime.today().date() > item.last_modified.date():
                items_completed_today.append(item)

        return items_completed_today
