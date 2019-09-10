"""
The flask application package.
"""
from flask import Flask
import os
import spacy

app = Flask(__name__)
app.secret_key = os.urandom(24)
CWD = os.getcwd()
UPLOAD_FOLDER = os.path.join(CWD, 'Vocabanal/public/uploads')
RESULTS_FOLDER = os.path.join(CWD, 'Vocabanal/static/img/results/fullsize')
english_model = "en_core_web_md"
app.logger.info("Loading spaCy model: {0}".format(english_model))
nlp = spacy.load(english_model)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
from Vocabanal import views, api
