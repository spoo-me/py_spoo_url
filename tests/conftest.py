import pytest
import unittest.mock as mock
import json
from datetime import datetime, timedelta
import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend for testing


@pytest.fixture
def mock_successful_shorten_response():
    """Mock successful shortening API response"""
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.text = json.dumps({"short_url": "https://spoo.me/abc123"})
    return mock_response


@pytest.fixture
def mock_api_error_response():
    """Mock API error response"""
    mock_response = mock.Mock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    return mock_response


@pytest.fixture
def sample_statistics_data():
    """Sample statistics data for testing"""
    return {
        "url": "https://www.example.com",
        "average_daily_clicks": 15.5,
        "average_monthly_clicks": 465.0,
        "average_weekly_clicks": 108.5,
        "total-clicks": 1000,
        "total_unique_clicks": 750,
        "max-clicks": 2000,
        "last-click": "2024-01-15",
        "last-click-browser": "Chrome",
        "last-click-os": "Windows",
        "creation-date": "2024-01-01",
        "creation-time": "14:30:00",
        "browser": {"Chrome": 500, "Firefox": 300, "Safari": 200},
        "os_name": {"Windows": 600, "macOS": 250, "Linux": 150},
        "country": {"USA": 400, "UK": 300, "Germany": 300},
        "referrer": {"Google": 500, "Direct": 300, "Twitter": 200},
        "counter": {"2024-01-01": 50, "2024-01-02": 75, "2024-01-03": 100},
        "unique_browser": {"Chrome": 400, "Firefox": 200, "Safari": 150},
        "unique_os_name": {"Windows": 450, "macOS": 200, "Linux": 100},
        "unique_country": {"USA": 300, "UK": 250, "Germany": 200},
        "unique_referrer": {"Google": 400, "Direct": 200, "Twitter": 150},
        "unique_counter": {"2024-01-01": 40, "2024-01-02": 60, "2024-01-03": 80},
        "expired": False,
        "password": None,
        "_id": "abc123",
    }


@pytest.fixture
def recent_statistics_data(sample_statistics_data):
    """Statistics data with recent dates for last N days testing"""
    data = sample_statistics_data.copy()
    today = datetime.now()
    data["counter"] = {
        (today - timedelta(days=i)).strftime("%Y-%m-%d"): 50 + i * 10
        for i in range(10, 0, -1)
    }
    data["unique_counter"] = {
        (today - timedelta(days=i)).strftime("%Y-%m-%d"): 40 + i * 8
        for i in range(10, 0, -1)
    }
    return data


@pytest.fixture
def mock_geopandas():
    """Mock geopandas functionality for heatmap testing"""
    with mock.patch("geopandas.read_file") as mock_read_file:
        mock_gdf = mock.Mock()
        mock_gdf.merge.return_value = mock_gdf
        mock_gdf.boundary.plot.return_value = mock.Mock()
        mock_gdf.plot.return_value = mock.Mock()
        mock_read_file.return_value = mock_gdf
        yield mock_gdf


@pytest.fixture
def mock_matplotlib():
    """Mock matplotlib functionality for chart testing"""
    with mock.patch("matplotlib.pyplot.subplots") as mock_subplots:
        with mock.patch("matplotlib.pyplot.bar") as mock_bar:
            with mock.patch("matplotlib.pyplot.pie") as mock_pie:
                mock_fig, mock_ax = mock.Mock(), mock.Mock()
                mock_subplots.return_value = (mock_fig, mock_ax)

                yield {
                    "subplots": mock_subplots,
                    "bar": mock_bar,
                    "pie": mock_pie,
                    "fig": mock_fig,
                    "ax": mock_ax,
                }


@pytest.fixture(autouse=True)
def reset_matplotlib():
    """Reset matplotlib state after each test"""
    yield
    # Clear any matplotlib state that might affect other tests
    import matplotlib.pyplot as plt

    plt.close("all")


# Test markers for categorizing tests
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.slow = pytest.mark.slow
