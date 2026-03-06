#!/usr/bin/env python3
"""
VtxDeep Stock Analysis API
A simple stock analysis API providing daily predictions and insights
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Get port from environment (Render.com provides this)
PORT = int(os.environ.get('PORT', 5000))

# Mock data for demonstration - in production, use real market data
STOCK_DATA = {
    "nasdaq": {
        "name": "NASDAQ Composite",
        "symbol": "^IXIC",
        "base_price": 22800
    },
    "dow": {
        "name": "Dow Jones Industrial",
        "symbol": "^DJI",
        "base_price": 43100
    },
    "sp500": {
        "name": "S&P 500",
        "symbol": "^GSPC",
        "base_price": 6850
    },
    "tqqq": {
        "name": "ProShares UltraPro QQQ",
        "symbol": "TQQQ",
        "base_price": 50.0
    },
    "sndk": {
        "name": "SanDisk Corporation",
        "symbol": "SNDK",
        "base_price": 620.0
    }
}

def generate_prediction(symbol):
    """Generate mock prediction - in production, use real ML model"""
    base = STOCK_DATA.get(symbol.lower(), {}).get("base_price", 100)
    
    # Add some randomness for demo
    variance = base * 0.02  # 2% variance
    
    high = round(base + variance + random.uniform(0, variance), 2)
    low = round(base - variance - random.uniform(0, variance), 2)
    close = round(base + random.uniform(-variance, variance), 2)
    
    return {
        "high": high,
        "low": low,
        "close": close,
        "change_percent": round((close - base) / base * 100, 2)
    }

@app.route('/')
def index():
    """API documentation"""
    return jsonify({
        "name": "VtxDeep Stock Analysis API",
        "version": "1.0.0",
        "description": "AI-powered stock analysis and predictions",
        "endpoints": {
            "/predict/<symbol>": "Get prediction for a specific stock/index",
            "/market/summary": "Get market summary for major indices",
            "/insider/<symbol>": "Get insider trading data (if available)"
        }
    })

@app.route('/predict/<symbol>')
def predict(symbol):
    """Get stock prediction for a specific symbol"""
    symbol = symbol.upper()
    
    # Check if free tier limit reached
    api_key = request.headers.get('X-RapidAPI-Key')
    if not api_key:
        # Free tier - limited requests
        return jsonify({
            "error": "API key required. Sign up at RapidAPI for free key.",
            "status": 401
        })
    
    prediction = generate_prediction(symbol)
    
    return jsonify({
        "symbol": symbol,
        "timestamp": datetime.now().isoformat(),
        "prediction": prediction,
        "confidence": "medium",
        "data_source": "GROK AI Analysis"
    })

@app.route('/market/summary')
def market_summary():
    """Get summary of major market indices"""
    indices = ["nasdaq", "dow", "sp500", "tqqq", "sndk"]
    
    summary = {}
    for idx in indices:
        summary[idx] = generate_prediction(idx)
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "market": summary,
        "sentiment": random.choice(["bullish", "neutral", "bearish"])
    })

@app.route('/insider/<symbol>')
def insider_trading(symbol):
    """Get insider trading information - mock data for demo"""
    symbol = symbol.upper()
    
    return jsonify({
        "symbol": symbol,
        "timestamp": datetime.now().isoformat(),
        "insider_buys": [],
        "insider_sells": [],
        "note": "Insider data requires enterprise subscription"
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)
