import firebase_admin
from firebase_admin import firestore, credentials
from flask import Flask, request, render_template, jsonify

cred = credentials.Certificate("creds.json")

firebase_admin.initialize_app(cred)

db_client = firestore.client()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    try:
        p = db_client.collection("data").document("potentiometer").get().to_dict()
        value = p["value"]

        return render_template("index.html", value=value)
    except Exception as e:
        print(e)
        return jsonify({"status": "failed"}), 400


def add():
    try:
        value = request.json.get("potentiometer")

        db_client.collection("data").document("potentiometer").set({"value": value})

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(e)
        return jsonify({"status": "failed"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
