"""
Routes and APIs for the flask application.
"""
import os
import json
from io import BytesIO
from flask import request, flash, redirect, Response
from werkzeug.utils import secure_filename
from Vocabanal import app, nlp, UPLOAD_FOLDER, RESULTS_FOLDER
from Vocabanal.classes.Text import TextPreprocessor
from Vocabanal.modules.data import get_data, normalize_data, kwords_count
from Vocabanal.modules.plot import plot_pos, plot_kwords
from Vocabanal.utils.constants import ALLOWED_EXTENSIONS
from Vocabanal.utils.misc import (
    extract_text, create_nonexistent_dir, save_wordcloud)


@app.route('/api/download')
def download():
    """Send the archive of the produced files"""
    # TODO Call a function to zip the files produced and return the archive
    return "Work in progress"


def allowed_file(filename):
    """
    Validate the filename
    :param filename: str
    :return: bool
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=["POST"])
def upload():
    """Return the files produced"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            app.logger.info("Saving {} to {}".format(filename, filepath))
            file.save(filepath)
            return analyze(filename)
            # return redirect(url_for("analyze", filename=filename))
    else:
        app.logger.error("Something else is wrong")
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''


@app.route('/api/analyze/<filename>', methods=["GET"])
def analyze(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    n_max_words = 15
    with open(filepath, 'rb') as file_in:
        pdf_byte_content = BytesIO(file_in.read())
    corpus = extract_text(pdf_byte_content)
    app.logger.info("Loading spaCy English model. This may take up to 1 minute")
    # nlp = spacy.load("en_core_web_sm")
    app.logger.info("Model loaded")
    doc = nlp(corpus)
    doc_data = get_data(nlp, doc)
    norm_data = normalize_data(doc_data)
    create_nonexistent_dir(RESULTS_FOLDER)
    if len(norm_data["adverbs"]) != 0:
        plot_pos(norm_data["adverbs"], RESULTS_FOLDER, n_max_words, type_pos="Adverbs")
    else:
        app.logger.warning("No adverbs found in the provided PDF")
    if len(norm_data["verbs"]) != 0:
        plot_pos(norm_data["verbs"], RESULTS_FOLDER, n_max_words, type_pos="Verbs")
    else:
        app.logger.warning("No verbs found in the provided PDF")
    if len(norm_data["nouns"]) != 0:
        plot_pos(norm_data["nouns"], RESULTS_FOLDER, n_max_words, type_pos="Nouns")
    else:
        app.logger.warning("No nouns found in the provided PDF")
    if len(norm_data["adjectives"]) != 0:
        plot_pos(norm_data["adjectives"], RESULTS_FOLDER, n_max_words, type_pos="Adjectives")
    else:
        app.logger.warning("No adjectives found in the provided PDF")
    if len(norm_data["entities"]) != 0:
        plot_pos(norm_data["entities"], RESULTS_FOLDER, n_max_words, type_pos="Entities")
        plot_pos(norm_data["entity_types"], RESULTS_FOLDER, n_max_words, type_pos="Entity Types")
    else:
        app.logger.warning("No entities found in the provided PDF")
    save_wordcloud(corpus, RESULTS_FOLDER)
    tp = TextPreprocessor(corpus)
    cleaned_text = tp.preprocess()
    kwords_data = kwords_count(cleaned_text)
    if len(kwords_data) != 0:
        plot_kwords(kwords_data, RESULTS_FOLDER, n_max_words)
    else:
        app.logger.warning("No keywords found in the provided PDF")
    status = {
        "status": "OK",
        "message": "Done with no errors."
    }
    return Response(
        json.dumps(status), status=200)
