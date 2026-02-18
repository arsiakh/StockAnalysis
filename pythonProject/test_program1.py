"""Tests for the Stocks class in program1.py — covers all ratio methods,
rating/recommendation logic, reset, graph generation, and edge cases."""

import os
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd

from program1 import Stocks


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

VALID_INFO = {
    "shortName": "Apple Inc.",
    "regularMarketPrice": 180.0,
    "marketCap": 2_800_000_000_000,
    "trailingPE": 15.0,
    "forwardPE": 14.0,
    "trailingEps": 6.0,
    "returnOnEquity": 0.25,
    "debtToEquity": 45.0,
    "quickRatio": 1.5,
    "pegRatio": 0.9,
}


@pytest.fixture
def stock():
    """Return a Stocks instance with yfinance completely mocked out."""
    with patch("program1.yf.Ticker") as mock_ticker_cls:
        mock_ticker = MagicMock()
        mock_ticker.info = VALID_INFO.copy()
        mock_ticker_cls.return_value = mock_ticker

        s = Stocks("", "AAPL", "2024-01-01", "2024-12-31")
        s.setvalueTicker()
        return s


@pytest.fixture
def fresh_stock():
    """Return an un-initialised Stocks instance (setvalueTicker not called)."""
    return Stocks("", "AAPL", "2024-01-01", "2024-12-31")


# ---------------------------------------------------------------------------
# Constructor & getters
# ---------------------------------------------------------------------------

class TestConstructorAndGetters:
    def test_ticker_symbol(self, stock):
        assert stock.getTicker() == "AAPL"

    def test_start_date(self, stock):
        assert stock.getStart() == "2024-01-01"

    def test_end_date(self, stock):
        assert stock.getEnd() == "2024-12-31"

    def test_initial_rating(self, fresh_stock):
        assert fresh_stock.getRating() == 0.0

    def test_initial_dict_values(self, fresh_stock):
        assert fresh_stock.getdictValues() == []


# ---------------------------------------------------------------------------
# setvalueTicker
# ---------------------------------------------------------------------------

class TestSetvalueTicker:
    def test_valid_ticker(self, stock):
        assert stock.getTicker() == "AAPL"

    def test_empty_info_raises(self):
        with patch("program1.yf.Ticker") as mock_cls:
            mock_cls.return_value.info = {}
            s = Stocks("", "INVALID", "2024-01-01", "2024-12-31")
            with pytest.raises(ValueError, match="Invalid ticker"):
                s.setvalueTicker()

    def test_none_info_raises(self):
        with patch("program1.yf.Ticker") as mock_cls:
            mock_cls.return_value.info = None
            s = Stocks("", "BAD", "2024-01-01", "2024-12-31")
            with pytest.raises(ValueError, match="Invalid ticker"):
                s.setvalueTicker()

    def test_info_without_essential_fields_raises(self):
        with patch("program1.yf.Ticker") as mock_cls:
            mock_cls.return_value.info = {"someIrrelevantKey": True}
            s = Stocks("", "BAD", "2024-01-01", "2024-12-31")
            with pytest.raises(ValueError, match="no stock data found"):
                s.setvalueTicker()

    def test_yfinance_exception_wrapped(self):
        with patch("program1.yf.Ticker") as mock_cls:
            mock_cls.side_effect = RuntimeError("network error")
            s = Stocks("", "ERR", "2024-01-01", "2024-12-31")
            with pytest.raises(ValueError, match="Error fetching ticker data"):
                s.setvalueTicker()


# ---------------------------------------------------------------------------
# ratio1 — PE Ratio
# ---------------------------------------------------------------------------

