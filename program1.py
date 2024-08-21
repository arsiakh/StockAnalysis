import yfinance as yf

import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8')


class Stocks:
    def __init__(self, history, ticker, start,
                 end):  # variables ticker, start and end found from user input in html form
        self.emptyDict = {}
        self.__rating = 0
        self.history1 = history
        self.__dictValues = []
        self.dictExplain = []
        self.rec = 0
        self.explain = None
        self.__ticker = ticker
        self.__start = start
        self.__end = end

    def getTicker(self):
        return self.__ticker

    def getStart(self):
        return self.__start

    def getEnd(self):
        return self.__end

    def getRating(self):
        return self.__rating

    def getdictValues(self):
        return self.__dictValues

    def setvalueTicker(self):
        self.__ticker = yf.Ticker(self.__ticker)  # setting the ticker based off user input
        return self.__ticker

    # emptyDict = {}
    def ratio1(self, ratioPE):
        for key in self.__ticker.info:
            if 'trailingPE' not in self.__ticker.info:
                self.ratioPE = self.__ticker.info[
                    'forwardPE']  # checks if trailingPE can be returned, if not it uses the forwardPE number
            else:
                self.ratioPE = self.__ticker.info['trailingPE']
        if 20 <= self.ratioPE <= 25:
            self.emptyDict[
                "a"] = "The PE ratio is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. PE stands for The price-earnings ratio. It’s the company's share price to the company's earnings per share. The ratio is used for valuing companies and to find out whether they are overvalued or undervalued. Your stock scored between 20 and 25 this means that your stocks PE ratio would be considered ok not bad not good it means that the company is not struggling when it comes to their PE ratio. This PE ratio would be considered a safe PE ratio."  # assigns the reasoning for the value that would be given from PE ratio
            self.__rating += (4 * .375)  # gives unique rating based on value of PE ratio
            return self.emptyDict
        elif 10 <= self.ratioPE <= 19:
            self.emptyDict[
                "a1"] = "The PE ratio is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. PE stands for The price-earnings ratio. It’s the company's share price to the company's earnings per share. The ratio is used for valuing companies and to find out whether they are overvalued or undervalued. Your stock scored between 10 and 19this means that your stocks PE ratio would be considered good. It means that the company is doing a good job when it comes to their PE ratio. This PE ratio would be considered a good PE ratio."
            self.__rating += (7 * .375)
            return self.emptyDict
        elif 0 <= self.ratioPE <= 9.9:
            self.emptyDict[
                'a2'] = "The PE ratio is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. PE stands for The price-earnings ratio. It’s the company's share price to the company's earnings per share. The ratio is used for valuing companies and to find out whether they are overvalued or undervalued. Your stock scored between 0 and 9.9 this means that your stocks PE ratio would be considered amazing. It means that the company is doing exceptionally well when it comes to their PE ratio. This PE ratio would be considered a very good ratio."
            self.__rating += (10 * .375)
            return self.emptyDict
        else:
            return self.emptyDict

    def ratio2(self, ratioEPS):
        self.ratioEPS = self.__ticker.info['trailingEps']
        if 0.8 <= self.ratioEPS <= 1.5:
            self.emptyDict[
                'b'] = "Eps is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. Eps stand for earnings per share. The Eps ratio shows the investor how much profit per share the company is making. It helps investors find out whether they are overvalued or undervalued. Your stock scored between 0.8 and 1.5 this means that your stock's Eps ratio would be considered ok not bad not good it means that the company is not struggling when it comes to their Eps ratio. This Eps ratio would be considered a safe Eps ratio."
            self.__rating += (4 * .25)
            return self.emptyDict
        elif 1.6 <= self.ratioEPS <= 5:
            self.emptyDict[
                'b1'] = "Eps is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. Eps stand for earnings per share. The Eps ratio shows the investor how much profit per share the company is making. It helps investors find out whether they are overvalued or undervalued. Your stock scored between 1.6 and 5 this means that your stocks Epsratio would be considered good. It means that the company is doing a good job when it comes to their Eps ratio. This Eps Ratio would be considered a good Eps ratio."
            self.__rating += (7 * .25)
            return self.emptyDict
        elif self.ratioEPS >= 5.1:
            self.emptyDict[
                'b2'] = "Eps is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. Eps stand for earnings per share. The Eps ratio shows the investor how much profit per share the company is making. It helps investors find out whether they are overvalued or undervalued. Your stock scored greater than 5.1 this means that your stocks Epsratio would be considered amazing. It means that the company is doing exceptionally well when it comes to their Eps ratio. This Eps ratio would be considered a very good ratio."
            self.__rating += (10 * .25)
            return self.emptyDict
        else:
            return self.emptyDict

    def ratio3(self, ratioROE):
        self.ratioROE = self.__ticker.info['returnOnEquity']
        self.ratioROE = self.ratioROE * 100
        if 15 <= self.ratioROE <= 20:
            self.emptyDict[
                'c'] = "Roe is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. Roe stands for return on equity. The return on equity is a measure of the profitability of a business in relation to the equity.ROE can also be thought of as a return on assets minus liabilities. Roe helps investors understand how much return the business is getting based on how much money the business puts in. Your stock scored between 15 and 20 this means that your stock's roe ratio would be considered ok not bad not good it means that the company is not struggling when it comes to their roe ratio. This roe ratio would be considered a safe roe ratio. "
            self.__rating += (4 * 0.5)
            return self.emptyDict
        elif 21 <= self.ratioROE <= 100:
            self.emptyDict[
                'c1'] = "Roe is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. Roe stands for return on equity. The return on equity is a measure of the profitability of a business in relation to the equity.ROE can also be thought of as a return on assets minus liabilities. Roe helps investors understand how much return the business is getting based on how much money the business puts in. Your stock scored between 21 and 100 this means that your stocks Roe ratio would be considered good. It means that the company is doing a good job when it comes to their roe ratio. This roe Ratio would be considered a good roe ratio."
            self.__rating += (7 * 0.5)
            return self.emptyDict
        elif self.ratioROE >= 101:
            self.emptyDict[
                'c2'] = "Roe is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. Roe stands for return on equity. The return on equity is a measure of the profitability of a business in relation to the equity.ROE can also be thought of as a return on assets minus liabilities. Roe helps investors understand how much return the business is getting based on how much money the business puts in. Your stock scored greater than 101 this means that your stocks Roe ratio would be considered amazing. It means that the company is doing exceptionally well when it comes to their Roe ratio. This Roe ratio would be considered a very good ratio."
            self.__rating += (10 * 0.5)
            return self.emptyDict
        else:
            return self.emptyDict

    def ratio4(self, debt_equity):
        self.debt_equity = self.__ticker.info['debtToEquity']
        if 0 <= self.debt_equity <= 50:
            self.emptyDict[
                'd2'] = "Debt to equity ratio is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. The debt-to-equity ratio compares a company's total liabilities to its shareholder equity and can be used to evaluate how much leverage a company is using. This helps investors to understand how risky the investment is based on how leveraged the company is. Your stock scored between 0 and 50 this means that your stocks Debt to equity ratio would be considered amazing. It means that the company is doing exceptionally well when it comes to their Debt to equity ratio. This Debt to equity ratio would be considered a very good ratio."
            self.__rating += (10 * 1)
            return self.emptyDict
        elif 51 <= self.debt_equity <= 99:
            self.emptyDict[
                'd1'] = "Debt to equity ratio is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. The debt-to-equity ratio compares a company's total liabilities to its shareholder equity and can be used to evaluate how much leverage a company is using. This helps investors to understand how risky the investment is based on how leveraged the company is. Your stock scored between 51 and 99 this means that your stocks Debt to equity ratio would be considered good. It means that the company is doing a good job when it comes to their Debt to equity ratio. This Debt to equity Ratio would be considered a good ratio."
            self.__rating += (7 * 1)
            return self.emptyDict
        elif 100 <= self.debt_equity <= 250:
            self.emptyDict[
                'd'] = "Debt to equity ratio is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. The debt-to-equity ratio compares a company's total liabilities to its shareholder equity and can be used to evaluate how much leverage a company is using. This helps investors to understand how risky the investment is based on how leveraged the company is. Your stock scored between 100 and 250 this means that your stock's Debt to equity ratio would be considered ok not bad not good it means that the company is not struggling when it comes to their Debt to equity ratio. This Debt to equity ratio would be considered a safe ratio."
            self.__rating += (4 * 1)
            return self.emptyDict
        else:
            return self.emptyDict

    def ratio5(self, quick):
        self.quick = self.__ticker.info['quickRatio']
        if 1 <= self.quick <= 2:
            self.emptyDict[
                'e'] = "Quick ratio is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. The quick ratio indicates your company's ability to meet creditors' immediate demands using its most liquid and current assets. This lets investors know how easy it is for the company to pay off its debts to creditors. This also lets the investors know how easy it is for the company to borrow money. Your stock scored between 1 and 2 this means that your stock's quick ratio would be considered ok, not bad not good it means that the company is not struggling when it comes to their quick ratio. This quick ratio would be considered a safe quick ratio."
            self.__rating += (4 * .75)
            return self.emptyDict
        elif 2.1 <= self.quick <= 4:
            self.emptyDict[
                'e1'] = "Quick ratio is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. The quick ratio indicates your company's ability to meet creditors' immediate demands using its most liquid and current assets. This lets investors know how easy it is for the company to pay off its debts to creditors. This also lets the investors know how easy it is for the company to borrow money. Your stock scored between 2.1 and 4 this means that your stocks quick ratio would be considered good. It means that the company is doing a good job when it comes to their quick ratio. This quick ratio would be considered a good quick ratio."
            self.__rating += (7 * .75)
            return self.emptyDict
        elif self.quick >= 4.1:
            self.emptyDict[
                'e2'] = "Quick ratio is a financial ratio that helps investors get a better understanding of how well the company and stock is doing. The quick ratio indicates your company's ability to meet creditors' immediate demands using its most liquid and current assets. This lets investors know how easy it is for the company to pay off its debts to creditors. This also lets the investors know how easy it is for the company to borrow money. Your stock scored greater than 4.1 this means that your stocks Quick ratio would be considered amazing. It means that the company is doing exceptionally well when it comes to their quick ratio. This Quick ratio would be considered a very good ratio."
            self.__rating += (10 * .75)
            return self.emptyDict
        else:
            return self.emptyDict

    def ratio6(self, ratioPEG):
        self.ratioPEG = self.__ticker.info['pegRatio']
        if 1.5 <= self.ratioPEG <= 2:
            self.emptyDict[
                "f"] = "PEG ratio is a financial ratio that helps investors get a better understanding of how well the company and stock is doing.PEG stands for price earning ratio. The PEG ratio is a valuation metric for determining the relative trade-off between the price of a stock, the earnings generated per share, and the company's expected growth this helps inventors understand how much the stock is going to grow. Your stock scored between 1.5 and 2 this means that your stock's PEG ratio would be considered ok, not bad not good it means that the company is not struggling when it comes to their PEG ratio  This PEG ratio would be considered a safe PEG ratio."
            self.__rating += (4 * 0.5)
            return self.emptyDict
        elif 1.1 <= self.ratioPEG <= 1.49:
            self.emptyDict[
                'f1'] = "PEG ratio is a financial ratio that helps investors get a better understanding of how well the company and stock is doing.PEG stands for price earning ratio.The PEG ratio is a valuation metric for determining the relative trade-off between the price of a stock, the earnings generated per share, and the company's expected growth this helps inventors understand how much the stock is going to grow. Your stock scored between 1.1 to 1.49 this means that your stocks PEG ratio would be considered good. It means that the company is doing a good job when it comes to their PEG ratio. This PEG ratio would be considered a good PEG ratio."
            self.__rating += (7 * 0.5)
            return self.emptyDict
        elif 0 <= self.ratioPEG <= 1:
            self.emptyDict[
                'f2'] = "PEG ratio is a financial ratio that helps investors get a better understanding of how well the company and stock is doing.PEG stands for price earning ratio.The PEG ratio is a valuation metric for determining the relative trade-off between the price of a stock, the earnings generated per share, and the company's expected growth this helps inventors understand how much the stock is going to grow. Your stock scored between 0 to 1 this means that your stocks PEG ratio would be considered amazing. It means that the company is doing exceptionally well when it comes to their PEG ratio. This PEG ratio would be considered a very good ratio."
            self.__rating += (10 * 0.5)
            return self.emptyDict
        else:
            return self.emptyDict

    def finalRating(self):
        self.rec = round(((self.__rating / 24) * 100),
                         2)  # gets final rating and divides by a number thats appropriate in terms of justifying recommendation
        return self.rec

    def investmentRecommendation(self):
        self.rec = round(((self.__rating / 24) * 100), 2)
        if self.rec <= 30:
            self.explain = "Strongly Don't Recomend"
            return self.explain
        elif 31 <= self.rec <= 50:
            self.explain = "Don't Recomend"
            return self.explain
        elif 51 <= self.rec <= 65:
            self.explain = "are Neutral on"
            return self.explain
        elif 66 <= self.rec <= 90:
            self.explain = "Recomend"
            return self.explain
        else:
            self.explain = "Strongly Recomend"
            return self.explain

    def finalExplanation(self):
        self.__dictValues = list(self.emptyDict.values())
        for i in range(len(self.__dictValues)):
            self.dictExplain.append(
                self.__dictValues[i])  # transfering items to a new list, to be able to return all items
        return self.dictExplain

    def tickerGraph(self):
        self.history1 = self.__ticker.history(start=self.__start,
                                              end=self.__end)  # gets the dates to be inputted into the graph
        plt.figure()
        plt.plot(self.history1['Close'])  # uses data from closing history, from the given dates
        plt.ylabel('Closing Price (USD$)')
        plt.xlabel('Year')  # labels
        plt.title('Closing Price From Years Stated')
        plt.show()
        plt.savefig('static/img/pic.png')
