"""
The flask application package.
"""
from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CWD = os.getcwd()
UPLOAD_FOLDER = os.path.join(CWD, 'Vocabanal/public/uploads')
RESULTS_FOLDER = os.path.join(CWD, 'Vocabanal/static/img/results')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
from Vocabanal import views, routes