class TestRatio1PE:
    def test_pe_amazing(self, stock):
        stock.ratio1(ratioPE=5.0)
        assert stock.getRating() == pytest.approx(10 * 0.375)
        assert "pe_amazing" in stock.emptyDict

    def test_pe_good(self, stock):
        stock.ratio1(ratioPE=15.0)
        assert stock.getRating() == pytest.approx(7 * 0.375)
        assert "pe_good" in stock.emptyDict

    def test_pe_ok(self, stock):
        stock.ratio1(ratioPE=22.0)
        assert stock.getRating() == pytest.approx(4 * 0.375)
        assert "pe_ok" in stock.emptyDict

    def test_pe_high(self, stock):
        stock.ratio1(ratioPE=30.0)
        assert stock.getRating() == pytest.approx(2 * 0.375)
        assert "pe_high" in stock.emptyDict

    def test_pe_none_returns_empty(self, stock):
        stock._info = {"trailingPE": None, "forwardPE": None}
        result = stock.ratio1()
        assert stock.getRating() == 0.0
        assert result == stock.emptyDict

    def test_pe_fallback_to_forwardPE(self, stock):
        stock._info = {"trailingPE": None, "forwardPE": 12.0}
        stock.ratio1()
        assert stock.getRating() == pytest.approx(7 * 0.375)

    def test_pe_boundary_20(self, stock):
        stock.ratio1(ratioPE=20.0)
        assert "pe_ok" in stock.emptyDict

    def test_pe_boundary_25(self, stock):
        stock.ratio1(ratioPE=25.0)
        assert "pe_ok" in stock.emptyDict

    def test_pe_boundary_10(self, stock):
        stock.ratio1(ratioPE=10.0)
        assert "pe_good" in stock.emptyDict

    def test_pe_boundary_0(self, stock):
        stock.ratio1(ratioPE=0.0)
        assert "pe_amazing" in stock.emptyDict


# ---------------------------------------------------------------------------
# ratio2 — EPS
# ---------------------------------------------------------------------------

class TestRatio2EPS:
    def test_eps_amazing(self, stock):
        stock.ratio2(ratioEPS=6.0)
        assert stock.getRating() == pytest.approx(10 * 0.25)
        assert "eps_amazing" in stock.emptyDict

    def test_eps_good(self, stock):
        stock.ratio2(ratioEPS=3.0)
        assert stock.getRating() == pytest.approx(7 * 0.25)
        assert "eps_good" in stock.emptyDict

    def test_eps_ok(self, stock):
        stock.ratio2(ratioEPS=1.0)
        assert stock.getRating() == pytest.approx(4 * 0.25)
        assert "eps_ok" in stock.emptyDict

    def test_eps_very_low(self, stock):
        stock.ratio2(ratioEPS=0.5)
        assert stock.getRating() == pytest.approx(2 * 0.25)
        assert "eps_very_low" in stock.emptyDict

    def test_eps_negative(self, stock):
        stock.ratio2(ratioEPS=-2.0)
        assert stock.getRating() == pytest.approx(1 * 0.25)
        assert "eps_negative" in stock.emptyDict

    def test_eps_none_returns_empty(self, stock):
        stock._info = {}
        result = stock.ratio2()
        assert stock.getRating() == 0.0
        assert result == stock.emptyDict

    def test_eps_boundary_0_8(self, stock):
        stock.ratio2(ratioEPS=0.8)
        assert "eps_ok" in stock.emptyDict

    def test_eps_boundary_1_5(self, stock):
        stock.ratio2(ratioEPS=1.5)
        assert "eps_ok" in stock.emptyDict

    def test_eps_boundary_1_6(self, stock):
        stock.ratio2(ratioEPS=1.6)
        assert "eps_good" in stock.emptyDict

    def test_eps_boundary_5_1(self, stock):
        stock.ratio2(ratioEPS=5.1)
        assert "eps_amazing" in stock.emptyDict


# ---------------------------------------------------------------------------
# ratio3 — ROE
# ---------------------------------------------------------------------------

class TestRatio3ROE:
    def test_roe_ok(self, stock):
        stock.ratio3(ratioROE=0.17)
        assert stock.getRating() == pytest.approx(4 * 0.5)
        assert "roe_ok" in stock.emptyDict

    def test_roe_good(self, stock):
        stock.ratio3(ratioROE=0.50)
        assert stock.getRating() == pytest.approx(7 * 0.5)
        assert "roe_good" in stock.emptyDict

    def test_roe_extreme(self, stock):
        stock.ratio3(ratioROE=1.5)
        assert stock.getRating() == pytest.approx(10 * 0.5)
        assert "roe_extreme" in stock.emptyDict

    def test_roe_low(self, stock):
        stock.ratio3(ratioROE=0.10)
        assert stock.getRating() == pytest.approx(2 * 0.5)
        assert "roe_low" in stock.emptyDict

    def test_roe_none_returns_empty(self, stock):
        stock._info = {}
        result = stock.ratio3()
        assert stock.getRating() == 0.0
        assert result == stock.emptyDict

    def test_roe_boundary_15_percent(self, stock):
        stock.ratio3(ratioROE=0.15)
        assert "roe_ok" in stock.emptyDict

    def test_roe_boundary_20_percent(self, stock):
        stock.ratio3(ratioROE=0.20)
        assert "roe_ok" in stock.emptyDict

    def test_roe_boundary_21_percent(self, stock):
        stock.ratio3(ratioROE=0.21)
        assert "roe_good" in stock.emptyDict


