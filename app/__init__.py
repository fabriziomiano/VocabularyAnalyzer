"""
Flask application factory
"""
import os

import spacy
from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

nlp = spacy.load(os.environ["MODEL"])


def create_app():
    """
    Create flask application
    """
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'public/uploads')
    app.config['RESULTS_FOLDER'] = os.path.join(
        app.root_path, 'static/img/results')

    from .api import api
    app.register_blueprint(api)

    from .views import ui
    app.register_blueprint(ui)

    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.error("{}".format(e))
        return render_template('404.html'), 404

    return app
