from flask import Flask, request, jsonify
from utils.fetch_api import fetch_arxiv
from flask_cors import CORS
import sqlite3
import os


app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

DB_PATH = os.getenv('DATABASE_URL', 'sqlite:///papers.db').replace('sqlite:///', '')

def init_db():
    conn = sqlite3.connect('papers.db')
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.close()

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route('/api/search')
def search():
    query = request.args.get("q", "")
    papers = fetch_arxiv(query, max_results=5)
    return jsonify({"papers": papers})


@app.route('/')
def home():
    return {
        "message": "Welcome to the Research Paper Recommender API 👋",
        "arxiv_base": os.getenv("ARXIV_BASE")
    }

if __name__ == "__main__":
    app.run(debug=True)