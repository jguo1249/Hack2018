import functools

from flask import (
  Blueprint, g, request, url_for
)

from ndq.db import get_db, TOPICLIST

bp = Blueprint('user', __name__, url_prefix='/user')

def parse_topics(topics):
  returned = {}
  for T in TOPICLIST:
    if T in topics:
      returned[T] = True
    else:
      returned[T] = False
  return returned

@bp.route('/signup', methods=['POST'])
def signup():
  phone = request.form['phone']
  topics = request.form['topics']
  frequency = request.form['frequency']
  firstDelivery = request.form['firstDelivery']

  db = get_db()
  error = None

  if not phone:
    error = 'Phone number is required.'
  elif not password:
    error = 'Password is required.'
  elif db.execute(
    'SELECT id FROM user WHERE phone = ?', (phone,)
  ).fetchone() is not None:
    error = 'Phone number {} is already registered.'.format(phone)

  if error is None:
    topics = parse_topics(topics)
    db.execute(
      'INSERT INTO user (phone, world, local, sports, science, food, entertainment, politics, technology, context, frequency, firstDelivery) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
      (username, topics["world"], topics["local"],
       topics["sports"], topics["science"], topics["food"],
       topics["entertainment"], topics["politics"], topics["technology"], frequency, firstDelivery)
    )
    db.commit()
  return 200

def change_topics(phone, new_topics):
  new_topics = parse_topics(new_topics)

  db.execute(
    'UPDATE user SET (world, local, sports, science, food, entertainment, politics, technology) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ) WHERE phone = ?', # almost positive this won't work #TODO
    (topics["world"], topics["local"],
     topics["sports"], topics["science"], topics["food"],
     topics["entertainment"], topics["politics"], topics["technology"], phone)
  )
  db.commit()

def unsubscribe(phone):
  db.execute(
    'DELETE user WHERE phone = ?', # not sure that this will work #TODO
    (phone)
  )
  db.commit()

def change_frequency(phone, frequency):
  db.execute(
    'UPDATE user SET (frequency) VALUES (?) WHERE phone = ?', # almost positive this won't work #TODO
    (frequency, phone)
  )
  db.commit()

def change_delivery_time(phone, time):
   db.execute(
     'UPDATE user SET (firstDelivery) VALUES (?) WHERE phone = ?', # almost positive this won't work #TODO
     (time, phone)
   )
   db.commit()
