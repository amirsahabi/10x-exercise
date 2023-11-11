from flask import Flask, jsonify, request
import database
from datetime import date


app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(database.get_all())


@app.route("/query")
def query():
    # Verify inputs
    if request.args.get("limit") is not None and not request.args.get("limit").isnumeric():
        return "Invalid limit", 400
    elif request.args.get("date") is not None:
        try:
            # just try the conversion to see if it is of valid format
            date.fromisoformat(request.args.get('date'))
        except:
            return "Invalid date, expected ISO format", 400

    return jsonify(
        database.get_by_parameters(
            request.args.get("date"),
            request.args.get("weather"),
            request.args.get("limit"),
        )
    )


# For development ONLY
# Sample production command: python3 -m gunicorn -w 4 app:app --config gunicorn.config.py
if __name__ == "__main__":
    database.init()
    app.run("0.0.0.0", 8000, debug=True)
