from flask import (Blueprint, Response, flash, g, redirect, render_template,
                   request, url_for)
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
    articles = db.execute('SELECT * FROM article WHERE topic = ?',
                          (topic, )).fetchall()
    return render_template(
        'topic.html', articles=articles, topic=topic.capitalize())


@bp.route('/me')
def me():
    db = get_db()

    topics = request.args.get('topics').split(',')

    print(topics)

    query = 'SELECT * FROM article WHERE'
    query += ' topic = \'' + topics[0]
    query += '\''

    print(query)

    articles = db.execute(query).fetchall()
    return render_template('me.html', articles=articles)


@bp.route('/')
def index():
    db = get_db()

    articles = db.execute('SELECT * FROM article')

    for article in articles:
        if article['author']:
            print()

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

    # topic = 'local'
    #
    # db.execute(
    #     'INSERT INTO article (headline, body, link, topic, published, author, imglink) VALUES (?, ?, ?, ?, ?, ?, ?)',
    #     (article['headline'], article['body'], article['link'], topic,
    #      article['published'], article['author'], article['image']))
    # db.commit()

    return Response(status=200)
