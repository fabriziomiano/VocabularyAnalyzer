"""
Views for the flask application.
"""
from datetime import datetime

from flask import Blueprint, render_template

ui = Blueprint('ui', __name__)


@ui.route('/')
@ui.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year,
    )
