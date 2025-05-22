"""
Integration tests for the PySpooUrl SDK.
"""

import pytest
import unittest.mock as mock
import json
import os
from py_spoo_url import Shortener, Statistics


@pytest.mark.integration
class TestShortenerStatisticsWorkflow:
    """Integration tests for complete workflows"""

    @mock.patch("requests.post")
    def test_shortener_statistics_workflow(self, mock_post):
        """Test complete workflow: shorten URL then get statistics"""
        # Mock shortening response
        shorten_response = mock.Mock()
        shorten_response.status_code = 200
        shorten_response.text = json.dumps({"short_url": "https://spoo.me/abc123"})

        # Mock statistics response
        stats_response = mock.Mock()
        stats_response.status_code = 200
        sample_data = {
            "url": "https://www.example.com",
            "total-clicks": 0,
            "total_unique_clicks": 0,
            "average_daily_clicks": 0,
            "average_monthly_clicks": 0,
            "average_weekly_clicks": 0,
            "max-clicks": None,
            "last-click": None,
            "last-click-browser": None,
            "last-click-os": None,
            "creation-date": "2024-01-01",
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
        stats_response.text = json.dumps(sample_data)

        # Configure mock to return different responses for different calls
        mock_post.side_effect = [shorten_response, stats_response]

        # Test workflow
        shortener = Shortener()
        short_url = shortener.shorten("https://www.example.com")

        # Extract short code from URL
        short_code = short_url.split("/")[-1]

        stats = Statistics(short_code)

        assert short_url == "https://spoo.me/abc123"
        assert stats.short_code == "abc123"
        assert stats.long_url == "https://www.example.com"

        # Verify both API calls were made
        assert mock_post.call_count == 2

    @mock.patch("requests.post")
    def test_emojify_statistics_workflow(self, mock_post):
        """Test complete workflow: emojify URL then get statistics"""
        # Mock emojify response
        emojify_response = mock.Mock()
        emojify_response.status_code = 200
        emojify_response.text = json.dumps({"short_url": "https://spoo.me/😎🚀"})

        # Mock statistics response
        stats_response = mock.Mock()
        stats_response.status_code = 200
        sample_data = {
            "url": "https://www.example.com",
            "total-clicks": 15,
            "total_unique_clicks": 12,
            "average_daily_clicks": 5.0,
            "average_monthly_clicks": 150.0,
            "average_weekly_clicks": 35.0,
            "max-clicks": 100,
            "last-click": "2024-01-16",
            "last-click-browser": "Firefox",
            "last-click-os": "macOS",
            "creation-date": "2024-01-01",
            "browser": {"Firefox": 8, "Chrome": 7},
            "os_name": {"macOS": 8, "Windows": 7},
            "country": {"USA": 10, "UK": 5},
            "referrer": {"Direct": 10, "Google": 5},
            "counter": {"2024-01-15": 5, "2024-01-16": 10},
            "unique_browser": {"Firefox": 6, "Chrome": 6},
            "unique_os_name": {"macOS": 6, "Windows": 6},
            "unique_country": {"USA": 8, "UK": 4},
            "unique_referrer": {"Direct": 8, "Google": 4},
            "unique_counter": {"2024-01-15": 4, "2024-01-16": 8},
            "expired": False,
            "password": None,
            "_id": "😎🚀",
        }
        stats_response.text = json.dumps(sample_data)

        # Configure mock to return different responses for different calls
        mock_post.side_effect = [emojify_response, stats_response]

        # Test workflow
        shortener = Shortener()
        emoji_url = shortener.emojify("https://www.example.com", emoji_alias="😎🚀")

        # Extract short code from URL
        short_code = emoji_url.split("/")[-1]

        stats = Statistics(short_code)

        assert emoji_url == "https://spoo.me/😎🚀"
        assert stats.short_code == "😎🚀"
        assert stats.long_url == "https://www.example.com"
        assert stats.total_clicks == 15

        # Verify both API calls were made
        assert mock_post.call_count == 2


@pytest.mark.integration
class TestPasswordProtectedWorkflow:
    """Integration tests for password-protected URLs"""

    @mock.patch("requests.post")
    def test_password_protected_workflow(self, mock_post):
        """Test workflow with password-protected URL"""
        # Mock shortening response
        shorten_response = mock.Mock()
        shorten_response.status_code = 200
        shorten_response.text = json.dumps({"short_url": "https://spoo.me/secret123"})

        # Mock statistics response
        stats_response = mock.Mock()
        stats_response.status_code = 200
        sample_data = {
            "url": "https://www.example.com/private",
            "total-clicks": 5,
            "total_unique_clicks": 4,
            "average_daily_clicks": 1.0,
            "average_monthly_clicks": 30.0,
            "average_weekly_clicks": 7.0,
            "max-clicks": 50,
            "last-click": "2024-01-15",
            "last-click-browser": "Chrome",
            "last-click-os": "Windows",
            "creation-date": "2024-01-01",
            "browser": {"Chrome": 5},
            "os_name": {"Windows": 5},
            "country": {"USA": 5},
            "referrer": {"Direct": 5},
            "counter": {"2024-01-15": 5},
            "unique_browser": {"Chrome": 4},
            "unique_os_name": {"Windows": 4},
            "unique_country": {"USA": 4},
            "unique_referrer": {"Direct": 4},
            "unique_counter": {"2024-01-15": 4},
            "expired": False,
            "password": "mypassword",
            "_id": "secret123",
        }
        stats_response.text = json.dumps(sample_data)

        # Configure mock to return different responses for different calls
        mock_post.side_effect = [shorten_response, stats_response]

        # Test workflow
        shortener = Shortener()
        short_url = shortener.shorten(
            "https://www.example.com/private", password="mypassword", max_clicks=50
        )

        # Extract short code from URL
        short_code = short_url.split("/")[-1]

        # Get statistics with password
        stats = Statistics(short_code, password="mypassword")

        assert short_url == "https://spoo.me/secret123"
        assert stats.short_code == "secret123"
        assert stats.long_url == "https://www.example.com/private"
        assert stats.password == "mypassword"
        assert stats.max_clicks == 50

        # Verify both API calls were made with correct parameters
        assert mock_post.call_count == 2

        # Check shortening call
        first_call = mock_post.call_args_list[0]
        assert first_call[1]["data"]["password"] == "mypassword"
        assert first_call[1]["data"]["max_clicks"] == 50

        # Check statistics call
        second_call = mock_post.call_args_list[1]
        assert second_call[1]["data"]["password"] == "mypassword"


@pytest.mark.integration
class TestCompleteAnalyticsWorkflow:
    """Integration tests for complete analytics workflow"""

    @mock.patch("requests.post")
    def test_complete_analytics_workflow(self, mock_post, sample_statistics_data):
        """Test complete analytics workflow: shorten, analyze, chart, export"""
        # Mock shortening response
        shorten_response = mock.Mock()
        shorten_response.status_code = 200
        shorten_response.text = json.dumps(
            {"short_url": "https://spoo.me/analytics123"}
        )

        # Mock statistics response
        stats_response = mock.Mock()
        stats_response.status_code = 200
        stats_response.text = json.dumps(sample_statistics_data)

        # Configure mock to return different responses for different calls
        mock_post.side_effect = [shorten_response, stats_response]

        # Step 1: Shorten URL
        shortener = Shortener()
        short_url = shortener.shorten("https://www.example.com/analytics")
        short_code = short_url.split("/")[-1]

        # Step 2: Get statistics
        stats = Statistics(short_code)

        # Step 3: Analyze data
        assert stats.total_clicks == 1000
        assert stats.total_unique_clicks == 750
        assert len(stats.browsers_analysis) == 3
        assert len(stats.country_analysis) == 3

        # Step 4: Generate charts
        with mock.patch("matplotlib.pyplot.bar") as mock_bar:
            chart_result = stats.make_chart("browsers_analysis", "bar")
            assert chart_result is not None
            mock_bar.assert_called_once()

        with mock.patch("matplotlib.pyplot.pie") as mock_pie:
            pie_result = stats.make_chart("country_analysis", "pie")
            assert pie_result is not None
            mock_pie.assert_called_once()

        # Step 5: Export data
        temp_filename = "analytics_export.json"
        try:
            stats.export_data(filename=temp_filename, filetype="json")

            # Verify export
            assert os.path.exists(temp_filename)
            with open(temp_filename, "r") as f:
                exported_data = json.load(f)
            assert exported_data == sample_statistics_data

        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


@pytest.mark.integration
class TestMultipleURLWorkflow:
    """Integration tests for managing multiple URLs"""

    @mock.patch("requests.post")
    def test_multiple_url_management(self, mock_post):
        """Test managing multiple shortened URLs"""
        # Mock responses for multiple URLs
        url_responses = [
            {"short_url": "https://spoo.me/url1"},
            {"short_url": "https://spoo.me/url2"},
            {"short_url": "https://spoo.me/url3"},
        ]

        stats_responses = []
        for i in range(3):
            stats_data = {
                "url": f"https://www.example{i + 1}.com",
                "total-clicks": (i + 1) * 100,
                "total_unique_clicks": (i + 1) * 75,
                "average_daily_clicks": (i + 1) * 10.0,
                "average_monthly_clicks": (i + 1) * 300.0,
                "average_weekly_clicks": (i + 1) * 70.0,
                "max-clicks": (i + 1) * 1000,
                "last-click": "2024-01-15",
                "last-click-browser": "Chrome",
                "last-click-os": "Windows",
                "creation-date": "2024-01-01",
                "browser": {"Chrome": (i + 1) * 50, "Firefox": (i + 1) * 30},
                "os_name": {"Windows": (i + 1) * 60, "macOS": (i + 1) * 20},
                "country": {"USA": (i + 1) * 40, "UK": (i + 1) * 35},
                "referrer": {"Google": (i + 1) * 50, "Direct": (i + 1) * 25},
                "counter": {f"2024-01-{15 + i}": (i + 1) * 50},
                "unique_browser": {"Chrome": (i + 1) * 40, "Firefox": (i + 1) * 25},
                "unique_os_name": {"Windows": (i + 1) * 50, "macOS": (i + 1) * 15},
                "unique_country": {"USA": (i + 1) * 35, "UK": (i + 1) * 30},
                "unique_referrer": {"Google": (i + 1) * 40, "Direct": (i + 1) * 20},
                "unique_counter": {f"2024-01-{15 + i}": (i + 1) * 40},
                "expired": False,
                "password": None,
                "_id": f"url{i + 1}",
            }
            stats_responses.append(stats_data)

        # Prepare mock responses
        mock_responses = []
        for i in range(3):
            # Shortening response
            shorten_mock = mock.Mock()
            shorten_mock.status_code = 200
            shorten_mock.text = json.dumps(url_responses[i])
            mock_responses.append(shorten_mock)

            # Statistics response
            stats_mock = mock.Mock()
            stats_mock.status_code = 200
            stats_mock.text = json.dumps(stats_responses[i])
            mock_responses.append(stats_mock)

        mock_post.side_effect = mock_responses

        # Test workflow
        shortener = Shortener()
        urls_and_stats = []

        for i in range(3):
            # Shorten URL
            short_url = shortener.shorten(f"https://www.example{i + 1}.com")
            short_code = short_url.split("/")[-1]

            # Get statistics
            stats = Statistics(short_code)

            urls_and_stats.append((short_url, stats))

        # Verify all URLs were created and have correct statistics
        assert len(urls_and_stats) == 3

        for i, (short_url, stats) in enumerate(urls_and_stats):
            assert short_url == f"https://spoo.me/url{i + 1}"
            assert stats.short_code == f"url{i + 1}"
            assert stats.total_clicks == (i + 1) * 100
            assert stats.total_unique_clicks == (i + 1) * 75
            assert stats.long_url == f"https://www.example{i + 1}.com"

        # Verify all API calls were made
        assert mock_post.call_count == 6  # 3 shortenings + 3 statistics


@pytest.mark.integration
class TestErrorRecoveryWorkflow:
    """Integration tests for error recovery scenarios"""

    @mock.patch("requests.post")
    def test_partial_failure_recovery(self, mock_post):
        """Test recovery from partial failures in workflow"""
        # Mock first shortening failure, then success
        failure_response = mock.Mock()
        failure_response.status_code = 400
        failure_response.text = "Bad Request"

        success_response = mock.Mock()
        success_response.status_code = 200
        success_response.text = json.dumps(
            {"short_url": "https://spoo.me/recovered123"}
        )

        stats_response = mock.Mock()
        stats_response.status_code = 200
        sample_data = {
            "url": "https://www.example.com",
            "total-clicks": 0,
            "total_unique_clicks": 0,
            "average_daily_clicks": 0,
            "average_monthly_clicks": 0,
            "average_weekly_clicks": 0,
            "max-clicks": None,
            "last-click": None,
            "last-click-browser": None,
            "last-click-os": None,
            "creation-date": "2024-01-01",
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
            "_id": "recovered123",
        }
        stats_response.text = json.dumps(sample_data)

        mock_post.side_effect = [failure_response, success_response, stats_response]

        shortener = Shortener()

        # First attempt should fail
        with pytest.raises(Exception):
            shortener.shorten("https://www.example.com")

        # Second attempt should succeed
        short_url = shortener.shorten("https://www.example.com")
        short_code = short_url.split("/")[-1]

        # Statistics should work
        stats = Statistics(short_code)

        assert short_url == "https://spoo.me/recovered123"
        assert stats.short_code == "recovered123"
        assert mock_post.call_count == 3


@pytest.mark.integration
@pytest.mark.slow
class TestPerformanceWorkflow:
    """Integration tests for performance scenarios"""

    @mock.patch("requests.post")
    def test_large_dataset_workflow(self, mock_post):
        """Test workflow with large datasets"""
        # Create large dataset
        large_browsers = {f"Browser{i}": i * 10 for i in range(100)}
        large_countries = {f"Country{i}": i * 5 for i in range(200)}
        large_counter = {f"2024-01-{i:02d}": i * 20 for i in range(1, 32)}

        large_data = {
            "url": "https://www.example.com/large",
            "average_daily_clicks": 500.0,
            "average_monthly_clicks": 15000.0,
            "average_weekly_clicks": 3500.0,
            "total-clicks": 50000,
            "total_unique_clicks": 35000,
            "max-clicks": 100000,
            "last-click": "2024-01-31",
            "last-click-browser": "Chrome",
            "last-click-os": "Windows",
            "creation-date": "2024-01-01",
            "creation-time": "14:30:00",
            "browser": large_browsers,
            "os_name": {"Windows": 25000, "macOS": 15000, "Linux": 10000},
            "country": large_countries,
            "referrer": {"Google": 30000, "Direct": 15000, "Social": 5000},
            "counter": large_counter,
            "unique_browser": {k: int(v * 0.7) for k, v in large_browsers.items()},
            "unique_os_name": {"Windows": 17500, "macOS": 10500, "Linux": 7000},
            "unique_country": {k: int(v * 0.7) for k, v in large_countries.items()},
            "unique_referrer": {"Google": 21000, "Direct": 10500, "Social": 3500},
            "unique_counter": {k: int(v * 0.7) for k, v in large_counter.items()},
            "expired": False,
            "password": None,
            "_id": "large123",
        }

        # Mock responses
        shorten_response = mock.Mock()
        shorten_response.status_code = 200
        shorten_response.text = json.dumps({"short_url": "https://spoo.me/large123"})

        stats_response = mock.Mock()
        stats_response.status_code = 200
        stats_response.text = json.dumps(large_data)

        mock_post.side_effect = [shorten_response, stats_response]

        # Test workflow
        shortener = Shortener()
        short_url = shortener.shorten("https://www.example.com/large")
        short_code = short_url.split("/")[-1]

        stats = Statistics(short_code)

        # Verify large dataset handling
        assert stats.total_clicks == 50000
        assert len(stats.browsers_analysis) == 100
        assert len(stats.country_analysis) == 200
        assert len(stats.clicks_analysis) == 31

        # Test chart generation with large dataset
        with mock.patch("matplotlib.pyplot.bar") as mock_bar:
            result = stats.make_chart("browsers_analysis", "bar")
            assert result is not None
            mock_bar.assert_called_once()

        # Test export with large dataset
        temp_filename = "large_export.json"
        try:
            stats.export_data(filename=temp_filename, filetype="json")

            assert os.path.exists(temp_filename)
            file_size = os.path.getsize(temp_filename)
            assert file_size > 1000  # Should be a substantial file

        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
