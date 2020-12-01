import os
import app
import pytest
import trello_service
from card import Status
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from threading import Thread


@pytest.fixture(scope="module")
def driver():
    with webdriver.Chrome() as driver:
        yield driver


@pytest.fixture(scope='module')
def new_board():
    # Load env properties
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    # Create the new board & update the board id environment variable
    board_id = trello_service.create_board('selenium')
    os.environ['BOARD_ID'] = board_id

    lists = trello_service.get_lists_per_board()
    if lists is None:
        return

    os.environ['TODO_LIST_ID'] = lists[Status.TODO]
    os.environ['DOING_LIST_ID'] = lists[Status.DOING]
    os.environ['DONE_LIST_ID'] = lists[Status.DONE]

    # construct the new application
    application = app.create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    # Tear Down
    thread.join(1)
    trello_service.delete_board()


def test_item_journey(driver, new_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

    todo_empty_list = driver.find_element_by_id('no-todo-items-message')
    assert 'No items found' in str(todo_empty_list.text)

    doing_empty_list = driver.find_element_by_id('no-doing-items-message')
    assert 'No items found' in str(doing_empty_list.text)

    done_empty_list = driver.find_element_by_id('no-done-items-message')
    assert 'No items found' in str(done_empty_list.text)

    driver.find_element_by_id('add-item').click()
    driver.implicitly_wait(5)
    new_title_input = driver.find_element_by_id('title')
    new_title_input.send_keys('test-name')
    new_title_input.submit()
    driver.implicitly_wait(5)

    todo_list = driver.find_element_by_id('todo-item-title')
    assert 'test-name' in str(todo_list.text)

    driver.find_element_by_id('move_item_to_doing').click()
    doing_list = driver.find_element_by_id('doing-item-title')
    assert 'test-name' in str(doing_list.text)

    driver.find_element_by_id('move_item_to_done').click()
    done_list = driver.find_element_by_id('done-item-title')
    assert 'test-name' in str(done_list.text)




