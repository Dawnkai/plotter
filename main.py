from flask import Flask, render_template, jsonify, request
from database import Database
from logger import setup_logger
import logging

app = Flask(__name__)
db = Database("data.db")
logger = logging.getLogger()

def setup():
    setup_logger()
    db.commit_query('''CREATE TABLE IF NOT EXISTS Status (id INTEGER, state TEXT)''')
    db.init_state("Status")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/plot", methods=["GET", "POST"])
def plot_page():
    if request.method == "GET":
        return render_template("plot.html")
    elif request.method == "POST":
        plotting = db.get_state("Status")
        if plotting == "Idle":
            db.change_state("Status", "Busy")
            # TODO : Plot
            db.change_state("Status", "Idle")
            return jsonify(result="Plotting finished.")
        else:
            resp = jsonify({'message': 'Plotter is busy.'})
            return resp, 403


if __name__ == "__main__":
    logger.debug("Setting up the server...")
    setup()
    logger.info("Server ready to work!")
    app.logger.setLevel(logging.INFO)
    app.run(debug=True)
