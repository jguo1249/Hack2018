from flask import (
  Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from ndq.db import get_db

bp = Blueprint('news', __name__)

@bp.route('/about')
def about():
  return render_template('about.html')

@bp.route('/<topic>')
def topic(topic):
  db = get_db()
  articles = db.execute(
    'SELECT * FROM article WHERE topic = ?', (topic,)
  ).fetchall()
  return render_template('topic.html', articles=articles)

@bp.route('/me')
def me():
  db = get_db()

  topics = request.args.get('topic').split(',')

  temp = db.execute(
    'SELECT * FROM article WHERE topic IN ?'
    ' ORDER BY topic ASC',
    (topics)
  ).fetchall()
  return render_template('me.html', articles=articles)

@bp.route('/')
def index():
  db = get_db()

  articles = db.execute(
    'SELECT * FROM article'
  )

  return render_template('index.html', articles=articles)

@bp.route('/god', methods=['POST'])
def god():
  pass

def get_post(id, check_author=True):
  post = get_db().execute(
    'SELECT p.id, title, body, created, author_id, username'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' WHERE p.id = ?',
    (id,)
  ).fetchone()

  if post is None:
    abort(404, "Post id {0} doesn't exist.".format(id))

  if check_author and post['author_id'] != g.user['id']:
    abort(403)

  return post


@bp.route("/<int:id>/update", methods=["GET", "POST"])
def update(id):
  post = get_post(id)

  if request.method == 'POST':
    title = request.form['title']
    body = request.form['body']
    error = None

    if not title:
      error = 'Title is required.'

    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'UPDATE post SET title = ?, body = ?'
        ' WHERE id = ?',
        (title, body, id)
      )
      db.commit()
      return redirect(url_for('blog.index'))

  return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=["POST"])
def delete(id):
  get_post(id)
  db = get_db()
  db.execute('DELETE FROM post WHERE id = ?', (id,))
  db.commit()
  return redirect(url_for('blog.index'))
