import json
from flask import Flask, redirect, render_template, jsonify, request, url_for
from werkzeug.utils import secure_filename
from database import Database
#from camera import Camera
from logger import setup_logger
import logging
import os

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = 'static/images'

db = Database("data.db")
#cam = Camera()
logger = logging.getLogger()

def setup():
    setup_logger()
    db.commit_query('''CREATE TABLE IF NOT EXISTS Status (id INTEGER, state TEXT)''')
    db.init_state("Status")


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/plot", methods=["GET", "POST"])
def plot_page():
    # GET
    if request.method == "GET":
        return render_template("plot.html")
    
    # POST
    plotting = db.get_state("Status")
    if plotting == "Idle":
        db.change_state("Status", "Busy")
        # TODO : Plot
        db.change_state("Status", "Idle")
        return jsonify(result="Plotting finished.")
    else:
        resp = jsonify({'message': 'Plotter is busy.'})
        return resp, 403


@app.route("/camera", methods=["GET", "POST"])
def take_picture():
    # GET
    if request.method == "GET":
        return render_template("camera.html")

    # POST
    else:
        try:
            #cam.take_picture()
            return jsonify({'message': 'Picture taken successfully.'}), 201
        except Exception as e:
            logger.error("Error while taking a picture: %s", e)
            return jsonify({'message': 'Problem with camera'}), 403


@app.route("/images", methods=["GET", "POST"])
def images():
    if request.method == "GET":
        return render_template("images.html")
    else:
        try:
            return jsonify({'images': db.get_images("images")}), 200
        except KeyError:
            return jsonify({'message': 'Request in incorrect format'}), 401


@app.route("/images/<string:name>", methods=["GET"])
def get_image(name):
    img = db.retrieve_image("images", name)
    if img[0]:
        with open('static/res.jpg', 'wb') as file:
            file.write(img[0])
    return jsonify({"message": "Image retrieved."}), 200


@app.route("/display")
def display_image():
    return redirect(url_for('static', filename="res.jpg"), code=301)


@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if 'img-file' not in request.files:
            return jsonify({"message": "No image provided."}), 401
        file = request.files['img-file']
        if file == '':
            return jsonify({"message": "No image provided."}), 401
        if file and '.' in file.filename:
            if "jpg" in file.filename.rsplit('.', 1)[1].lower():
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], "input.jpg"))
                db.store_image(os.path.join(app.config['UPLOAD_FOLDER'], "input.jpg"), "images", file.filename)
                return jsonify({"message": "Image uploaded."}), 200
            else:
                return jsonify({"message": "Image is not a jpg."}), 401
        else:
            return jsonify({"message": "File is not an image."}), 401
    return render_template("upload.html")


if __name__ == "__main__":
    logger.debug("Setting up the server...")
    setup()
    logger.info("Server ready to work!")
    app.logger.setLevel(logging.INFO)
    app.run(debug=True)