# ---------------------------------------------------------------------------
# ratio4 — Debt-to-Equity
# ---------------------------------------------------------------------------

class TestRatio4DebtEquity:
    def test_de_amazing(self, stock):
        stock.ratio4(debt_equity=30.0)
        assert stock.getRating() == pytest.approx(10 * 1)
        assert "de_amazing" in stock.emptyDict

    def test_de_good(self, stock):
        stock.ratio4(debt_equity=75.0)
        assert stock.getRating() == pytest.approx(7 * 1)
        assert "de_good" in stock.emptyDict

    def test_de_ok(self, stock):
        stock.ratio4(debt_equity=150.0)
        assert stock.getRating() == pytest.approx(4 * 1)
        assert "de_ok" in stock.emptyDict

    def test_de_high(self, stock):
        stock.ratio4(debt_equity=300.0)
        assert stock.getRating() == pytest.approx(1 * 1)
        assert "de_high" in stock.emptyDict

    def test_de_none_returns_empty(self, stock):
        stock._info = {}
        result = stock.ratio4()
        assert stock.getRating() == 0.0
        assert result == stock.emptyDict

    def test_de_boundary_0(self, stock):
        stock.ratio4(debt_equity=0.0)
        assert "de_amazing" in stock.emptyDict

    def test_de_boundary_50(self, stock):
        stock.ratio4(debt_equity=50.0)
        assert "de_amazing" in stock.emptyDict

    def test_de_boundary_51(self, stock):
        stock.ratio4(debt_equity=51.0)
        assert "de_good" in stock.emptyDict

    def test_de_boundary_250(self, stock):
        stock.ratio4(debt_equity=250.0)
        assert "de_ok" in stock.emptyDict

    def test_de_boundary_251(self, stock):
        stock.ratio4(debt_equity=251.0)
        assert "de_high" in stock.emptyDict


# ---------------------------------------------------------------------------
# ratio5 — Quick Ratio
# ---------------------------------------------------------------------------

class TestRatio5Quick:
    def test_quick_low(self, stock):
        stock.ratio5(quick=0.5)
        assert stock.getRating() == pytest.approx(2 * 0.75)
        assert "quick_low" in stock.emptyDict

    def test_quick_ok(self, stock):
        stock.ratio5(quick=1.5)
        assert stock.getRating() == pytest.approx(4 * 0.75)
        assert "quick_ok" in stock.emptyDict

    def test_quick_good(self, stock):
        stock.ratio5(quick=3.0)
        assert stock.getRating() == pytest.approx(7 * 0.75)
        assert "quick_good" in stock.emptyDict

    def test_quick_very_high(self, stock):
        stock.ratio5(quick=5.0)
        assert stock.getRating() == pytest.approx(10 * 0.75)
        assert "quick_very_high" in stock.emptyDict

    def test_quick_none_returns_empty(self, stock):
        stock._info = {}
        result = stock.ratio5()
        assert stock.getRating() == 0.0
        assert result == stock.emptyDict

    def test_quick_boundary_1(self, stock):
        stock.ratio5(quick=1.0)
        assert "quick_ok" in stock.emptyDict

    def test_quick_boundary_2(self, stock):
        stock.ratio5(quick=2.0)
        assert "quick_ok" in stock.emptyDict

    def test_quick_boundary_2_1(self, stock):
        stock.ratio5(quick=2.1)
        assert "quick_good" in stock.emptyDict

    def test_quick_boundary_4_1(self, stock):
        stock.ratio5(quick=4.1)
        assert "quick_very_high" in stock.emptyDict


# ---------------------------------------------------------------------------
# ratio6 — PEG Ratio
# ---------------------------------------------------------------------------

