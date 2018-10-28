import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

TOPIC_LIST = set([
    "world", "local", "sports", "science", "food", "entertainment", "politics",
    "technology"
])


def parse_topics(topics):
    return {t: t in topics for t in TOPIC_LIST}


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def get_attribute(phone, attribute):
    db = get_db()
    attr = db.execute('SELECT * FROM user WHERE phone = ?',
                      (phone, )).fetchone()[attribute]

    return attr


def get_topics(phone):
    db = get_db()
    attr = db.execute('SELECT * FROM user WHERE phone = ?',
                      (phone, )).fetchone()
    ls = []
    for col in attr.keys():
        if attr[col] == 1 and col in TOPIC_LIST:
            ls.append(col)

    print(ls)
    return ls


def set_attribute(phone, attribute, value):
    print(phone, attribute, value)
    db = get_db()
    db.execute('UPDATE user SET {} = ? WHERE phone = ?'.format(attribute), (
        value,
        phone,
    ))
    db.commit()


def change_topics(phone, topics):
    topics = parse_topics(topics)
    db = get_db()

    db.execute(
        'UPDATE user SET world = ?, local = ?, sports = ?, science = ?, food = ?, entertainment = ?, politics = ?, technology = ? WHERE phone = ?',
        (topics["world"], topics["local"], topics["sports"], topics["science"],
         topics["food"], topics["entertainment"], topics["politics"],
         topics["technology"], phone))
    db.commit()


def unsubscribe(phone):
    db = get_db()
    db.execute(
        'DELETE FROM user WHERE phone = ?',  # not sure that this will work #TODO
        (phone, ))
    db.commit()


def get_me_link(phone):
    user = get_db().execute('SELECT * FROM user WHERE phone = ?',
                            (phone, )).fetchone()

    topics = []

    for key in user.keys():
        topics.append(user[key])

    return 'http://www.newsdonequick.online{}'.format(
        url_for('news.me', topics=','.join(topics)).replace('%2C', ','))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
