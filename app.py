import io

from flask import Flask, jsonify, request, send_file, abort, redirect, url_for, session
import crud
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim, Yandex

app = Flask(__name__)

CORS(app)

app.config["IMAGE_FOLDER"] = "files/images/"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic'}


cors = CORS(app, resources={r"*": {"origins": "*"}})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return "<h1>Welcome to the Bendermachine187's backend!</h1>" \
           "<h2>Have fun!</h2>"


# User API


@app.get('/users/<user_id>')
def get_user(user_id):
    user = crud.get_user(user_id)
    return jsonify(user)


@app.get('/users/')
def get_users():
    users = crud.get_users()
    return jsonify(users)


@app.post('/users/')
def create_user():
    user = crud.create_user(request.get_json())
    return jsonify(user)


# Report API


@app.get('/reports/<report_id>')
def get_report(report_id):
    user = crud.get_report(report_id)
    return jsonify(user)


@app.get('/reports/')
def get_reports():
    reports = crud.get_reports()
    return jsonify(reports)


@app.post('/reports/')
def create_report():
    print(request.get_json())
    report = crud.create_report(request.get_json())
    return jsonify(report)


@app.post('/like_report/')
def like_report():
    return jsonify(crud.like_report(request.get_json()['report_id']))


@app.route("/images/<path:filename>", methods=["GET"])
def get_image(filename):
    # безопасно соединяем базовый каталог и имя файла
    safe_path = app.config["IMAGE_FOLDER"] + filename
    print(safe_path)
    try:
        return send_file(safe_path, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route("/upload_image", methods=["POST", "PUT"])
def upload_image():
    target = app.config["IMAGE_FOLDER"]
    if not os.path.isdir(target):
        os.mkdir(target)
    # file = list(request.form.items())
    # file = io.BytesIO(bytes(file[0][1].encode()))
    file = request.files['file']
    print(file)
    # f = open(, "wb")
    filename = secure_filename(file.filename)
    destination = "/".join([target, filename])
    file.save(destination)
    session['uploadFilePath'] = destination

    return jsonify({"file_url": url_for('get_image', filename=filename)})


@app.route("/markers/", methods=["GET"])
def get_markers():
    markers = []
    locator = Yandex(api_key="8aeb294a-cc6e-4270-a6b3-8f7cbfe62021", user_agent="BenderMachine187's donoser")
    for item in crud.get_reports():
        location = locator.geocode(item["address"])
        if location is None:
            continue
        # print(location)
        try:
            markers.append({"title": item["title"], "description": item["description"],
                            "latitude": location.latitude, "longitude": location.longitude})
        except AttributeError:
            continue
    return jsonify(markers)


# @app.route("/markers/", methods=["GET"])
# async def get_markers():
#     markers = []
#     async with Nominatim(
#             user_agent="BenderMachine187's donoser",
#             adapter_factory=AioHTTPAdapter,
#     ) as locator:
#         for item in crud.get_reports():
#             location = await locator.geocode(item["address"])
#             if location is None:
#                 continue
#             # print(location)
#             try:
#                 markers.append({"title": item["title"], "description": item["description"],
#                                 "latitude": location.latitude, "longitude": location.longitude})
#             except AttributeError:
#                 continue
#         return jsonify(markers)


if __name__ == '__main__':
    app.secret_key = '77t7bdcbgycdfsyut'
    app.run(host="0.0.0.0", port=5000, debug=True)
