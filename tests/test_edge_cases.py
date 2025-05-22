import pytest
import unittest.mock as mock
import json
from py_spoo_url import Shortener, Statistics


class TestEdgeCases:
    """Test suite for edge cases and error scenarios"""

    @pytest.mark.unit
    def test_shortener_empty_url(self):
        """Test shortening with empty URL"""
        shortener = Shortener()

        with mock.patch("requests.post") as mock_post:
            mock_response = mock.Mock()
            mock_response.status_code = 400
            mock_response.text = "URL is required"
            mock_post.return_value = mock_response

            with pytest.raises(Exception) as exc_info:
                shortener.shorten("")

            assert "Error 400" in str(exc_info.value)

    @pytest.mark.unit
    def test_shortener_invalid_url(self):
        """Test shortening with invalid URL format"""
        shortener = Shortener()

        with mock.patch("requests.post") as mock_post:
            mock_response = mock.Mock()
            mock_response.status_code = 400
            mock_response.text = "Invalid URL format"
            mock_post.return_value = mock_response

            with pytest.raises(Exception) as exc_info:
                shortener.shorten("not-a-url")

            assert "Error 400" in str(exc_info.value)

    @pytest.mark.unit
    def test_shortener_very_long_url(self):
        """Test shortening with extremely long URL"""
        shortener = Shortener()
        very_long_url = "https://example.com/" + "a" * 10000

        with mock.patch("requests.post") as mock_post:
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.text = json.dumps({"short_url": "https://spoo.me/long123"})
            mock_post.return_value = mock_response

            result = shortener.shorten(very_long_url)
            assert result == "https://spoo.me/long123"

    @pytest.mark.unit
    def test_shortener_special_characters_in_alias(self):
        """Test shortening with special characters in alias"""
        shortener = Shortener()

        with mock.patch("requests.post") as mock_post:
            mock_response = mock.Mock()
            mock_response.status_code = 400
            mock_response.text = "Invalid alias format"
            mock_post.return_value = mock_response

            with pytest.raises(Exception) as exc_info:
                shortener.shorten("https://example.com", alias="test@#$%")

            assert "Error 400" in str(exc_info.value)

    @pytest.mark.unit
    def test_statistics_nonexistent_shortcode(self):
        """Test statistics with non-existent short code"""
        with mock.patch("requests.post") as mock_post:
            mock_response = mock.Mock()
            mock_response.status_code = 404
            mock_response.text = "Short URL not found"
            mock_post.return_value = mock_response

            with pytest.raises(Exception) as exc_info:
                Statistics("nonexistent123")

            assert "Error 404" in str(exc_info.value)

    @pytest.mark.unit
    def test_statistics_wrong_password(self):
        """Test statistics with incorrect password"""
        with mock.patch("requests.post") as mock_post:
            mock_response = mock.Mock()
            mock_response.status_code = 401
            mock_response.text = "Incorrect password"
            mock_post.return_value = mock_response

            with pytest.raises(Exception) as exc_info:
                Statistics("abc123", password="wrongpass")

            assert "Error 401" in str(exc_info.value)

    @pytest.mark.unit
    def test_statistics_malformed_response(self):
        """Test statistics with malformed JSON response"""
        with mock.patch("requests.post") as mock_post:
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.text = "invalid json"
            mock_post.return_value = mock_response

            with pytest.raises(json.JSONDecodeError):
                Statistics("abc123")

    @pytest.mark.unit
    def test_statistics_missing_required_fields(self):
        """Test statistics with response missing required fields"""
        with mock.patch("requests.post") as mock_post:
            mock_response = mock.Mock()
            mock_response.status_code = 200
            # Missing required fields
            incomplete_data = {
                "url": "https://example.com",
                # Missing many required fields
            }
            mock_response.text = json.dumps(incomplete_data)
            mock_post.return_value = mock_response

            with pytest.raises(KeyError):
                Statistics("abc123")

    @pytest.mark.unit
    def test_network_timeout_shortener(self):
        """Test network timeout during shortening"""
        shortener = Shortener()

        with mock.patch("requests.post") as mock_post:
            mock_post.side_effect = Exception("Connection timeout")

            with pytest.raises(Exception) as exc_info:
                shortener.shorten("https://example.com")

            assert "Connection timeout" in str(exc_info.value)

    @pytest.mark.unit
    def test_network_timeout_statistics(self):
        """Test network timeout during statistics retrieval"""
        with mock.patch("requests.post") as mock_post:
            mock_post.side_effect = Exception("Connection timeout")

            with pytest.raises(Exception) as exc_info:
                Statistics("abc123")

            assert "Connection timeout" in str(exc_info.value)

    @pytest.mark.unit
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

        # Test chart generation with empty data
        with mock.patch("matplotlib.pyplot.bar") as mock_bar:
            _ = stats.make_chart("browsers_analysis", "bar")
            # Should not raise an error even with empty data
            mock_bar.assert_called_once()

    @pytest.mark.unit
    @mock.patch("requests.post")
    def test_unicode_in_urls(self, mock_post):
        """Test handling URLs with unicode characters"""
        shortener = Shortener()
        unicode_url = "https://例え.テスト/パス"

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({"short_url": "https://spoo.me/unicode123"})
        mock_post.return_value = mock_response

        result = shortener.shorten(unicode_url)
        assert result == "https://spoo.me/unicode123"

        # Verify the unicode URL was passed correctly
        called_args = mock_post.call_args
        assert called_args[1]["data"]["url"] == unicode_url

    @pytest.mark.unit
    @mock.patch("requests.post")
    def test_large_dataset_statistics(self, mock_post):
        """Test statistics with large datasets"""
        # Create large dataset
        large_data = {
            "url": "https://example.com",
            "average_daily_clicks": 1000.5,
            "average_monthly_clicks": 30000.0,
            "average_weekly_clicks": 7000.0,
            "total-clicks": 1000000,
            "total_unique_clicks": 750000,
            "max-clicks": 2000000,
            "last-click": "2024-01-15",
            "last-click-browser": "Chrome",
            "last-click-os": "Windows",
            "creation-date": "2024-01-01",
            "creation-time": "14:30:00",
            "browser": {f"Browser{i}": i * 100 for i in range(100)},
            "os_name": {f"OS{i}": i * 50 for i in range(50)},
            "country": {f"Country{i}": i * 200 for i in range(200)},
            "referrer": {f"Referrer{i}": i * 75 for i in range(75)},
            "counter": {f"2024-01-{i:02d}": i * 10 for i in range(1, 32)},
            "unique_browser": {f"Browser{i}": i * 80 for i in range(100)},
            "unique_os_name": {f"OS{i}": i * 40 for i in range(50)},
            "unique_country": {f"Country{i}": i * 160 for i in range(200)},
            "unique_referrer": {f"Referrer{i}": i * 60 for i in range(75)},
            "unique_counter": {f"2024-01-{i:02d}": i * 8 for i in range(1, 32)},
            "expired": False,
            "password": None,
            "_id": "abc123",
        }

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(large_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        # Verify large dataset is handled correctly
        assert stats.total_clicks == 1000000
        assert len(stats.browsers_analysis) == 100
        assert len(stats.country_analysis) == 200

        # Test chart generation with large dataset
        with mock.patch("matplotlib.pyplot.bar") as mock_bar:
            _ = stats.make_chart("country_analysis", "bar")
            mock_bar.assert_called_once()


class TestInputValidation:
    """Test suite for input validation"""

    @pytest.mark.unit
    def test_shortener_max_clicks_validation(self):
        """Test max_clicks parameter validation"""
        shortener = Shortener()

        with mock.patch("requests.post") as mock_post:
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.text = json.dumps({"short_url": "https://spoo.me/test"})
            mock_post.return_value = mock_response

            # Test negative max_clicks
            _ = shortener.shorten("https://example.com", max_clicks=-1)

            # Verify the negative value was passed (API should handle validation)
            called_args = mock_post.call_args
            assert called_args[1]["data"]["max-clicks"] == -1

    @pytest.mark.unit
    def test_statistics_short_code_variations(self):
        """Test various short code input formats"""
        test_cases = [
            ("abc123", "abc123"),  # Simple short code
            ("https://spoo.me/abc123", "abc123"),  # Full URL
            ("spoo.me/abc123", "abc123"),  # URL without protocol
            ("abc123/", ""),  # With trailing slash results in empty
            ("/abc123", "abc123"),  # With leading slash
        ]

        for short_code_input, expected_code in test_cases:
            with mock.patch("requests.post") as mock_post:
                mock_response = mock.Mock()
                mock_response.status_code = 200
                mock_response.text = json.dumps(
                    {
                        "url": "https://example.com",
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
                        "_id": expected_code,
                    }
                )
                mock_post.return_value = mock_response

                stats = Statistics(short_code_input)
                # Should resolve to the expected short code
                assert stats.short_code == expected_code
