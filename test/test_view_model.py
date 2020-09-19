import pytest
from view_model import ViewModel
from card import Card, Status


@pytest.fixture
def view_model() -> ViewModel:
    items = [Card(1, "Bananas", Status.TODO), Card(2, "Pears", Status.DONE)]
    return ViewModel(items)


def test_todo_items(view_model: ViewModel):
    todo_items = view_model.items_by_type(Status.TODO)
    assert len(todo_items) == 1
    for item in todo_items:
        assert item.status == Status.TODO


def test_done_items(view_model: ViewModel):
    done_items = view_model.items_by_type(Status.DONE)
    assert len(done_items) == 1
    for item in done_items:
        assert item.status == Status.DONE
