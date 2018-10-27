import functools

from flask import (
  Blueprint, g, request, redirect, url_for, Response
)

from ndq.db import get_db, TOPIC_LIST
from ndq.twilio_functions import twilio_signup

bp = Blueprint('user', __name__, url_prefix='/user')

def parse_topics(topics):
  return {t: t in topics for t in TOPIC_LIST}


@bp.route('/signup', methods=['POST'])
def signup():
  phone = request.form['phone']
  topics = request.form['topics[]']
  frequency = request.form['frequency']
  firstDelivery = request.form['firstDelivery']

  db = get_db()
  error = None

  if not phone:
    error = 'Phone number is required.'
  elif db.execute(
    'SELECT id FROM user WHERE phone = ?', (phone,)
  ).fetchone() is not None:
    error = 'Phone number {} is already registered.'.format(phone)

  if error is None:
    topics = parse_topics(topics)
    db.execute(
      'INSERT INTO user (phone, world, local, sports, science, food, entertainment, politics, technology, context, frequency, firstDelivery) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
      (phone, topics["world"], topics["local"],
       topics["sports"], topics["science"], topics["food"],
       topics["entertainment"], topics["politics"], topics["technology"], '', frequency, firstDelivery)
    )
    db.commit()
    twilio_signup(phone)


    topic_param = topics
    return redirect('/me?topics=' + topic_param)
  else:
    pass
