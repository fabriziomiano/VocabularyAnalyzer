"""
Routes and APIs for the flask application.
"""
import os
import shutil
import spacy
from io import BytesIO
from uuid import uuid4
from zipfile import ZipFile, ZIP_DEFLATED
from werkzeug.utils import secure_filename
from flask import (
    request, flash, redirect, make_response,
    url_for, jsonify, send_from_directory
)
from pdfminer.pdfparser import PDFSyntaxError
from Vocabanal import app, UPLOAD_FOLDER, RESULTS_FOLDER
from Vocabanal.classes.Text import TextPreprocessor
from Vocabanal.modules.data import get_data, normalize_data, kwords_count
from Vocabanal.modules.plot import plot_pos, plot_kwords
from Vocabanal.utils.constants import ALLOWED_EXTENSIONS
from Vocabanal.utils.misc import (
    extract_text, create_nonexistent_dir, save_wordcloud,
    b64str_from_path
)


def allowed_file(filename):
    """
    Validate the filename
    :param filename: str
    :return: bool
    """
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/upload", methods=["POST"])
def upload():
    """Return the files produced"""
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            request_uuid = uuid4().hex
            updir_path = os.path.join(UPLOAD_FOLDER, request_uuid)
            create_nonexistent_dir(updir_path)
            filename = secure_filename(file.filename)
            filepath = os.path.join(updir_path, filename)
            app.logger.info("Saving {} to {}".format(filename, filepath))
            file.save(filepath)
            return redirect(url_for(
                "analyze", request_uuid=request_uuid, filename=filename)
            )


@app.route("/api/analyze/<request_uuid>, <filename>", methods=["GET"])
def analyze(request_uuid, filename):
    filepath = os.path.join(UPLOAD_FOLDER, request_uuid, filename)
    n_max_words = 15
    try:
        with open(filepath, "rb") as file_in:
            pdf_byte_content = BytesIO(file_in.read())
    except PDFSyntaxError as e:
        return make_response(
            jsonify(status="KO", message=e),
            400)
    corpus = extract_text(pdf_byte_content)
    app.logger.warning("Loading spaCy English model. This may take up to 1 minute")
    nlp = spacy.load("en_core_web_md")
    app.logger.warning("Model loaded")
    doc = nlp(corpus)
    doc_data = get_data(nlp, doc)
    norm_data = normalize_data(doc_data)
    results_dir = os.path.join(RESULTS_FOLDER, request_uuid)
    create_nonexistent_dir(results_dir)
    save_wordcloud(corpus, results_dir)
    for pos in norm_data.keys():
        if len(norm_data[pos]) != 0:
            plot_pos(norm_data[pos], results_dir, n_max_words, type_pos=pos)
    tp = TextPreprocessor(corpus)
    cleaned_text = tp.preprocess()
    kwords_data = kwords_count(cleaned_text)
    if len(kwords_data) != 0:
        plot_kwords(kwords_data, results_dir, n_max_words)
    else:
        app.logger.warning("No keywords found in the provided PDF")
    return redirect(url_for("serve_plots", request_uuid=request_uuid))


@app.route("/api/serve_plots/<request_uuid>", methods=["GET"])
def serve_plots(request_uuid):
    results_dir = os.path.join(RESULTS_FOLDER, request_uuid)
    results = dict()
    for i, plot in enumerate(os.listdir(results_dir)):
        plot_path = os.path.join(results_dir, plot)
        plot_str = b64str_from_path(plot_path)
        if isinstance(plot_str, Exception):
            continue
        else:
            results[i] = plot_str
    return make_response(
        jsonify(uuid=request_uuid, status="OK", results=results), 200)


@app.route("/api/download/<request_uuid>")
def download(request_uuid):
    """
    Send the archive of the produced files
    :param request_uuid: str
    :return: send_from_directory
    """
    results_path = os.path.join(RESULTS_FOLDER, request_uuid)
    zipfile_name = "results.zip"
    zipfile_path = os.path.join(results_path, zipfile_name)
    with ZipFile(zipfile_path, "w", compression=ZIP_DEFLATED) as zipfile_out:
        for filename in os.listdir(results_path):
            if not filename.endswith(".zip"):
                filename_path = os.path.join(results_path, filename)
                zipfile_out.write(
                    filename_path,
                    os.path.basename(filename_path),
                    compress_type=ZIP_DEFLATED)
    return send_from_directory(results_path, zipfile_name, as_attachment=True)


@app.route("/api/delete/<request_uuid>", methods=["POST"])
def delete_data(request_uuid):
    if request.method == "POST":
        dir_paths = [
            os.path.join(UPLOAD_FOLDER, request_uuid),
            os.path.join(RESULTS_FOLDER, request_uuid)
        ]
        for dir_path in dir_paths:
            try:
                shutil.rmtree(dir_path)
            except FileNotFoundError:
                pass
        return jsonify(status="OK", message="removed batch {}".format(request_uuid))
