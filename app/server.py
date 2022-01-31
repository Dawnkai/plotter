from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

def get_status(dbname):
    conn = None
    result = ""
    try:
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        cur.execute("SELECT * FROM CurStatus")
        rows = cur.fetchall()
        result = rows[0][1]
    except sqlite3.Error as e:
        print(f"Error while fetching status: {e}")
        result = "Error"
    finally:
        if conn is not None:
            conn.close()
        return result


def change_status(dbname, new_status):
    conn = None
    try:
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        cur.execute(f"UPDATE CurStatus SET status = '{new_status}' WHERE id = 1")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error while changing status: {e}")
    finally:
        if conn is not None:
            conn.close()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/plot", methods=["GET", "POST"])
def plot_page():
    if request.method == "GET":
        return render_template("plot.html")
    elif request.method == "POST":
        plotting = get_status("data.db")
        if plotting == "Idle":
            change_status("data.db", "Busy")
            # TODO : Plot
            change_status("data.db", "Idle")
            return jsonify(result="Plotting finished.")
        else:
            resp = jsonify({'message': 'Plotter is busy.'})
            return resp, 403


if __name__ == "__main__":
    app.run(debug=True)
