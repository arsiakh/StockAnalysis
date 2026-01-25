from flask import Flask, redirect, url_for, render_template, request, session, flash
import json
from datetime import datetime, date

from program1 import Stocks

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Change this in production


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        try:
            a = request.form.get("ticker", "").strip().upper()
            b = request.form.get("start", "").strip()
            c = request.form.get("end", "").strip()
            
            # Input validation
            if not a:
                flash("Please enter a ticker symbol.", "error")
                return render_template("index.html")
            if not b or not c:
                flash("Please enter both start and end dates.", "error")
                return render_template("index.html")
            
            # Date validation
            try:
                start_date = datetime.strptime(b, "%Y-%m-%d").date()
                end_date = datetime.strptime(c, "%Y-%m-%d").date()
            except ValueError:
                flash("Invalid date format. Please use YYYY-MM-DD format.", "error")
                return render_template("index.html")
            
            if end_date <= start_date:
                flash("End date must be after start date.", "error")
                return render_template("index.html")
            
            if start_date > date.today():
                flash("Start date cannot be in the future.", "error")
                return render_template("index.html")
            
            if end_date > date.today():
                flash("End date cannot be in the future. Using today's date instead.", "warning")
                c = date.today().strftime("%Y-%m-%d")
            
            stock = Stocks('', a, b, c)  # passing inputed variables, ticker, start, end
            stock.setvalueTicker()
            stock.ratio1()  # Let methods fetch data from yfinance
            stock.ratio2()
            stock.ratio3()
            stock.ratio4()
            stock.ratio5()
            stock.ratio6()
            stock.finalRating()
            stock.investmentRecommendation()
            stock.finalExplanation()
            stock.tickerGraph("pythonProject/static/img/pic.png")
            
            # Store data in session instead of URL parameters
            session['rating'] = stock.finalRating()
            session['recommendation'] = stock.investmentRecommendation()
            session['explanation'] = json.dumps(stock.finalExplanation())
            
            return redirect(url_for("output"))  # redirecting to output page
        except ValueError as e:
            flash(f"Error: {str(e)}", "error")
            return render_template("index.html")
        except KeyError as e:
            flash(f"Missing data for this stock. Some financial metrics may not be available.", "error")
            return render_template("index.html")
        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}", "error")
            return render_template("index.html")
    else:
        return render_template("index.html")


@app.route("/output")  # output page route
def output():
    # Retrieve data from session
    rating = session.get('rating', 'N/A')
    recommendation = session.get('recommendation', 'N/A')
    explanation_json = session.get('explanation', '[]')
    
    try:
        explanation = json.loads(explanation_json)
    except (json.JSONDecodeError, TypeError):
        explanation = []
    
    # Remove duplicates if they exist (legacy fix)
    if len(explanation) > 0:
        # Remove duplicates while preserving order
        seen = set()
        explanation = [x for x in explanation if not (x in seen or seen.add(x))]
    
    return render_template("outputPage.html", rating=rating, recommendation=recommendation,
                           explanation=explanation)  # renders new page with variables needed


if __name__ == "__main__":
    app.run(debug=True)
