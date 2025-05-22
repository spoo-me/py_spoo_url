"""
Tests for chart generation and visualization functionality.
"""

import pytest
import unittest.mock as mock
import json
import matplotlib.pyplot as plt
from py_spoo_url import Statistics


@pytest.mark.unit
class TestChartGeneration:
    """Test suite for chart generation functionality"""

    @mock.patch("requests.post")
    def test_make_chart_bar(self, mock_post, sample_statistics_data):
        """Test chart creation with bar chart"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        # Test bar chart creation
        with mock.patch("matplotlib.pyplot.bar") as mock_bar:
            result = stats.make_chart("browsers_analysis", "bar")

            assert result == plt
            mock_bar.assert_called_once()

    @mock.patch("requests.post")
    def test_make_chart_pie(self, mock_post, sample_statistics_data):
        """Test chart creation with pie chart"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        # Test pie chart creation
        with mock.patch("matplotlib.pyplot.pie") as mock_pie:
            result = stats.make_chart("country_analysis", "pie")

            assert result == plt
            mock_pie.assert_called_once()

    @mock.patch("requests.post")
    def test_make_chart_line(self, mock_post, sample_statistics_data):
        """Test chart creation with line chart"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with mock.patch("matplotlib.pyplot.plot") as mock_plot:
            result = stats.make_chart("clicks_analysis", "line")

            assert result == plt
            mock_plot.assert_called_once()

    @mock.patch("requests.post")
    def test_make_chart_scatter(self, mock_post, sample_statistics_data):
        """Test chart creation with scatter plot"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with mock.patch("matplotlib.pyplot.scatter") as mock_scatter:
            result = stats.make_chart("platforms_analysis", "scatter")

            assert result == plt
            mock_scatter.assert_called_once()

    @mock.patch("requests.post")
    def test_make_chart_histogram(self, mock_post, sample_statistics_data):
        """Test chart creation with histogram"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with mock.patch("matplotlib.pyplot.hist") as mock_hist:
            result = stats.make_chart("referrers_analysis", "hist")

            assert result == plt
            mock_hist.assert_called_once()

    @mock.patch("requests.post")
    def test_make_chart_boxplot(self, mock_post, sample_statistics_data):
        """Test chart creation with box plot"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with mock.patch("matplotlib.pyplot.boxplot") as mock_box:
            result = stats.make_chart("unique_browsers_analysis", "box")

            assert result == plt
            mock_box.assert_called_once()

    @mock.patch("requests.post")
    def test_make_chart_area(self, mock_post, sample_statistics_data):
        """Test chart creation with area plot"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with mock.patch("matplotlib.pyplot.stackplot") as mock_area:
            result = stats.make_chart("unique_country_analysis", "area")

            assert result == plt
            mock_area.assert_called_once()


@pytest.mark.unit
class TestChartDataTypes:
    """Test suite for different data types in charts"""

    @mock.patch("requests.post")
    def test_all_valid_data_types(self, mock_post, sample_statistics_data):
        """Test chart creation with all valid data types"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        valid_data_types = [
            "browsers_analysis",
            "platforms_analysis",
            "country_analysis",
            "referrers_analysis",
            "clicks_analysis",
            "unique_browsers_analysis",
            "unique_platforms_analysis",
            "unique_country_analysis",
            "unique_referrers_analysis",
            "unique_clicks_analysis",
        ]

        for data_type in valid_data_types:
            with mock.patch("matplotlib.pyplot.bar"):
                result = stats.make_chart(data_type, "bar")
                assert result == plt

    @mock.patch("requests.post")
    def test_last_n_days_chart(self, mock_post, recent_statistics_data):
        """Test chart creation with last N days data"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(recent_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with mock.patch("matplotlib.pyplot.bar") as mock_bar:
            result = stats.make_chart("last_n_days_analysis", "bar", days=7)

            assert result == plt
            mock_bar.assert_called_once()

    @mock.patch("requests.post")
    def test_last_n_days_unique_chart(self, mock_post, recent_statistics_data):
        """Test chart creation with last N days unique data"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(recent_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with mock.patch("matplotlib.pyplot.bar") as mock_bar:
            result = stats.make_chart("last_n_days_unique_analysis", "bar", days=5)

            assert result == plt
            mock_bar.assert_called_once()


