from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/test")
def testfunc():
    return jsonify(result="Server called!")

@app.route("/")
def home():
    return render_template("home.html")
    
if __name__ == "__main__":
    app.run(debug=True)