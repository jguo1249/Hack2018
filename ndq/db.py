import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


TOPIC_LIST = set(["world", "local", "sports", "science", "food", "entertainment", "politics", "technology"])

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
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

def get_attribute(phone, attribute, db):
  print(db)
  print(db == get_db()) # need to test
  print(db is get_db()) # need to test
  db.execute('SELECT * FROM user WHERE phone = ?', (phone,))
  attr = db.fetchone()
  print(attr)

  return attr

def get_topics(phone):
  db = get_db()
  query = 'SELECT * FROM user WHERE phone = {}'.format(phone)
  attr = db.execute(query).fetchall()
  ls = []
  for cols in attr:
    if attr[cols] == 'True':
     ls.append(cols)
  return ls


def set_attribute(phone, attribute, value):
  query = 'UPDATE user SET {} = \'{}\' WHERE phone = {}'.format(attribute, value, phone)
  db = get_db()
  db.execute(query)
  db.commit()

def change_topics(phone, new_topics):
  new_topics = parse_topics(new_topics)
  db = get_db()

  db.execute(
    'UPDATE user SET (world, local, sports, science, food, entertainment, politics, technology) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ) WHERE phone = ?', # almost positive this won't work #TODO
    (topics["world"], topics["local"],
     topics["sports"], topics["science"], topics["food"],
     topics["entertainment"], topics["politics"], topics["technology"], phone)
  )
  db.commit()

def unsubscribe(phone):
  db = get_db()
  db.execute(
    'DELETE user WHERE phone = ?', # not sure that this will work #TODO
    (phone)
  )
  db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
