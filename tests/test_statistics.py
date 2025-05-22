"""
Tests for the Statistics class core functionality.
"""

import pytest
import unittest.mock as mock
import json
from py_spoo_url import Statistics


@pytest.mark.unit
class TestStatisticsInit:
    """Test suite for Statistics class initialization"""

    @mock.patch("requests.post")
    def test_init_success(self, mock_post, sample_statistics_data):
        """Test successful Statistics initialization"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        assert stats.short_code == "abc123"
        assert stats.long_url == "https://www.example.com"
        assert stats.total_clicks == 1000
        assert stats.total_unique_clicks == 750
        assert stats.average_daily_clicks == 15.5

        # Verify API call
        mock_post.assert_called_once_with("https://spoo.me/stats/abc123", data=None)

    @mock.patch("requests.post")
    def test_init_with_password(self, mock_post, sample_statistics_data):
        """Test Statistics initialization with password"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123", password="secret")

        assert stats.short_code == "abc123"

        # Verify API call with password
        mock_post.assert_called_once_with(
            "https://spoo.me/stats/abc123", data={"password": "secret"}
        )

    @mock.patch("requests.post")
    def test_init_with_url_shortcode(self, mock_post, sample_statistics_data):
        """Test Statistics initialization with full URL containing short code"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("https://spoo.me/abc123")

        assert stats.short_code == "abc123"

    @mock.patch("requests.post")
    def test_init_api_error(self, mock_post):
        """Test Statistics initialization API error handling"""
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_post.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            Statistics("nonexistent")

        assert "Error 404: Not Found" in str(exc_info.value)

    @mock.patch("requests.post")
    def test_init_malformed_json(self, mock_post):
        """Test Statistics initialization with malformed JSON response"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = "invalid json"
        mock_post.return_value = mock_response

        with pytest.raises(json.JSONDecodeError):
            Statistics("abc123")


@pytest.mark.unit
class TestStatisticsProperties:
    """Test suite for Statistics data properties"""

    @mock.patch("requests.post")
    def test_data_properties(self, mock_post, sample_statistics_data):
        """Test all data properties are correctly assigned"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        # Test basic properties
        assert stats.long_url == "https://www.example.com"
        assert stats.average_daily_clicks == 15.5
        assert stats.average_monthly_clicks == 465.0
        assert stats.average_weekly_clicks == 108.5
        assert stats.total_clicks == 1000
        assert stats.total_unique_clicks == 750
        assert stats.max_clicks == 2000
        assert stats.last_click == "2024-01-15"
        assert stats.last_click_browser == "Chrome"
        assert stats.last_click_platform == "Windows"
        assert stats.created_at == "2024-01-01"
        assert stats.creation_time == "14:30:00"
        assert not stats.expired
        assert stats.password is None

        # Test analysis dictionaries
        assert stats.browsers_analysis == {"Chrome": 500, "Firefox": 300, "Safari": 200}
        assert stats.platforms_analysis == {"Windows": 600, "macOS": 250, "Linux": 150}
        assert stats.country_analysis == {"USA": 400, "UK": 300, "Germany": 300}
        assert stats.referrers_analysis == {
            "Google": 500,
            "Direct": 300,
            "Twitter": 200,
        }

        # Test unique analysis dictionaries
        assert stats.unique_browsers_analysis == {
            "Chrome": 400,
            "Firefox": 200,
            "Safari": 150,
        }
        assert stats.unique_platforms_analysis == {
            "Windows": 450,
            "macOS": 200,
            "Linux": 100,
        }
        assert stats.unique_country_analysis == {"USA": 300, "UK": 250, "Germany": 200}
        assert stats.unique_referrers_analysis == {
            "Google": 400,
            "Direct": 200,
            "Twitter": 150,
        }

    @mock.patch("requests.post")
    def test_str_repr(self, mock_post, sample_statistics_data):
        """Test string representation methods"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        assert str(stats) == "<Statistics abc123>"
        assert repr(stats) == "<Statistics abc123>"


