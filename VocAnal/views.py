"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template
from VocAnal import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year,
    )
