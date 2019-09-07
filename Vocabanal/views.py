"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template, send_from_directory, url_for
from Vocabanal import app

#
# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template('404.jade'), 404


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year,
    )


@app.route('/api/download')
def download():
    """Return the files produced"""
    # TODO Call a function to zip the files produced and return the archive
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year,
    )
