from flask import (Blueprint, Response, flash, g, redirect, render_template,
                   request)
from werkzeug.exceptions import abort

from ndq.anmol import parse_news_sources
from ndq.db import TOPIC_LIST, get_db

bp = Blueprint('news', __name__)


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/<topic>')
def topic(topic):
    db = get_db()
    print(topic)
    articles = db.execute(
        'SELECT * FROM article WHERE topic = ? ORDER BY published DESC',
        (topic, )).fetchall()
    print(articles)
    return render_template(
        'topic.html', articles=articles, topic=topic.capitalize())


@bp.route('/me')
def me():
    db = get_db()

    topics = request.args.get('topics').split(',')

    query = 'SELECT * FROM article WHERE'
    for topic in topics:
        query += ' topic = \'' + topic + '\' OR'

    query = query[:-3] + 'ORDER BY published DESC'

    articles = db.execute(query).fetchall()
    return render_template('me.html', articles=articles)


@bp.route('/')
def index():
    db = get_db()

    articles = db.execute('SELECT * FROM article ORDER BY published DESC')

    return render_template('index.html', articles=articles)


@bp.route('/update-articles', methods=['POST'])
def update_articles():
    db = get_db()
    for topic in TOPIC_LIST:
        articles = parse_news_sources(topic, 5, 50)
        for article in articles:
            if article['author']:
                article['author'] = ', '.join(article['author'].split(','))
            else:
                article['author'] = ''
            db.execute(
                'INSERT INTO article (headline, body, link, topic, published, author, imglink) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (article['headline'], article['body'], article['link'], topic,
                 article['published'], article['author'], article['image']))
            db.commit()

    return Response(status=200)


@bp.route('/update-articles/topic', methods=['POST'])
def update_articles():
    db = get_db()
    topic request.form['topic']
    articles = parse_news_sources(topic, 5, 50)
    for article in articles:
        if article['author']:
            article['author'] = ', '.join(article['author'].split(','))
        else:
            article['author'] = ''
        db.execute(
            'INSERT INTO article (headline, body, link, topic, published, author, imglink) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (article['headline'], article['body'], article['link'], topic,
             article['published'], article['author'], article['image']))
        db.commit()

    return Response(status=200)


def get_top_news():
    db = get_db()
    headlines = db.execute(
        'SELECT headline FROM article ORDER BY published DESC').fetchone()
    return headlines[0]
