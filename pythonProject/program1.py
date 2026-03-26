import os
import yfinance as yf
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for Flask compatibility (must be before pyplot import)
import matplotlib.pyplot as plt

# Use seaborn style if available, otherwise use default
try:
    plt.style.use("seaborn-v0_8")
except OSError:
    try:
        plt.style.use("seaborn")
    except OSError:
        plt.style.use("default")


class Stocks:
    MAX_POSSIBLE_RATING = 33.75  # keep this in one place

    def __init__(self, history, ticker, start, end):
        # Keep the original symbol separate from the yfinance object
        self.__symbol = ticker
        self.__ticker = None  # will become yf.Ticker after setvalueTicker()

        self.__start = start
        self.__end = end
        self.history1 = history

        self.__rating = 0.0

        # Store explanations cleanly
        self.emptyDict = {}
        self.__dictValues = []
        self.dictExplain = []
        self.rec = 0
        self.explain = None

        # Cache for yfinance info
        self._info = None

    def getTicker(self):
        # Return the symbol (string), not the yf.Ticker object
        return self.__symbol

    def getStart(self):
        return self.__start

    def getEnd(self):
        return self.__end

    def getRating(self):
        return self.__rating

    def getdictValues(self):
        return self.__dictValues

    def setvalueTicker(self):
        """
        Initializes the yfinance ticker object and caches .info once.
        Call this before calling ratio methods.
        """
        try:
            self.__ticker = yf.Ticker(self.__symbol)

            # Cache info once to avoid multiple network calls
            self._info = self.__ticker.info

            # Check if the ticker is valid by looking for essential fields
            # Invalid tickers often return empty dict or dict with minimal/null data
            if not self._info or len(self._info) == 0:
                raise ValueError(f"Invalid ticker symbol: '{self.__symbol}' not found.")
            
            # Check for essential fields that indicate a valid stock
            # Valid stocks should have at least a name or market price
            has_name = self._info.get('shortName') or self._info.get('longName')
            has_price = self._info.get('regularMarketPrice') or self._info.get('currentPrice')
            has_market_cap = self._info.get('marketCap')
            
            if not has_name and not has_price and not has_market_cap:
                raise ValueError(f"Invalid ticker symbol: '{self.__symbol}' - no stock data found.")

            return self.__ticker
        except ValueError:
            # Re-raise ValueError as-is (our custom validation errors)
            raise
        except Exception as e:
            raise ValueError(f"Error fetching ticker data for '{self.__symbol}': {str(e)}")

    def _ensure_info(self):
        """Safety: make sure ticker/info are initialized."""
        if self.__ticker is None or self._info is None:
            self.setvalueTicker()

    def reset_analysis(self):
        """
        Call this before running ratios again on the same object,
        so old explanations/ratings don't carry over.
        """
        self.emptyDict.clear()
        self.dictExplain.clear()
        self.__dictValues = []
        self.__rating = 0.0
        self.rec = 0
        self.explain = None

    def ratio1(self, ratioPE=None):
        """PE Ratio (trailingPE preferred; fallback forwardPE)."""
        self._ensure_info()

        try:
            info = self._info

            # Allow passing in a value; otherwise pull from yfinance
            if ratioPE is not None:
                self.ratioPE = ratioPE
            else:
                if info.get("trailingPE") is not None:
                    self.ratioPE = info["trailingPE"]
                elif info.get("forwardPE") is not None:
                    self.ratioPE = info["forwardPE"]
                else:
                    return self.emptyDict

            if self.ratioPE is None:
                return self.emptyDict

            if 20 <= self.ratioPE <= 25:
                self.emptyDict["pe_ok"] = (
                    "The PE ratio compares share price to earnings per share. A PE between 20 and 25 is often viewed "
                    "as reasonable/okay (context matters by industry)."
                )
                self.__rating += (4 * 0.375)
            elif 10 <= self.ratioPE <= 19:
                self.emptyDict["pe_good"] = (
                    "The PE ratio compares share price to earnings per share. A PE between 10 and 19 is often viewed "
                    "as good/value-leaning (context matters by industry)."
                )
                self.__rating += (7 * 0.375)
            elif 0 <= self.ratioPE <= 9.9:
                self.emptyDict["pe_amazing"] = (
                    "The PE ratio compares share price to earnings per share. A PE under ~10 can look very attractive, "
                    "but can also reflect low growth expectations or risk."
                )
                self.__rating += (10 * 0.375)
            elif self.ratioPE > 25:
                self.emptyDict["pe_high"] = (
                    "The PE ratio is above 25, which may indicate the stock is overvalued or has high growth expectations."
                )
                self.__rating += (2 * 0.375)

            return self.emptyDict
        except Exception:
            return self.emptyDict

    def ratio2(self, ratioEPS=None):
        """EPS (trailingEps)."""
        self._ensure_info()

        try:
            info = self._info

            if ratioEPS is not None:
                self.ratioEPS = ratioEPS
            else:
                self.ratioEPS = info.get("trailingEps")

            if self.ratioEPS is None:
                return self.emptyDict

            if self.ratioEPS < 0:
                self.emptyDict["eps_negative"] = (
                    "EPS (earnings per share) is negative, which can indicate the company is currently unprofitable."
                )
                self.__rating += (1 * 0.25)
            elif 0.8 <= self.ratioEPS <= 1.5:
                self.emptyDict["eps_ok"] = "EPS is modest; generally okay depending on company size/industry."
                self.__rating += (4 * 0.25)
            elif 1.6 <= self.ratioEPS <= 5:
                self.emptyDict["eps_good"] = "EPS is solid; generally a good sign of profitability."
                self.__rating += (7 * 0.25)
            elif self.ratioEPS >= 5.1:
                self.emptyDict["eps_amazing"] = "EPS is high; often a strong profitability signal (context matters)."
                self.__rating += (10 * 0.25)
            elif 0 <= self.ratioEPS < 0.8:
                self.emptyDict["eps_very_low"] = "EPS is very low but positive; profitability is minimal."
                self.__rating += (2 * 0.25)

            return self.emptyDict
        except Exception:
            return self.emptyDict

    def ratio3(self, ratioROE=None):
        """ROE (returnOnEquity) as percent."""
        self._ensure_info()

        try:
            info = self._info

            if ratioROE is not None:
                self.ratioROE = ratioROE
            else:
                self.ratioROE = info.get("returnOnEquity")

            if self.ratioROE is None:
                return self.emptyDict

            # yfinance commonly gives ROE as a decimal (e.g., 0.21 = 21%)
            self.ratioROE = self.ratioROE * 100

            if 15 <= self.ratioROE <= 20:
                self.emptyDict["roe_ok"] = (
                    "ROE (return on equity) measures profitability relative to shareholders' equity. "
                    "A ROE between 15% and 20% is often considered okay/solid."
                )
                self.__rating += (4 * 0.5)
            elif 21 <= self.ratioROE <= 100:
                self.emptyDict["roe_good"] = (
                    "ROE (return on equity) measures profitability relative to shareholders' equity. "
                    "A ROE above ~20% is often considered strong (verify sustainability)."
                )
                self.__rating += (7 * 0.5)
            elif self.ratioROE >= 101:
                self.emptyDict["roe_extreme"] = (
                    "ROE is extremely high. This can happen, but it can also be distorted by buybacks, "
                    "very low equity, or one-time effects—double-check fundamentals."
                )
                self.__rating += (10 * 0.5)
            elif self.ratioROE < 15:
                self.emptyDict["roe_low"] = (
                    "ROE is below 15%, which may indicate lower profitability or less efficient use of equity."
                )
                self.__rating += (2 * 0.5)

            return self.emptyDict
        except Exception:
            return self.emptyDict

    def ratio4(self, debt_equity=None):
        """Debt-to-equity (debtToEquity)."""
        self._ensure_info()

        try:
            info = self._info

            if debt_equity is not None:
                self.debt_equity = debt_equity
            else:
                self.debt_equity = info.get("debtToEquity")

            if self.debt_equity is None:
                return self.emptyDict

            if 0 <= self.debt_equity <= 50:
                self.emptyDict["de_amazing"] = (
                    "Debt-to-equity is low (0–50), suggesting lower leverage and typically lower financial risk."
                )
                self.__rating += (10 * 1)
            elif 51 <= self.debt_equity <= 99:
                self.emptyDict["de_good"] = "Debt-to-equity is moderate (51–99), generally acceptable leverage."
                self.__rating += (7 * 1)
            elif 100 <= self.debt_equity <= 250:
                self.emptyDict["de_ok"] = "Debt-to-equity is higher (100–250); leverage risk is more meaningful."
                self.__rating += (4 * 1)
            elif self.debt_equity > 250:
                self.emptyDict["de_high"] = (
                    "Debt-to-equity is very high (>250), indicating significant leverage and increased risk."
                )
                self.__rating += (1 * 1)

            return self.emptyDict
        except Exception:
            return self.emptyDict

    def ratio5(self, quick=None):
        """Quick ratio (quickRatio)."""
        self._ensure_info()

        try:
            info = self._info

            if quick is not None:
                self.quick = quick
            else:
                self.quick = info.get("quickRatio")

            if self.quick is None:
                return self.emptyDict

            if self.quick < 1:
                self.emptyDict["quick_low"] = (
                    "Quick ratio is below 1, which may indicate liquidity pressure meeting short-term obligations."
                )
                self.__rating += (2 * 0.75)
            elif 1 <= self.quick <= 2:
                self.emptyDict["quick_ok"] = "Quick ratio is 1–2, generally a reasonable liquidity position."
                self.__rating += (4 * 0.75)
            elif 2.1 <= self.quick <= 4:
                self.emptyDict["quick_good"] = "Quick ratio is 2.1–4, typically strong liquidity."
                self.__rating += (7 * 0.75)
            elif self.quick >= 4.1:
                self.emptyDict["quick_very_high"] = (
                    "Quick ratio is very high; liquidity is strong, but check if excess cash is being used effectively."
                )
                self.__rating += (10 * 0.75)

            return self.emptyDict
        except Exception:
            return self.emptyDict

    def ratio6(self, ratioPEG=None):
        """PEG ratio (pegRatio)."""
        self._ensure_info()

        try:
            info = self._info

            if ratioPEG is not None:
                self.ratioPEG = ratioPEG
            else:
                self.ratioPEG = info.get("pegRatio")

            if self.ratioPEG is None:
                return self.emptyDict

            if self.ratioPEG < 0:
                self.emptyDict["peg_negative"] = (
                    "PEG is negative; this can happen with negative earnings or unusual growth assumptions."
                )
                self.__rating += (2 * 0.5)
            elif self.ratioPEG > 2:
                self.emptyDict["peg_high"] = (
                    "PEG is above 2; this can suggest the stock is expensive relative to expected growth."
                )
                self.__rating += (3 * 0.5)
            elif 1.5 <= self.ratioPEG <= 2:
                self.emptyDict["peg_ok"] = "PEG is 1.5–2, often considered okay depending on context."
                self.__rating += (4 * 0.5)
            elif 1.1 <= self.ratioPEG <= 1.49:
                self.emptyDict["peg_good"] = "PEG is 1.1–1.49, often considered good/attractive."
                self.__rating += (7 * 0.5)
            elif 0 <= self.ratioPEG <= 1:
                self.emptyDict["peg_amazing"] = "PEG is 0–1, often considered very attractive (verify assumptions)."
                self.__rating += (10 * 0.5)

            return self.emptyDict
        except Exception:
            return self.emptyDict

    def finalRating(self):
        self.rec = round(((self.__rating / self.MAX_POSSIBLE_RATING) * 100), 2)
        return self.rec

    def investmentRecommendation(self):
        self.rec = round(((self.__rating / self.MAX_POSSIBLE_RATING) * 100), 2)

        if self.rec <= 30:
            self.explain = "Strongly Don't Recommend"
        elif 31 <= self.rec <= 50:
            self.explain = "Don't Recommend"
        elif 51 <= self.rec <= 65:
            self.explain = "Neutral"
        elif 66 <= self.rec <= 90:
            self.explain = "Recommend"
        else:
            self.explain = "Strongly Recommend"

        return self.explain

    def finalExplanation(self):
        # Return explanations in insertion order
        return list(self.emptyDict.values())

    def tickerGraph(self, out_path="static/img/pic.png"):
        self._ensure_info()

        try:
            self.history1 = self.__ticker.history(start=self.__start, end=self.__end)

            if self.history1 is None or self.history1.empty:
                return

            # Ensure directory exists
            out_dir = os.path.dirname(out_path)
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)

            plt.figure(figsize=(14, 8))
            plt.plot(self.history1["Close"])
            plt.ylabel("Closing Price (USD$)")
            plt.xlabel("Date")
            plt.title(f"Closing Price From {self.__start} to {self.__end}")
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(out_path, dpi=150, bbox_inches="tight")
            plt.close()
        except Exception as e:
            print(f"Warning: Could not generate graph: {str(e)}")
            return
