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

def get_attribute(phone, attribute):
  db = get_db()
  attr = db.execute(
    'SELECT ? FROM user WHERE phone = ?' # not sure this works #TODO
    (attribute, phone)
  )
  return attr

def set_attribute(phone, attribute):
  get_db.execute(
    'UPDATE ? FROM user WHERE phone = ?' # not sure this works #TODO
    (attribute, phone)
  )

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

def change_frequency(phone, frequency):
  db = get_db()
  db.execute(
    'UPDATE user SET (frequency) VALUES (?) WHERE phone = ?', # almost positive this won't work #TODO
    (frequency, phone)
  )
  db.commit()

def change_delivery_time(phone, time):
  db = get_db()
  db.execute(
    'UPDATE user SET (firstDelivery) VALUES (?) WHERE phone = ?', # almost positive this won't work #TODO
    (time, phone)
  )
  db.commit()
