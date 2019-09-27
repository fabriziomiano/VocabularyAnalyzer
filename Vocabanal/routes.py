"""
Routes and APIs for the flask application.
"""
import os
import shutil
from uuid import uuid4
from zipfile import ZipFile, ZIP_DEFLATED
from werkzeug.utils import secure_filename
from Vocabanal import app, UPLOAD_FOLDER, RESULTS_FOLDER
from Vocabanal.modules.data import analyze
from Vocabanal.utils.misc import create_nonexistent_dir, allowed_file
from flask import (
    request, flash, redirect,
    jsonify, send_from_directory
)


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
            return analyze(request_uuid, filename)


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
