from card import Card
from card import Status
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
