import functools

from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))

    return view(**kwargs)

  return wrapped_view

base_topic = {}
@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))

@bp.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    phone = request.form['phone']
    db = get_db()
    error = None

    if not phone:
      error = 'Phone number is required.'

    elif db.count_documents(
      {"phone" : phone }
    ) > 0:
      error = 'Phone Number {} is already registered.'.format(phone)

    if error is None:
      db.insert_one(
        { "phone" : phone,
          "history" : [],
          "topic" : {}
        }
      )
      db.commit()
      return redirect(url_for('auth.login'))

    flash(error)

  return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute(
      'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
      error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
      error = 'Incorrect password.'

    if error is None:
      session.clear()
      session['user_id'] = user['id']
      return redirect(url_for('index'))

    flash(error)

  return render_template('auth/login.html')
