import functools
import datetime

from flask import Blueprint, Response, flash, g, redirect, request, url_for

from ndq.db import TOPIC_LIST, get_db, parse_topics
from ndq.twilio_functions import twilio_signup

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/signup', methods=['POST'])
def signup():
    phone = '+1' + request.form['phone']
    topics = request.form['topics[]']
    frequency = request.form['frequency']
    firstDelivery = request.form['firstDelivery']
    firstDelivery = datetime.datetime.now() 

    db = get_db()
    error = None

    if not phone:
        error = 'Phone number is required.'
    elif db.execute('SELECT id FROM user WHERE phone = ?',
                    (phone, )).fetchone() is not None:
        error = 'Phone number {} is already registered.'.format(phone)

    if error is None:
        topics = parse_topics(topics)
        db.execute(
            'INSERT INTO user (phone, world, local, sports, science, food, entertainment, politics, technology, context, frequency, firstDelivery) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (phone, topics["world"], topics["local"], topics["sports"],
             topics["science"], topics["food"], topics["entertainment"],
             topics["politics"], topics["technology"], '', frequency,
             firstDelivery))
        db.commit()
        twilio_signup(phone)

        topic_param = topics
        print(topic_param)
        return redirect(url_for('news.me'), topics=topic_param)

    flash(error)
    return redirect(url_for('news.index'))
