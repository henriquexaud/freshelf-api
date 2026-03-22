import os

from flask import Flask, jsonify
from flask_cors import CORS
from database import init_db
from routes import bp as produtos_bp
from swagger import bp as docs_bp

app = Flask(__name__)
CORS(app)

init_db()
app.register_blueprint(produtos_bp)
app.register_blueprint(docs_bp)


@app.get("/health")
def health_check():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1", host="127.0.0.1", port=5001)
