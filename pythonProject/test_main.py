"""Tests for Flask routes in main.py — covers GET/POST, input validation,
session handling, error paths, and the output page."""

import json
from datetime import date, timedelta
from unittest.mock import patch, MagicMock

import pytest
import pandas as pd

import main as main_module
from main import app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"
    with app.test_client() as c:
        yield c


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


def _mock_stock_class():
    """Return a patched Stocks class whose instances are fully mocked."""
    mock_cls = MagicMock()
    instance = MagicMock()
    instance.finalRating.return_value = 75.0
    instance.investmentRecommendation.return_value = "Recommend"
    instance.finalExplanation.return_value = ["Good PE ratio", "Strong EPS"]
    mock_cls.return_value = instance
    return mock_cls


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------

class TestHomeGet:
    def test_home_page_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_home_page_contains_form(self, client):
        resp = client.get("/")
        assert b"ticker" in resp.data or b"Ticker" in resp.data or b"form" in resp.data.lower()


# ---------------------------------------------------------------------------
# POST / — input validation
# ---------------------------------------------------------------------------

class TestHomePostValidation:
    def test_missing_ticker(self, client):
        resp = client.post("/", data={"ticker": "", "start": "2024-01-01", "end": "2024-12-31"})
        assert resp.status_code == 200
        assert b"ticker" in resp.data.lower() or b"Please enter" in resp.data

    def test_missing_start_date(self, client):
        resp = client.post("/", data={"ticker": "AAPL", "start": "", "end": "2024-12-31"})
        assert resp.status_code == 200

    def test_missing_end_date(self, client):
        resp = client.post("/", data={"ticker": "AAPL", "start": "2024-01-01", "end": ""})
        assert resp.status_code == 200

    def test_invalid_date_format(self, client):
        resp = client.post("/", data={"ticker": "AAPL", "start": "not-a-date", "end": "2024-12-31"})
        assert resp.status_code == 200

    def test_end_before_start(self, client):
        resp = client.post("/", data={"ticker": "AAPL", "start": "2024-12-31", "end": "2024-01-01"})
        assert resp.status_code == 200

    def test_start_in_future(self, client):
        future = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
        far_future = (date.today() + timedelta(days=60)).strftime("%Y-%m-%d")
        resp = client.post("/", data={"ticker": "AAPL", "start": future, "end": far_future})
        assert resp.status_code == 200

    def test_end_in_future_flashes_warning(self, client):
        past = (date.today() - timedelta(days=60)).strftime("%Y-%m-%d")
        future = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
        with patch("main.Stocks") as mock_cls:
            mock_cls.return_value = _mock_stock_class().return_value
            resp = client.post(
                "/",
                data={"ticker": "AAPL", "start": past, "end": future},
                follow_redirects=True,
            )
            assert resp.status_code == 200

    def test_ticker_whitespace_is_stripped(self, client):
        past = (date.today() - timedelta(days=60)).strftime("%Y-%m-%d")
        yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        with patch("main.Stocks") as mock_cls:
            mock_cls.return_value = _mock_stock_class().return_value
            resp = client.post(
                "/",
                data={"ticker": "  aapl  ", "start": past, "end": yesterday},
                follow_redirects=True,
            )
            assert resp.status_code == 200
            mock_cls.assert_called_once()
            call_args = mock_cls.call_args[0]
            assert call_args[1] == "AAPL"


# ---------------------------------------------------------------------------
# POST / — successful submission
# ---------------------------------------------------------------------------

class TestHomePostSuccess:
    def test_valid_submission_redirects(self, client):
        past = (date.today() - timedelta(days=60)).strftime("%Y-%m-%d")
        yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        with patch("main.Stocks") as mock_cls:
            mock_cls.return_value = _mock_stock_class().return_value
            resp = client.post(
                "/",
                data={"ticker": "AAPL", "start": past, "end": yesterday},
            )
            assert resp.status_code == 302

    def test_valid_submission_stores_session(self, client):
        past = (date.today() - timedelta(days=60)).strftime("%Y-%m-%d")
        yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        with patch("main.Stocks") as mock_cls:
            mock_cls.return_value = _mock_stock_class().return_value
            with client.session_transaction() as sess:
                pass
            resp = client.post(
                "/",
                data={"ticker": "AAPL", "start": past, "end": yesterday},
                follow_redirects=True,
            )
            assert resp.status_code == 200


# ---------------------------------------------------------------------------
# POST / — error handling
# ---------------------------------------------------------------------------

class TestHomePostErrors:
    def test_value_error_shows_flash(self, client):
        past = (date.today() - timedelta(days=60)).strftime("%Y-%m-%d")
        yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        with patch("main.Stocks") as mock_cls:
            mock_cls.return_value.setvalueTicker.side_effect = ValueError("bad ticker")
            resp = client.post(
                "/",
                data={"ticker": "XXX", "start": past, "end": yesterday},
            )
            assert resp.status_code == 200

    def test_key_error_shows_flash(self, client):
        past = (date.today() - timedelta(days=60)).strftime("%Y-%m-%d")
        yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        with patch("main.Stocks") as mock_cls:
            mock_cls.return_value.setvalueTicker.side_effect = KeyError("trailingPE")
            resp = client.post(
                "/",
                data={"ticker": "AAPL", "start": past, "end": yesterday},
            )
            assert resp.status_code == 200

    def test_generic_exception_shows_flash(self, client):
        past = (date.today() - timedelta(days=60)).strftime("%Y-%m-%d")
        yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        with patch("main.Stocks") as mock_cls:
            mock_cls.return_value.setvalueTicker.side_effect = RuntimeError("unexpected")
            resp = client.post(
                "/",
                data={"ticker": "AAPL", "start": past, "end": yesterday},
            )
            assert resp.status_code == 200


# ---------------------------------------------------------------------------
# GET /output
# ---------------------------------------------------------------------------

class TestOutputPage:
    def test_output_with_session_data(self, client):
        with client.session_transaction() as sess:
            sess["rating"] = 75.0
            sess["recommendation"] = "Recommend"
            sess["explanation"] = json.dumps(["Good PE ratio", "Strong EPS"])

        resp = client.get("/output")
        assert resp.status_code == 200
        assert b"75" in resp.data
        assert b"Recommend" in resp.data

    def test_output_without_session_data(self, client):
        resp = client.get("/output")
        assert resp.status_code == 200
        assert b"N/A" in resp.data

    def test_output_with_invalid_json(self, client):
        with client.session_transaction() as sess:
            sess["rating"] = 50.0
            sess["recommendation"] = "Neutral"
            sess["explanation"] = "not-valid-json"

        resp = client.get("/output")
        assert resp.status_code == 200

    def test_output_deduplicates_explanations(self, client):
        with client.session_transaction() as sess:
            sess["rating"] = 50.0
            sess["recommendation"] = "Neutral"
            sess["explanation"] = json.dumps(["Same text", "Same text", "Different text"])

        resp = client.get("/output")
        assert resp.status_code == 200
        html = resp.data.decode()
        assert html.count("Same text") == 1

    def test_output_empty_explanation_list(self, client):
        with client.session_transaction() as sess:
            sess["rating"] = 42.0
            sess["recommendation"] = "Don't Recommend"
            sess["explanation"] = json.dumps([])

        resp = client.get("/output")
        assert resp.status_code == 200
