from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

SYMBOL_MAP = {
    "nifty": {
        "exchange": "NSE",
        "symbol": "NIFTY"
    },
    "sensex": {
        "exchange": "BSE",
        "symbol": "1"
    }
}

def get_time_range(days=7):
    end_time = int(time.time() * 1000)
    start_time = end_time - (days * 24 * 60 * 60 * 1000)
    return start_time, end_time

@app.route("/chart", methods=["GET"])
def get_chart():
    query = request.args.get("symbol", "").lower()

    if query not in SYMBOL_MAP:
        return jsonify({
            "error": "Invalid symbol. Use 'nifty' or 'sensex'"
        }), 400

    config = SYMBOL_MAP[query]
    start_time, end_time = get_time_range()

    url = f"https://groww.in/v1/api/charting_service/v2/chart/delayed/exchange/{config['exchange']}/segment/CASH/{config['symbol']}"

    params = {
        "startTimeInMillis": start_time,
        "endTimeInMillis": end_time,
        "intervalInMinutes": 5
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "x-app-id": "growwWeb",
        "x-device-type": "charts",
        "x-platform": "web"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        return jsonify({
            "status": "success",
            "symbol": query,
            "data": response.json()
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/")
def home():
    return jsonify({
        "message": "Groww Chart API Wrapper",
        "usage": "/chart?symbol=nifty or sensex"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
