from flask import Flask, redirect, url_for, render_template, request

from program1 import Stocks

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        a = request.form["ticker"]
        b = request.form["start"]
        c = request.form["end"]
        stock = Stocks('', a, b, c)  # passing inputed variables, ticker, start, end
        stock.setvalueTicker()
        stock.ratio1('')
        stock.ratio2('')  # calling each method, to be able to run with inputs and get variables to output
        stock.ratio3('')
        stock.ratio4('')
        stock.ratio5('')
        stock.ratio6('')
        stock.ratio6('')
        stock.finalRating()
        stock.investmentRecommendation()
        stock.finalExplanation()
        stock.tickerGraph()
        return redirect(url_for("output", rating=stock.finalRating(), recommendation=stock.investmentRecommendation(),
                                explanation=stock.finalExplanation()))  # redirecting variables to output page
    else:
        return render_template("index.html")


@app.route("/<rating>/<recommendation>/<explanation>")  # passing variables to output page
def output(rating, recommendation, explanation):
    list1 = eval(explanation)  # turning str object of list to an actual list object
    list2 = len(list1)
    list3 = list2 // 2
    list4 = list1[
            :list3]  # getting half of list, as original explanation variable repeated the values in the list twice

    return render_template("outputPage.html", rating=rating, recommendation=recommendation,
                           explanation=list4)  # renders new page with variables needed


if __name__ == "__main__":
    app.run(debug=True)
