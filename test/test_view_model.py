import pytest
from view_model import ViewModel
from card import Card, Status


@pytest.fixture
def view_model() -> ViewModel:
    items = [Card(1, "Bananas", Status.TODO),
             Card(2, "Pears", Status.DONE),
             Card(3, "Apples", Status.DOING),
             Card(4, "Coffee", Status.TODO)]
    return ViewModel(items)


def test_todo_items(view_model: ViewModel):
    todo_items = view_model.items_by_type(Status.TODO)
    assert len(todo_items) == 2
    for item in todo_items:
        assert item.status == Status.TODO
        assert item.title in ["Bananas", "Coffee"]


def test_todo_items_when_no_items():
    view_model = ViewModel([])
    todo_items = view_model.items_by_type(Status.TODO)
    assert len(todo_items) == 0


def test_todo_items_when_items_of_status():
    view_model = ViewModel([Card(2, "Pears", Status.DONE)])
    todo_items = view_model.items_by_type(Status.TODO)
    assert len(todo_items) == 0


def test_done_items(view_model: ViewModel):
    done_items = view_model.items_by_type(Status.DONE)
    assert len(done_items) == 1
    for item in done_items:
        assert item.status == Status.DONE
        assert item.title == "Pears"


def test_done_items_when_no_items():
    view_model = ViewModel([])
    todo_items = view_model.items_by_type(Status.DONE)
    assert len(todo_items) == 0


def test_done_items_when_items_of_status():
    view_model = ViewModel([Card(2, "Pears", Status.TODO)])
    todo_items = view_model.items_by_type(Status.DONE)
    assert len(todo_items) == 0


def test_doing_items(view_model: ViewModel):
    done_items = view_model.items_by_type(Status.DOING)
    assert len(done_items) == 1
    for item in done_items:
        assert item.status == Status.DOING
        assert item.title == "Apples"


def test_doing_items_when_no_items():
    view_model = ViewModel([])
    todo_items = view_model.items_by_type(Status.DOING)
    assert len(todo_items) == 0


def test_doing_items_when_items_of_status():
    view_model = ViewModel([Card(2, "Pears", Status.DONE)])
    todo_items = view_model.items_by_type(Status.DOING)
    assert len(todo_items) == 0