class TestRatio6PEG:
    def test_peg_amazing(self, stock):
        stock.ratio6(ratioPEG=0.8)
        assert stock.getRating() == pytest.approx(10 * 0.5)
        assert "peg_amazing" in stock.emptyDict

    def test_peg_good(self, stock):
        stock.ratio6(ratioPEG=1.3)
        assert stock.getRating() == pytest.approx(7 * 0.5)
        assert "peg_good" in stock.emptyDict

    def test_peg_ok(self, stock):
        stock.ratio6(ratioPEG=1.7)
        assert stock.getRating() == pytest.approx(4 * 0.5)
        assert "peg_ok" in stock.emptyDict

    def test_peg_high(self, stock):
        stock.ratio6(ratioPEG=3.0)
        assert stock.getRating() == pytest.approx(3 * 0.5)
        assert "peg_high" in stock.emptyDict

    def test_peg_negative(self, stock):
        stock.ratio6(ratioPEG=-1.0)
        assert stock.getRating() == pytest.approx(2 * 0.5)
        assert "peg_negative" in stock.emptyDict

    def test_peg_none_returns_empty(self, stock):
        stock._info = {}
        result = stock.ratio6()
        assert stock.getRating() == 0.0
        assert result == stock.emptyDict

    def test_peg_boundary_0(self, stock):
        stock.ratio6(ratioPEG=0.0)
        assert "peg_amazing" in stock.emptyDict

    def test_peg_boundary_1(self, stock):
        stock.ratio6(ratioPEG=1.0)
        assert "peg_amazing" in stock.emptyDict

    def test_peg_boundary_1_1(self, stock):
        stock.ratio6(ratioPEG=1.1)
        assert "peg_good" in stock.emptyDict

    def test_peg_boundary_1_5(self, stock):
        stock.ratio6(ratioPEG=1.5)
        assert "peg_ok" in stock.emptyDict

    def test_peg_boundary_2(self, stock):
        stock.ratio6(ratioPEG=2.0)
        assert "peg_ok" in stock.emptyDict

    def test_peg_boundary_2_01(self, stock):
        stock.ratio6(ratioPEG=2.01)
        assert "peg_high" in stock.emptyDict


# ---------------------------------------------------------------------------
# finalRating / investmentRecommendation / finalExplanation
# ---------------------------------------------------------------------------

class TestFinalRating:
    def test_rating_is_percentage(self, stock):
        stock.ratio1(ratioPE=5.0)
        rating = stock.finalRating()
        assert 0 <= rating <= 100

    def test_rating_zero_when_no_ratios(self, stock):
        assert stock.finalRating() == 0.0

    def test_full_analysis_rating(self, stock):
        stock.ratio1(ratioPE=5.0)
        stock.ratio2(ratioEPS=6.0)
        stock.ratio3(ratioROE=0.50)
        stock.ratio4(debt_equity=30.0)
        stock.ratio5(quick=3.0)
        stock.ratio6(ratioPEG=0.8)
        rating = stock.finalRating()
        expected = round(
            (
                (10 * 0.375)
                + (10 * 0.25)
                + (7 * 0.5)
                + (10 * 1)
                + (7 * 0.75)
                + (10 * 0.5)
            )
            / Stocks.MAX_POSSIBLE_RATING
            * 100,
            2,
        )
        assert rating == pytest.approx(expected)


class TestInvestmentRecommendation:
    def _run_all_ratios(self, stock, pe, eps, roe, de, quick, peg):
        stock.ratio1(ratioPE=pe)
        stock.ratio2(ratioEPS=eps)
        stock.ratio3(ratioROE=roe)
        stock.ratio4(debt_equity=de)
        stock.ratio5(quick=quick)
        stock.ratio6(ratioPEG=peg)

    def test_strongly_dont_recommend(self, stock):
        self._run_all_ratios(stock, pe=30, eps=-2, roe=0.05, de=300, quick=0.5, peg=3.0)
        rec = stock.investmentRecommendation()
        assert rec == "Strongly Don't Recommend"

    def test_strongly_recommend(self, stock):
        self._run_all_ratios(stock, pe=5, eps=6, roe=1.5, de=30, quick=5.0, peg=0.5)
        rec = stock.investmentRecommendation()
        assert rec == "Strongly Recommend"

    def test_neutral_range(self, stock):
        self._run_all_ratios(stock, pe=22, eps=1.0, roe=0.17, de=150, quick=1.5, peg=1.7)
        rec = stock.investmentRecommendation()
        assert rec in (
            "Strongly Don't Recommend",
            "Don't Recommend",
            "Neutral",
            "Recommend",
            "Strongly Recommend",
        )

    def test_recommendation_returns_string(self, stock):
        stock.ratio1(ratioPE=15)
        rec = stock.investmentRecommendation()
        assert isinstance(rec, str)


