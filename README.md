# VtxDeep Stock Analysis API

AI-powered stock analysis API providing daily predictions and market insights.

## Endpoints

- GET / - API documentation
- GET /predict/<symbol> - Stock prediction
- GET /market/summary - Market summary
- GET /insider/<symbol> - Insider data
- GET /health - Health check

## Deploy

1. Connect to Render.com
2. Build: pip install -r requirements.txt
3. Start: gunicorn app:app

## Pricing

- Free: 100 req/month
- Basic: \$9.99/month

- Pro: \$29.99/month
- gunicorn -w 4 app:app --bind 0.0.0.0:$PORT
