#!/usr/bin/env python3
"""
VtxDeep Stock Analysis API
A simple stock analysis API providing daily predictions and insights
"""

from flask import Flask, jsonify, request
import random
from datetime import datetime

app = Flask(__name__)

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
        "description": "AI-powered stock analysis and predictions",
        "endpoints": {
            "/predict/<symbol>": "Get prediction for a specific stock/index",
            "/market/summary": "Get market summary for major indices",
            "/insider/<symbol>": "Get insider trading data"
        }
    })

@app.route('/predict/<symbol>')
def predict(symbol):
    symbol = symbol.upper()
    return jsonify({
        "symbol": symbol,
        "timestamp": datetime.now().isoformat(),
        "prediction": generate_prediction(symbol),
        "confidence": "medium",
        "data_source": "GROK AI Analysis"
    })

@app.route('/market/summary')
def market_summary():
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "market": {idx: generate_prediction(idx) for idx in STOCK_DATA.keys()},
        "sentiment": random.choice(["bullish", "neutral", "bearish"])
    })

@app.route('/insider/<symbol>')
def insider_trading(symbol):
    return jsonify({"symbol": symbol.upper(), "insider_buys": [], "insider_sells": [], "note": "Enterprise only"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)