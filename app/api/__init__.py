"""
APIs definition
"""
import os
import shutil
from uuid import uuid4
from zipfile import ZipFile, ZIP_DEFLATED

from flask import Blueprint
from flask import current_app as app
from flask import (
    request, flash, redirect, jsonify, send_from_directory, make_response
)
from werkzeug.utils import secure_filename

from app.modules.data import analyze
from app.utils.misc import create_nonexistent_dir, allowed_file

api = Blueprint('api', __name__, url_prefix='/api')


@api.post("/upload")
def upload():
    """Upload a file to the server and call the anlyze function"""
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
            updir_path = os.path.join(app.config["UPLOAD_FOLDER"],
                                      request_uuid)
            create_nonexistent_dir(updir_path)
            filename = secure_filename(file.filename)
            filepath = os.path.join(updir_path, filename)
            app.logger.debug("Saving {} to {}".format(filename, filepath))
            file.save(filepath)
            return analyze(request_uuid, filename)


@api.get("/download/<request_uuid>")
def download(request_uuid):
    """
    Send the archive containing the produced files
    :param request_uuid: str
    :return: send_from_directory
    """
    results_path = os.path.join(app.config["RESULTS_FOLDER"], request_uuid)
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


@api.post("/api/delete/<request_uuid>")
def delete_data(request_uuid):
    """
    Delete the data for a given request_uuid
    :param request_uuid: str
    :return: JSON object
    """
    if request.method == "POST":
        dir_paths = [
            os.path.join(app.config["UPLOAD_FOLDER"], request_uuid),
            os.path.join(app.config["RESULTS_FOLDER"], request_uuid)
        ]
        for dir_path in dir_paths:
            try:
                shutil.rmtree(dir_path)
            except FileNotFoundError:
                pass
        message = "removed batch {}".format(request_uuid)
        return make_response(jsonify(status="OK", message=message), 200)
