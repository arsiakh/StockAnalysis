# Stock Analysis Project

A Flask-based web application for analyzing stocks using financial ratios and providing investment recommendations.

## Requirements
- Python 3.10+ (Python 3.13 works)
- pip

## Setup + Manual Run

### 1: Clone the repo and enter the project folder
```bash
git clone <YOUR_REPO_URL>
cd StockAnalysis

# Create virtual environment (if not already created)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

**Option B: Manual run**
```bash
# Make sure you're in the project root directory
# Activate virtual environment
source venv/bin/activate

# Navigate to pythonProject and run
cd pythonProject
python main.py
```

### 4. Access the Application

Once the server starts, open your web browser and navigate to:

**http://127.0.0.1:5000** or **http://localhost:5000**

You should see the stock analysis form where you can:
- Enter a stock ticker symbol (e.g., AAPL, MSFT, GOOGL)
- Select a start date
- Select an end date
- Click "Analyze Stock" to get recommendations

## Project Structure

```
StockAnalysis/
├── pythonProject/
│   ├── main.py              # Flask application entry point
│   ├── program1.py          # Backend stock analysis logic
│   ├── templates/           # HTML templates
│   │   ├── index.html
│   │   └── outputPage.html
│   └── static/              # Static files (CSS/images)
│       ├── style.css
│       └── img/             # Generated charts
├── requirements.txt         # Python dependencies
└── README.md

```

## Features

- **Financial Ratio Analysis**: Analyzes 6 key financial ratios:
  - PE Ratio (Price-to-Earnings)
  - EPS (Earnings Per Share)
  - ROE (Return on Equity)
  - Debt-to-Equity Ratio
  - Quick Ratio
  - PEG Ratio (Price/Earnings to Growth)

- **Investment Recommendations**: Provides ratings from 0-100 with investment recommendations
- **Price Charts**: Displays historical stock price charts
- **Modern UI**: Responsive design with modern styling

## Troubleshooting

If you encounter import errors, make sure:
1. You're running from the correct directory
2. PYTHONPATH includes the project root directory
3. Virtual environment is activated
4. All dependencies are installed

## Notes

- The application uses yfinance to fetch real-time stock data
- Some stocks may have incomplete financial data
- The analysis is for educational purposes only
