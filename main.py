from flask import Flask, jsonify
from db import get_db_connection

app = Flask(__name__)
conn = get_db_connection()

@app.route("/")
def home():
    cursor = conn.cursor()
    cursor.execute("select count(*) from imoveis;")
    count = cursor.fetchone()[0]
    return jsonify({"message": "API is running", "imoveis_count": count})

if __name__ == "__main__":
    app.run()

