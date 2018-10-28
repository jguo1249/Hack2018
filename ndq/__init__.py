import os

from flask import Flask, request, Response

from ndq.twilio_functions import process_info
from ndq.db import get_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'ndq.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/god', methods=['POST'])
    def god():
      if request.method == 'POST':
        from_number = request.form['From']
        body = request.form['Body']
        db = get_db()
        print(body)
        try:
          process_info(body, from_number, db)
          return Response(status=200)
        except:
          return Response(status=500)
      else:
        return Response(status=404)



    from . import db
    db.init_app(app) #init db

    from . import user
    app.register_blueprint(user.bp) #create blueprint

    from . import news #news view
    app.register_blueprint(news.bp)
    #app.add_url_rule('/', endpoint='index')

    return app