class TestFinalExplanation:
    def test_explanations_populated(self, stock):
        stock.ratio1(ratioPE=15.0)
        stock.ratio2(ratioEPS=6.0)
        explanations = stock.finalExplanation()
        assert len(explanations) >= 2
        assert all(isinstance(e, str) for e in explanations)

    def test_no_explanations_when_nothing_computed(self, stock):
        assert stock.finalExplanation() == []


# ---------------------------------------------------------------------------
# reset_analysis
# ---------------------------------------------------------------------------

class TestResetAnalysis:
    def test_reset_clears_rating(self, stock):
        stock.ratio1(ratioPE=15.0)
        stock.reset_analysis()
        assert stock.getRating() == 0.0

    def test_reset_clears_dict(self, stock):
        stock.ratio1(ratioPE=15.0)
        stock.reset_analysis()
        assert stock.emptyDict == {}

    def test_reset_clears_explanations(self, stock):
        stock.ratio1(ratioPE=15.0)
        stock.reset_analysis()
        assert stock.finalExplanation() == []


# ---------------------------------------------------------------------------
# _ensure_info auto-init
# ---------------------------------------------------------------------------

class TestEnsureInfo:
    def test_ratio_auto_inits_ticker(self):
        with patch("program1.yf.Ticker") as mock_cls:
            mock_cls.return_value.info = VALID_INFO.copy()
            s = Stocks("", "AAPL", "2024-01-01", "2024-12-31")
            s.ratio1(ratioPE=15.0)
            assert s.getRating() > 0


# ---------------------------------------------------------------------------
# tickerGraph
# ---------------------------------------------------------------------------

class TestTickerGraph:
    def test_graph_creates_file(self, stock, tmp_path):
        dates = pd.date_range("2024-01-01", periods=30)
        mock_history = pd.DataFrame({"Close": range(30)}, index=dates)

        with patch.object(stock, "_Stocks__ticker") as mock_ticker:
            mock_ticker.history.return_value = mock_history
            out = str(tmp_path / "test_chart.png")
            stock.tickerGraph(out)
            assert os.path.exists(out)

    def test_graph_handles_empty_history(self, stock):
        with patch.object(stock, "_Stocks__ticker") as mock_ticker:
            mock_ticker.history.return_value = pd.DataFrame()
            stock.tickerGraph("/tmp/should_not_exist.png")

    def test_graph_handles_none_history(self, stock):
        with patch.object(stock, "_Stocks__ticker") as mock_ticker:
            mock_ticker.history.return_value = None
            stock.tickerGraph("/tmp/should_not_exist.png")

    def test_graph_creates_directory(self, stock, tmp_path):
        dates = pd.date_range("2024-01-01", periods=10)
        mock_history = pd.DataFrame({"Close": range(10)}, index=dates)

        with patch.object(stock, "_Stocks__ticker") as mock_ticker:
            mock_ticker.history.return_value = mock_history
            out = str(tmp_path / "subdir" / "chart.png")
            stock.tickerGraph(out)
            assert os.path.exists(out)


# ---------------------------------------------------------------------------
# Integration-style: full analysis pipeline
# ---------------------------------------------------------------------------

class TestFullPipeline:
    def test_complete_analysis_workflow(self):
        with patch("program1.yf.Ticker") as mock_cls:
            mock_cls.return_value.info = VALID_INFO.copy()

            s = Stocks("", "AAPL", "2024-01-01", "2024-12-31")
            s.setvalueTicker()
            s.ratio1()
            s.ratio2()
            s.ratio3()
            s.ratio4()
            s.ratio5()
            s.ratio6()

            rating = s.finalRating()
            rec = s.investmentRecommendation()
            expl = s.finalExplanation()

            assert 0 <= rating <= 100
            assert rec in (
                "Strongly Don't Recommend",
                "Don't Recommend",
                "Neutral",
                "Recommend",
                "Strongly Recommend",
            )
            assert len(expl) > 0

    def test_analysis_then_reset_then_reanalyze(self):
        with patch("program1.yf.Ticker") as mock_cls:
            mock_cls.return_value.info = VALID_INFO.copy()

            s = Stocks("", "AAPL", "2024-01-01", "2024-12-31")
            s.setvalueTicker()
            s.ratio1(ratioPE=15.0)
            first_rating = s.getRating()

            s.reset_analysis()
            assert s.getRating() == 0.0

            s.ratio1(ratioPE=5.0)
            assert s.getRating() != first_rating
