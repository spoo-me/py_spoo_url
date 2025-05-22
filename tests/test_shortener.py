"""
Tests for the Shortener class functionality.
"""

import pytest
import unittest.mock as mock
import json
from py_spoo_url import Shortener


@pytest.mark.unit
class TestShortener:
    """Test suite for the Shortener class"""

    def setup_method(self):
        """Setup for each test method"""
        self.shortener = Shortener()

    def test_init(self):
        """Test Shortener initialization"""
        assert self.shortener.short_code is None
        assert self.shortener._url == "https://spoo.me"

    @mock.patch("requests.post")
    def test_shorten_success(self, mock_post):
        """Test successful URL shortening"""
        # Mock successful API response
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({"short_url": "https://spoo.me/abc123"})
        mock_post.return_value = mock_response

        result = self.shortener.shorten("https://www.example.com")

        assert result == "https://spoo.me/abc123"
        assert self.shortener.short_code == "https://spoo.me/abc123"

        # Verify API call
        mock_post.assert_called_once_with(
            "https://spoo.me",
            data={"url": "https://www.example.com"},
            headers={"Accept": "application/json"},
        )

    @mock.patch("requests.post")
    def test_shorten_with_all_parameters(self, mock_post):
        """Test URL shortening with all optional parameters"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({"short_url": "https://spoo.me/custom"})
        mock_post.return_value = mock_response

        result = self.shortener.shorten(
            "https://www.example.com",
            password="secret123",
            max_clicks=100,
            alias="custom",
        )

        assert result == "https://spoo.me/custom"

        # Verify API call with all parameters
        expected_data = {
            "url": "https://www.example.com",
            "password": "secret123",
            "max_clicks": 100,
            "alias": "custom",
        }
        mock_post.assert_called_once_with(
            "https://spoo.me",
            data=expected_data,
            headers={"Accept": "application/json"},
        )

    @mock.patch("requests.post")
    def test_shorten_api_error(self, mock_post):
        """Test URL shortening API error handling"""
        mock_response = mock.Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            self.shortener.shorten("https://www.example.com")

        assert "Error 400: Bad Request" in str(exc_info.value)

    @mock.patch("requests.post")
    def test_shorten_network_error(self, mock_post):
        """Test URL shortening with network error"""
        mock_post.side_effect = ConnectionError("Network error")

        with pytest.raises(ConnectionError):
            self.shortener.shorten("https://www.example.com")


@pytest.mark.unit
class TestEmojifyShortener:
    """Test suite for emoji URL functionality"""

    def setup_method(self):
        """Setup for each test method"""
        self.shortener = Shortener()

    @mock.patch("requests.post")
    def test_emojify_success(self, mock_post):
        """Test successful emoji URL creation"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({"short_url": "https://spoo.me/😆🤯"})
        mock_post.return_value = mock_response

        result = self.shortener.emojify("https://www.example.com")

        assert result == "https://spoo.me/😆🤯"
        assert self.shortener.short_code == "https://spoo.me/😆🤯"

        # Verify API call
        mock_post.assert_called_once_with(
            "https://spoo.me/emoji",
            data={"url": "https://www.example.com"},
            headers={"Accept": "application/json"},
        )

    @mock.patch("requests.post")
    def test_emojify_with_parameters(self, mock_post):
        """Test emoji URL creation with all parameters"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({"short_url": "https://spoo.me/🎉🚀"})
        mock_post.return_value = mock_response

        result = self.shortener.emojify(
            "https://www.example.com",
            emoji_alias="🎉🚀",
            max_clicks=50,
            password="emoji_pass",
        )

        assert result == "https://spoo.me/🎉🚀"

        expected_data = {
            "url": "https://www.example.com",
            "emojies": "🎉🚀",
            "max_clicks": 50,
            "password": "emoji_pass",
        }
        mock_post.assert_called_once_with(
            "https://spoo.me/emoji",
            data=expected_data,
            headers={"Accept": "application/json"},
        )

    @mock.patch("requests.post")
    def test_emojify_api_error(self, mock_post):
        """Test emoji URL creation API error handling"""
        mock_response = mock.Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            self.shortener.emojify("https://www.example.com")

        assert "Error 500: Internal Server Error" in str(exc_info.value)

    @mock.patch("requests.post")
    def test_emojify_with_custom_emoji_sequence(self, mock_post):
        """Test emoji URL creation with custom emoji sequence"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({"short_url": "https://spoo.me/🔥💯🚀"})
        mock_post.return_value = mock_response

        result = self.shortener.emojify("https://www.example.com", emoji_alias="🔥💯🚀")

        assert result == "https://spoo.me/🔥💯🚀"

        expected_data = {"url": "https://www.example.com", "emojies": "🔥💯🚀"}
        mock_post.assert_called_once_with(
            "https://spoo.me/emoji",
            data=expected_data,
            headers={"Accept": "application/json"},
        )
