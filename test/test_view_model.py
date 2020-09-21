import pytest
from view_model import ViewModel
from card import Card, Status
from datetime import datetime, timedelta
from typing import List

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


@pytest.fixture
def view_model() -> ViewModel:
    items = [Card(1, "Bananas", Status.TODO, datetime.now().strftime(DATE_TIME_FORMAT)),
             Card(2, "Pears", Status.DONE, datetime.now().strftime(DATE_TIME_FORMAT)),
             Card(3, "Apples", Status.DOING, datetime.now().strftime(DATE_TIME_FORMAT)),
             Card(4, "Coffee", Status.TODO, datetime.now().strftime(DATE_TIME_FORMAT))]
    return ViewModel(items)


@pytest.fixture
def done_items() -> List[Card]:
    return [Card(1, "Bananas", Status.DONE, (datetime.today() - timedelta(days=2)).strftime(DATE_TIME_FORMAT)),
            Card(2, "Pears", Status.DONE, datetime.now().strftime(DATE_TIME_FORMAT)),
            Card(3, "Apples", Status.DONE, (datetime.today() - timedelta(days=1)).strftime(DATE_TIME_FORMAT)),
            Card(4, "Coffee", Status.DONE, (datetime.now() - timedelta(minutes=2)).strftime(DATE_TIME_FORMAT))]


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
    view_model = ViewModel([Card(2, "Pears", Status.DONE, datetime.now().strftime(DATE_TIME_FORMAT))])
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
    view_model = ViewModel([Card(2, "Pears", Status.TODO, datetime.now().strftime(DATE_TIME_FORMAT))])
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
    view_model = ViewModel([Card(2, "Pears", Status.DONE, datetime.now().strftime(DATE_TIME_FORMAT))])
    todo_items = view_model.items_by_type(Status.DOING)
    assert len(todo_items) == 0


def test_get_completed_items_when_less_than_5(done_items: List[Card]):
    view_model = ViewModel(done_items)
    actual_items = view_model.get_completed_items()
    assert len(actual_items) == 4


def test_get_completed_items_when_equal_5(done_items: List[Card]):
    view_model = ViewModel(done_items)
    actual_items = view_model.get_completed_items()
    actual_items.append(
        Card(5, "asdasd", Status.DONE, (datetime.today() - timedelta(days=2)).strftime(DATE_TIME_FORMAT)))
    assert len(actual_items) == 5


def test_get_completed_items_when_equal_0():
    actual_items = []
    assert len(actual_items) == 0


def test_get_completed_items_when_more_than_5(done_items: List[Card]):
    done_items.append(
        Card(5, "another one", Status.DONE, (datetime.today() - timedelta(days=2)).strftime(DATE_TIME_FORMAT)))
    done_items.append(
        Card(6, "another another one", Status.DONE, (datetime.today() - timedelta(days=3)).strftime(DATE_TIME_FORMAT)))
    view_model = ViewModel(done_items)
    actual_items = view_model.get_completed_items()

    assert len(actual_items) == 2
