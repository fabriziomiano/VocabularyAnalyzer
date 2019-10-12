"""
The flask application package.
"""
import os
import logging
import spacy
from flask import Flask


NLP = spacy.load("en_core_web_sm")
# NLP = spacy.load("en_core_web_md")
app = Flask(__name__)
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = os.path.join(app.root_path, 'public/uploads')
RESULTS_FOLDER = os.path.join(app.root_path, 'static/img/results')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.logger.setLevel(logging.INFO)
from VocAnal import views, routes
