import functools

from flask import (
  Blueprint, g, request, url_for
)

from flaskr.db import get_db, TOPICLIST

bp = Blueprint('auth', __name__, url_prefix='/auth')

def parse_topics(topics):
  returned = {}
  for T in TOPICLIST:
    if T in topics:
      returned[T] = True
    else:
      returned[T] = False
  return returned

@bp.route('/signup', methods=('POST'))
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
      'INSERT INTO user (phone, world, local, sports, science, food,
      entertainment, politics, technology, context, frequency, firstDelivery)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
      (username, topics["world"], topics["local"],
       topics["sports"], topics["science"], topics["food"],
       topics["entertainment"], topics["politics"], topics["technology"], frequency, firstDelivery)
    )
    db.commit()
