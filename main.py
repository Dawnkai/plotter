import json
from flask import Flask, redirect, render_template, jsonify, request, make_response, url_for
from database import Database
#from camera import Camera
from logger import setup_logger
import logging

app = Flask(__name__)
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
    response = make_response(img[0])
    response.headers.set('Content-Type', 'image/jpeg')
    return response, 200


@app.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for('static', filename=filename), code=301)


if __name__ == "__main__":
    logger.debug("Setting up the server...")
    setup()
    logger.info("Server ready to work!")
    app.logger.setLevel(logging.INFO)
    app.run(debug=True)
