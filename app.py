from flask import Flask, render_template, request, redirect, url_for
import trello_service as trello
import logging
from view_model import ViewModel
from card import Status


def create_app():
    app = Flask(__name__)
    app.config.from_object('flask_config.Config')

    @app.route('/favicon.ico')
    def favicon():
        return app.send_static_file('web/favicon.ico')

    @app.route('/')
    def index():
        cards = get_and_sort_cards_by_status()
        view_model = ViewModel(cards)
        return render_template('index.html', view_model=view_model,
                               status_done=Status.DONE,
                               status_todo=Status.TODO,
                               status_doing=Status.DOING)

    @app.route('/', methods=['POST'])
    def add_item():

        title = request.form['title']
        cards = get_and_sort_cards_by_status()

        if title == '':
            view_model = ViewModel(cards)
            view_model.error = "Title can not be empty"
            return render_template('index.html', view_model=view_model,
                                   status_done=Status.DONE,
                                   status_todo=Status.TODO,
                                   status_doing=Status.DOING)

        for card in cards:
            if card.title == title:
                error_message = 'A card with the title ' + title + ' already exists.'
                logging.error(error_message)
                view_model = ViewModel(cards)
                view_model.error = error_message
                return render_template('index.html', view_model=view_model,
                                       status_done=Status.DONE,
                                       status_todo=Status.TODO,
                                       status_doing=Status.DOING)

        trello.create_card(title)
        return redirect('/')

    @app.route('/<card_id>', methods=['POST'])
    def move_state(card_id):
        print('moving cards')
        trello.update_card(card_id)
        return redirect(url_for('index'))

    @app.route('/<card_id>/delete', methods=['POST'])
    @app.route('/<card_id>', methods=['DELETE'])
    def delete_item(card_id):
        trello.delete_card(card_id)
        return redirect(url_for('index'))

    @app.route('/', methods=['DELETE'])
    @app.route('/delete', methods=['POST'])
    def delete_all_items():
        trello.archive_all_card()

        return redirect(url_for('index'))

    def get_and_sort_cards_by_status():
        cards = trello.get_cards()
        cards.sort(key=get_status)
        return cards

    def get_status(card) -> Status:
        return card.status.value

    if __name__ == '__main__':
        app.run()

    return app