@pytest.mark.unit
class TestStatisticsAnalysis:
    """Test suite for Statistics analysis methods"""

    @mock.patch("requests.post")
    def test_last_n_days_analysis(self, mock_post, recent_statistics_data):
        """Test last N days analysis"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(recent_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        result = stats.last_n_days_analysis(days=7)

        assert len(result) <= 7
        assert all(isinstance(date, str) for date in result.keys())
        assert all(isinstance(clicks, int) for clicks in result.values())

    @mock.patch("requests.post")
    def test_last_n_days_unique_analysis(self, mock_post, recent_statistics_data):
        """Test last N days unique analysis"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(recent_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        result = stats.last_n_days_unique_analysis(days=5)

        assert len(result) <= 5
        assert all(isinstance(date, str) for date in result.keys())
        assert all(isinstance(clicks, int) for clicks in result.values())

    @mock.patch("requests.post")
    def test_last_n_days_analysis_no_data(self, mock_post, sample_statistics_data):
        """Test last N days analysis with no recent data"""
        old_data = sample_statistics_data.copy()
        old_data["counter"] = {"2020-01-01": 50}  # Very old data
        old_data["unique_counter"] = {"2020-01-01": 40}  # Very old data

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(old_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with pytest.raises(ValueError) as exc_info:
            stats.last_n_days_analysis(days=7)

        assert "No data available for the last 7 days" in str(exc_info.value)

    @mock.patch("requests.post")
    def test_last_n_days_unique_analysis_no_data(
        self, mock_post, sample_statistics_data
    ):
        """Test last N days unique analysis with no recent data"""
        old_data = sample_statistics_data.copy()
        old_data["counter"] = {"2020-01-01": 50}  # Very old data
        old_data["unique_counter"] = {"2020-01-01": 40}  # Very old data

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(old_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with pytest.raises(ValueError) as exc_info:
            stats.last_n_days_unique_analysis(days=7)

        assert "No data available for the last 7 days" in str(exc_info.value)


@pytest.mark.unit
class TestStatisticsEdgeCases:
    """Test suite for Statistics edge cases"""

    @mock.patch("requests.post")
    def test_empty_statistics_data(self, mock_post):
        """Test statistics with empty data sets"""
        empty_data = {
            "url": "https://example.com",
            "average_daily_clicks": 0,
            "average_monthly_clicks": 0,
            "average_weekly_clicks": 0,
            "total-clicks": 0,
            "total_unique_clicks": 0,
            "max-clicks": None,
            "last-click": None,
            "last-click-browser": None,
            "last-click-os": None,
            "creation-date": "2024-01-01",
            "creation-time": None,
            "browser": {},
            "os_name": {},
            "country": {},
            "referrer": {},
            "counter": {},
            "unique_browser": {},
            "unique_os_name": {},
            "unique_country": {},
            "unique_referrer": {},
            "unique_counter": {},
            "expired": False,
            "password": None,
            "_id": "abc123",
        }

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(empty_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        assert stats.total_clicks == 0
        assert stats.browsers_analysis == {}
        assert stats.country_analysis == {}
        assert stats.creation_time is None

    @mock.patch("requests.post")
    def test_missing_optional_fields(self, mock_post):
        """Test statistics with missing optional fields"""
        minimal_data = {
            "url": "https://example.com",
            "average_daily_clicks": 10,
            "average_monthly_clicks": 300,
            "average_weekly_clicks": 70,
            "total-clicks": 100,
            "total_unique_clicks": 80,
            "max-clicks": 500,
            "last-click": "2024-01-15",
            "last-click-browser": "Chrome",
            "last-click-os": "Windows",
            "creation-date": "2024-01-01",
            # Missing creation-time
            "browser": {"Chrome": 100},
            "os_name": {"Windows": 100},
            "country": {"USA": 100},
            "referrer": {"Google": 100},
            "counter": {"2024-01-01": 100},
            "unique_browser": {"Chrome": 80},
            "unique_os_name": {"Windows": 80},
            "unique_country": {"USA": 80},
            "unique_referrer": {"Google": 80},
            "unique_counter": {"2024-01-01": 80},
            "expired": False,
            # Missing password
            "_id": "abc123",
        }

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(minimal_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        assert stats.total_clicks == 100
        assert stats.creation_time is None  # Should handle missing field
        assert stats.password is None  # Should handle missing field
