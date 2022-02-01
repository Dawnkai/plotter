import json
from flask import Flask, redirect, render_template, jsonify, request, url_for, send_file
from werkzeug.utils import secure_filename
from database import Database
#from camera import Camera
from extractor import Extractor
#from plot import Plotter
from logger import setup_logger
import logging
import os

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = 'static/images'

db = Database("data.db")
#cam = Camera()
ext = Extractor()
#plotter = Plotter()
logger = logging.getLogger()

def setup():
    setup_logger()
    db.commit_query('''CREATE TABLE IF NOT EXISTS Status (id INTEGER, state TEXT)''')
    db.commit_query('''CREATE TABLE IF NOT EXISTS Images (date DATE, name TEXT NOT NULL, image BLOB NOT NULL)''')
    db.init_state("Status")


def plot(image):
    plotted = False
    # Create image for plotting
    img = db.retrieve_image("Images", image)
    if img[0]:
        with open('static/plot.jpg', 'wb') as file:
            file.write(img[0])
        # Prevent plot spamming
        db.change_state("Status", "Busy")
        ext.set_filepath('static/plot.jpg')
        # Plot the image
        #plotter.plot(ext.get_contours())
        db.change_state("Status", "Idle")
        plotted = True
    return plotted


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/plot", methods=["GET", "POST"])
def plot_page():
    # GET
    if request.method == "GET":
        return render_template("plot.html")
    
    # POST
    try:
        plotting = db.get_state("Status")
        if plotting == "Idle":
            data = json.loads(request.data.decode("utf-8"))
            exists = db.image_exists(data['image'], 'Images')
            if exists:
                if plot(data['image']):
                    return jsonify({"message": "Image plotted."}), 200
                return jsonify({"message": "Cannot plot imagge."}), 403
            return jsonify({"message": "Image does not exist"}), 404
        else:
            return jsonify({'message': 'Plotter is busy.'}), 403
    except Exception as e:
        logger.error("Error while plotting an image: %s", e)
        return jsonify({"message": "Unable to plot image"}), 403


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


@app.route("/images/<string:name>", methods=["GET", "DELETE"])
def get_image(name):
    if request.method == "GET":
        img = db.retrieve_image("images", name)
        if img[0]:
            with open('static/res.jpg', 'wb') as file:
                file.write(img[0])
        return jsonify({"message": "Image retrieved."}), 200
    # DELETE
    try:
        removed = db.remove_image("images", name)
        if removed:
            return jsonify({"message": "Image removed."}), 200
        return jsonify({"message": "Unable to remove image."}), 403
    except Exception as ex:
        logger.error("Error while removing image %s : %s", name, ex)
        return jsonify({"message": "Unable to remove image."}), 403


@app.route("/display")
def display_image():
    return redirect(url_for('static', filename="res.jpg"), code=301)


@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if 'img-file' not in request.files:
            return jsonify({"message": "No image provided."}), 401
        file = request.files['img-file']
        # If no file is specified, browsers send empty files
        if file == '':
            return jsonify({"message": "No image provided."}), 401
        # Image must have an extension
        if file and '.' in file.filename:
            # Only jpg files are supported
            if "jpg" in file.filename.rsplit('.', 1)[1].lower():
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], "input.jpg"))
                db.store_image(os.path.join(app.config['UPLOAD_FOLDER'], "input.jpg"), "images", file.filename)
                return jsonify({"message": "Image uploaded."}), 200
            else:
                return jsonify({"message": "Image is not a jpg."}), 401
        else:
            return jsonify({"message": "File is not an image."}), 401
    return render_template("upload.html")


@app.route("/stats/status", methods=["GET"])
def get_status():
    try:
        status = db.get_state("Status")
        return jsonify({"message": status}), 200
    except Exception as e:
        logger.error("Error while getting status : %s", e)
        return jsonify({"message": "Error"}), 200


@app.route("/stats/logs", methods=["GET"])
def get_logs():
    try:
        return send_file("plotter.log", as_attachment=True)
    except Exception as e:
        logger.error("Error while sending logs : %s", e)
        return jsonify({"message": "Unable to send logs"}), 403



@app.route("/stats", methods=["GET"])
def get_stats():
    return render_template("stats.html")


if __name__ == "__main__":
    logger.debug("Setting up the server...")
    setup()
    logger.info("Server ready to work!")
    app.logger.setLevel(logging.INFO)
    app.run(debug=True)
