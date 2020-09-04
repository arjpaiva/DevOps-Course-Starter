from flask import Flask, render_template, request, redirect, url_for
import session_items as session
import trello_service as trello

app = Flask(__name__)
app.config.from_object('flask_config.Config')


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('web/favicon.ico')


@app.route('/')
def index():
    cards = get_and_sort_cards_by_status()
    return render_template('index.html', items=cards)


@app.route('/', methods=['POST'])
def add_item():

    title = request.form['title']
    cards = trello.get_cards()

    if title == '':
        return render_template('index.html', items=cards)

    for card in cards:
        if card.title == title:
            # todo show error on front end
            print('A card with the title ' + title + ' already exists.')
            return render_template('index.html', items=cards)

    trello.create_card(title)
    cards = get_and_sort_cards_by_status()

    return render_template('index.html', items=cards)


@app.route('/<card_id>')
def get_item(card_id):
    session.get_item(card_id)
    return index()


@app.route('/<card_id>', methods=['POST'])
def mark_as_completed(card_id):
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
    print('before delete')
    trello.archive_all_card()
    print('after delete')

    return redirect(url_for('index'))


def get_and_sort_cards_by_status():
    cards = trello.get_cards()
    cards.sort(key=get_status)
    return cards


def get_status(card):
    return card.status


if __name__ == '__main__':
    app.run()
