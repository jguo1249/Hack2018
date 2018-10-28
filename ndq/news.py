from flask import (Blueprint, Response, flash, g, redirect, render_template,
                   request, url_for)
from werkzeug.exceptions import abort

from ndq.anmol import parse_news_sources
from ndq.db import get_db

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

    return render_template('index.html', articles=articles)


@bp.route('/update-articles', methods=['POST'])
def update_articles():
    db = get_db()
    world_articles = parse_news_sources('world')
    print(world_articles)
    # for article in world_articles:
    #     print(article)
    #     query = 'INSERT INTO article (headline, body, link, topic, published, author, imglink) VALUES ({headline}, {body}, {link}, {topic}, {published}, {author}, {imglink})'.format(
    #         headline=article.headline,
    #         body=article.body,
    #         link=article.link,
    #         topic=topic,
    #         published=article.published,
    #         author=article.author,
    #         imglink=article.image)
    #     db.execute(query)
    #     db.commit()

    article = {
        'headline':
        'Right-Wing Candidate Poised For Win As Brazilians Head To Polls',
        'body':
        'Sao Paulo, Brazil  Brazilians on Sunday will elect the country\'s next President amid one of the most polarizing and violent political campaigns in its history. This comes as the country of 200 million people continues to suffer from a prolonged recession, rising insecurity, and a massive corruption scandal that rocked political and financial institutions. During his Brazil tour, Pink Floyd co-founder Roger Waters exhibited the slogan on stage in neon lights and chanted "ele nao" with the crowd. Lago created an Instagram account called "elenaovaoinosmatar," or "he won\'t kill us" in English, shortly after being verbally assaulted and threatened by a group of Bolsonaro supporters for being gay. Laura Chinchilla, the head of the Organization of American States mission of observers for the Sunday election, said she worries about a fake news "phenomenon" seen throughout the campaign. Whatsapp shut down a number of accounts following an investigation by Brazilian daily Folha de Sao Paulo that found companies were buying mass text messaging packages to blast users with negative campaign ads on their phones. "Today, as part of our ongoing efforts to protect our community from this type of abuse, Facebook removed 68 Pages and 43 accounts associated with a Brazilian marketing group, Raposo Fernandes Associados (RFA), for violating our misrepresentation and spam policies." The Workers\' Party governed Brazil for more than 13 years under President Luiz Inacio Lula da Silva, from 2003 to 2011, and his successor Dilma Rousseff, from 2011 to 2016.',
        'link':
        'https://www.cnn.com/2018/10/27/americas/brazil-election/index.html',
        'topic':
        'world',
        'published':
        '2018-06-19 12:00:00',
        'author':
        'Flora Charner,Marcia Reverdosa',
        'image':
        'https://cdn.cnn.com/cnnnext/dam/assets/181016150659-bolsonaro-haddad-super-tease.jpg'
    }

    # query = 'INSERT INTO article (headline, body, link, topic, published, author, imglink) VALUES ("{headline}", "{body}", "{link}", "{topic}", "{published}", "{author}", "{imglink}")'.format(
    #     headline=article['headline'],
    #     body=article['body'],
    #     link=article['link'],
    #     topic=topic,
    #     published=article['published'],
    #     author=article['author'],
    #     imglink=article['image'])
    # print(query)

    topic = 'world'

    db.execute(
        'INSERT INTO article (headline, body, link, topic, published, author, imglink) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (article['headline'], article['body'], article['link'], topic,
         article['published'], article['author'], article['image']))
    db.commit()

    return Response(status=200)