@pytest.mark.unit
class TestChartErrors:
    """Test suite for chart generation errors"""

    @mock.patch("requests.post")
    def test_make_chart_invalid_data(self, mock_post, sample_statistics_data):
        """Test chart creation with invalid data type"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with pytest.raises(ValueError) as exc_info:
            stats.make_chart("invalid_data", "bar")

        assert "Invalid data type" in str(exc_info.value)

    @mock.patch("requests.post")
    def test_make_chart_invalid_type(self, mock_post, sample_statistics_data):
        """Test chart creation with invalid chart type"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with pytest.raises(Exception) as exc_info:
            stats.make_chart("browsers_analysis", "invalid_chart")

        assert "Invalid chart type" in str(exc_info.value)

    @mock.patch("requests.post")
    def test_chart_with_empty_data(self, mock_post):
        """Test chart generation with empty data"""
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

        # Should not raise an error even with empty data
        with mock.patch("matplotlib.pyplot.bar") as mock_bar:
            result = stats.make_chart("browsers_analysis", "bar")
            assert result == plt
            mock_bar.assert_called_once()


@pytest.mark.unit
@pytest.mark.slow
class TestHeatmaps:
    """Test suite for heatmap functionality"""

    @mock.patch("requests.post")
    def test_make_countries_heatmap_calls_method(
        self, mock_post, sample_statistics_data
    ):
        """Test that countries heatmap method exists and is callable"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        # Test that the method exists and has the expected signature
        assert hasattr(stats, "make_countries_heatmap")
        assert callable(getattr(stats, "make_countries_heatmap"))

        # Test that we can call it with different colormaps without errors
        # We'll mock the actual plotting to avoid matplotlib complexity
        with mock.patch.object(
            stats, "_create_heatmap", return_value=plt
        ) as mock_create:
            result = stats.make_countries_heatmap(cmap="viridis")

            assert result == plt
            mock_create.assert_called_once_with(
                data_analysis=stats.country_analysis,
                title="Countries Heatmap",
                merge_column="NAME",
                cmap="viridis",
            )

    @mock.patch("requests.post")
    def test_make_unique_countries_heatmap_calls_method(
        self, mock_post, sample_statistics_data
    ):
        """Test that unique countries heatmap method exists and is callable"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        # Test that the method exists and has the expected signature
        assert hasattr(stats, "make_unique_countries_heatmap")
        assert callable(getattr(stats, "make_unique_countries_heatmap"))

        # Test that we can call it with different colormaps without errors
        with mock.patch.object(
            stats, "_create_heatmap", return_value=plt
        ) as mock_create:
            result = stats.make_unique_countries_heatmap(cmap="plasma")

            assert result == plt
            mock_create.assert_called_once_with(
                data_analysis=stats.unique_country_analysis,
                title="Unique Countries Heatmap",
                merge_column="NAME",
                cmap="plasma",
            )

    @mock.patch("requests.post")
    def test_heatmap_with_different_colormaps(self, mock_post, sample_statistics_data):
        """Test heatmap creation with different colormap options"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        # Test different valid colormaps
        valid_colormaps = ["YlOrRd", "viridis", "plasma", "inferno", "RdPu_r"]

        with mock.patch.object(
            stats, "_create_heatmap", return_value=plt
        ) as mock_create:
            for cmap in valid_colormaps:
                result = stats.make_countries_heatmap(cmap=cmap)
                assert result == plt

            # Verify _create_heatmap was called for each colormap
            assert mock_create.call_count == len(valid_colormaps)


@pytest.mark.unit
class TestChartCustomization:
    """Test suite for chart customization options"""

    @mock.patch("requests.post")
    def test_chart_with_kwargs(self, mock_post, sample_statistics_data):
        """Test chart creation with additional kwargs"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with mock.patch("matplotlib.pyplot.bar") as mock_bar:
            result = stats.make_chart(
                "browsers_analysis", "bar", color="red", alpha=0.7, width=0.8
            )

            assert result == plt
            # Check that kwargs were passed to the plotting function
            call_args = mock_bar.call_args
            assert "color" in call_args.kwargs
            assert "alpha" in call_args.kwargs
            assert "width" in call_args.kwargs

    @mock.patch("requests.post")
    def test_pie_chart_with_kwargs(self, mock_post, sample_statistics_data):
        """Test pie chart creation with additional kwargs"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with mock.patch("matplotlib.pyplot.pie") as mock_pie:
            result = stats.make_chart(
                "country_analysis", "pie", autopct="%1.1f%%", startangle=90
            )

            assert result == plt
            # Check that kwargs were passed to the plotting function
            call_args = mock_pie.call_args
            assert "autopct" in call_args.kwargs
            assert "startangle" in call_args.kwargs
