# Stock Analysis Project

A Flask-based web application for analyzing stocks using financial ratios and providing investment recommendations.

## Requirements
- Python 3.10+
- pip

## Setup

### 1. Clone the repo and enter the project folder
```bash
git clone <YOUR_REPO_URL>
cd StockAnalysis
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python3 pythonProject/main.py
```

### 5. Open in your browser

**http://127.0.0.1:5000**

You can:
- Enter a stock ticker symbol (e.g., AAPL, MSFT, GOOGL)
- Select a start and end date
- Click "Analyze Stock" to get a recommendation and price chart

## Running Tests

Tests are written with `pytest` and cover the `Stocks` class and all Flask routes.

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run all tests with coverage report
python3 -m pytest -v --tb=short --cov=pythonProject --cov-report=term-missing
```

To run specific test files:
```bash
# Stocks class logic only
python3 -m pytest pythonProject/test_program1.py -v

# Flask routes only
python3 -m pytest pythonProject/test_main.py -v
```

To generate an HTML coverage report:
```bash
python3 -m pytest --cov=pythonProject --cov-report=html
# Then open htmlcov/index.html in your browser
```

## Project Structure

```
StockAnalysis/
├── pythonProject/
│   ├── main.py                # Flask application entry point
│   ├── program1.py            # Stock analysis logic (Stocks class)
│   ├── test_program1.py       # Unit tests for Stocks class
│   ├── test_main.py           # Unit tests for Flask routes
│   ├── templates/
│   │   ├── index.html         # Input form page
│   │   └── outputPage.html    # Results page
│   └── static/
│       ├── style.css          # Stylesheet
│       └── img/               # Generated chart (created at runtime)
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
├── .gitignore
└── README.md
```

## Features

- **Financial Ratio Analysis** — analyzes 6 key financial ratios:
  - PE Ratio (Price-to-Earnings)
  - EPS (Earnings Per Share)
  - ROE (Return on Equity)
  - Debt-to-Equity Ratio
  - Quick Ratio
  - PEG Ratio (Price/Earnings to Growth)

- **Investment Recommendations** — 0–100 rating with one of:
  - Strongly Don't Recommend
  - Don't Recommend
  - Neutral
  - Recommend
  - Strongly Recommend

- **Price Charts** — historical closing price chart for your selected date range
- **Modern UI** — responsive side-by-side layout

## Troubleshooting

- Make sure your virtual environment is activated (`source .venv/bin/activate`) before running the app or tests
- If a stock has missing financial data, some ratios will be skipped and the rating will reflect only the available data
- The app runs in debug mode by default — do not use this in production

## Notes

- Stock data is fetched live from Yahoo Finance via `yfinance`
- This application is for educational purposes only and is not financial advice
