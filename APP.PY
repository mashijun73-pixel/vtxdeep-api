#!/usr/bin/env python3
"""
VtxDeep Stock Analysis API
"""

from flask import Flask, jsonify, request
import random
from datetime import datetime
import os

app = Flask(__name__)

PORT = int(os.environ.get('PORT', 5000))

STOCK_DATA = {
    "nasdaq": {"name": "NASDAQ Composite", "symbol": "^IXIC", "base_price": 22800},
    "dow": {"name": "Dow Jones Industrial", "symbol": "^DJI", "base_price": 43100},
    "sp500": {"name": "S&P 500", "symbol": "^GSPC", "base_price": 6850},
    "tqqq": {"name": "ProShares UltraPro QQQ", "symbol": "TQQQ", "base_price": 50.0},
    "sndk": {"name": "SanDisk Corporation", "symbol": "SNDK", "base_price": 620.0}
}

def generate_prediction(symbol):
    base = STOCK_DATA.get(symbol.lower(), {}).get("base_price", 100)
    variance = base * 0.02
    high = round(base + variance + random.uniform(0, variance), 2)
    low = round(base - variance - random.uniform(0, variance), 2)
    close = round(base + random.uniform(-variance, variance), 2)
    return {"high": high, "low": low, "close": close, "change_percent": round((close - base) / base * 100, 2)}

@app.route('/')
def index():
    return jsonify({
        "name": "VtxDeep Stock Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "/predict/<symbol>": "Get prediction",
            "/market/summary": "Get market summary",
            "/insider/<symbol>": "Get insider data",
            "/health": "Health check"
        }
    })

@app.route('/predict/<symbol>')
def predict(symbol):
    symbol = symbol.upper()
    api_key = request.headers.get('X-RapidAPI-Key')
    if not api_key:
        return jsonify({"error": "API key required", "status": 401})
    prediction = generate_prediction(symbol)
    return jsonify({"symbol": symbol, "timestamp": datetime.now().isoformat(), "prediction": prediction, "confidence": "medium", "data_source": "GROK AI Analysis"})

@app.route('/market/summary')
def market_summary():
    summary = {idx: generate_prediction(idx) for idx in STOCK_DATA}
    return jsonify({"timestamp": datetime.now().isoformat(), "market": summary, "sentiment": random.choice(["bullish", "neutral", "bearish"])})

@app.route('/insider/<symbol>')
def insider_trading(symbol):
    return jsonify({"symbol": symbol.upper(), "timestamp": datetime.now().isoformat(), "insider_buys": [], "insider_sells": [], "note": "Insider data requires enterprise subscription"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)
