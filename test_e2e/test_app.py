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
    with webdriver.Chrome('/usr/local/bin/chromedriver') as driver:
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

    todo_empty_list = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[1]/div/p')
    assert 'No items found' in str(todo_empty_list.text)

    doing_empty_list = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/div/p')
    assert 'No items found' in str(doing_empty_list.text)

    done_empty_list = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[3]/div/p')
    assert 'No items found' in str(done_empty_list.text)

    driver.find_element_by_xpath('/html/body/div/div[4]/div/div/button').click()
    driver.implicitly_wait(5)
    new_title_input = driver.find_element_by_id('title')
    new_title_input.send_keys('test-name')
    new_title_input.submit()
    driver.implicitly_wait(5)

    todo_list = driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[1]')
    assert 'test-name' in str(todo_list.text)

    driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div/div[4]/form').click()
    doing_list = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/div')
    assert 'test-name' in str(doing_list.text)

    driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/div/div[4]/form').click()
    done_list = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[3]/div[2]')
    assert 'test-name' in str(done_list.text)




