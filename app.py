"""
Flask app to visualize a university scheduling tool.
"""

from dotenv import load_dotenv

load_dotenv()


from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
