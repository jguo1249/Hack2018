import datetime
import functools

from flask import Blueprint, Response, flash, g, redirect, request, url_for

from ndq.db import TOPIC_LIST, get_db, parse_topics
from ndq.twilio_functions import send_data, twilio_signup

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/signup', methods=['POST'])
def signup():

    phone = '+1' + request.form['phone']
    topics = []

    for value in request.form.getlist('topics[]'):
        topics.append(value)

    frequency = request.form['frequency']
    firstDelivery = request.form['firstDelivery']
    firstDelivery = datetime.datetime.now()

    print(topics)

    db = get_db()
    error = None

    if not phone:
        error = 'Phone number is required.'
    elif db.execute('SELECT id FROM user WHERE phone = ?',
                    (phone, )).fetchone() is not None:
        error = 'Phone number {} is already registered.'.format(phone)

    if error is None:
        topics_dict = parse_topics(topics)

        db.execute(
            'INSERT INTO user (phone, world, local, sports, science, food, entertainment, politics, technology, context, frequency, firstDelivery) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (phone, topics_dict["world"], topics_dict["local"],
             topics_dict["sports"], topics_dict["science"],
             topics_dict["food"], topics_dict["entertainment"],
             topics_dict["politics"], topics_dict["technology"], '', frequency,
             firstDelivery))
        db.commit()
        twilio_signup(phone)
        send_data(
            'http://www.newsdonequick.online{}'.format(
                url_for('news.me', topics=','.join(topics)).replace(
                    '%2C', ',')), phone)

        return redirect(
            url_for('news.me', topics=','.join(topics)).replace('%2C', ','))

    flash(error)
    return redirect(url_for('news.index'))


def get_me_link(phone):
    user = get_db().execute('SELECT * FROM user WHERE phone = ?',
                            (phone, )).fetchone()

    topics = []

    for key in user.keys():
        topics.append(user[key])

    return 'http://www.newsdonequick.online{}'.format(
        url_for('news.me', topics=','.join(topics)).replace('%2C', ','))
