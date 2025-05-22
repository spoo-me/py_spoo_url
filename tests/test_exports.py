"""
Tests for data export functionality.
"""

import pytest
import unittest.mock as mock
import json
import tempfile
import os
import zipfile
import pandas as pd
from py_spoo_url import Statistics


@pytest.mark.unit
class TestJSONExport:
    """Test suite for JSON export functionality"""

    @mock.patch("requests.post")
    def test_export_to_json(self, mock_post, sample_statistics_data):
        """Test JSON export functionality"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as f:
            temp_filename = f.name

        try:
            stats.export_data(filename=temp_filename, filetype="json")

            # Verify file was created and contains correct data
            with open(temp_filename, "r") as f:
                exported_data = json.load(f)

            assert exported_data == sample_statistics_data
        finally:
            os.unlink(temp_filename)

    @mock.patch("requests.post")
    def test_export_to_json_custom_filename(self, mock_post, sample_statistics_data):
        """Test JSON export with custom filename"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        custom_filename = "custom_export.json"

        try:
            stats.export_data(filename=custom_filename, filetype="json")

            # Verify file was created
            assert os.path.exists(custom_filename)

            # Verify contents
            with open(custom_filename, "r") as f:
                exported_data = json.load(f)

            assert exported_data == sample_statistics_data
        finally:
            if os.path.exists(custom_filename):
                os.unlink(custom_filename)


@pytest.mark.unit
class TestExcelExport:
    """Test suite for Excel export functionality"""

    @mock.patch("requests.post")
    def test_export_to_excel(self, mock_post, sample_statistics_data):
        """Test Excel export functionality"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            temp_filename = f.name

        try:
            stats.export_data(filename=temp_filename, filetype="xlsx")

            # Verify file was created
            assert os.path.exists(temp_filename)
            assert os.path.getsize(temp_filename) > 0

            # Try to read the Excel file to verify it's valid
            with pd.ExcelFile(temp_filename) as excel_file:
                sheet_names = excel_file.sheet_names
                expected_sheets = [
                    "Browser",
                    "Counter",
                    "Country",
                    "OS_Name",
                    "Referrer",
                    "Unique_Browser",
                    "Unique_Counter",
                    "Unique_Country",
                    "Unique_OS_Name",
                    "Unique_Referrer",
                    "General_Info",
                ]

                for sheet in expected_sheets:
                    assert sheet in sheet_names

        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    @mock.patch("requests.post")
    def test_export_to_excel_content_verification(
        self, mock_post, sample_statistics_data
    ):
        """Test Excel export content verification"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            temp_filename = f.name

        try:
            stats.export_data(filename=temp_filename, filetype="xlsx")

            # Read and verify specific sheet content
            browser_df = pd.read_excel(temp_filename, sheet_name="Browser")
            assert len(browser_df) == 3  # Chrome, Firefox, Safari
            assert "Browser" in browser_df.columns
            assert "Count" in browser_df.columns

            # Verify browser data
            browser_data = dict(zip(browser_df["Browser"], browser_df["Count"]))
            expected_browser_data = {"Chrome": 500, "Firefox": 300, "Safari": 200}
            assert browser_data == expected_browser_data

            # Verify general info sheet
            general_df = pd.read_excel(temp_filename, sheet_name="General_Info")
            assert general_df["TOTAL CLICKS"].iloc[0] == 1000
            assert general_df["TOTAL UNIQUE CLICKS"].iloc[0] == 750

        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


@pytest.mark.unit
class TestCSVExport:
    """Test suite for CSV export functionality"""

    @mock.patch("requests.post")
    def test_export_to_csv(self, mock_post, sample_statistics_data):
        """Test CSV export functionality"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        zip_filename = "test_export.zip"

        try:
            stats.export_data(filename="test_export", filetype="csv")

            # Verify ZIP file was created
            assert os.path.exists(zip_filename)
            assert os.path.getsize(zip_filename) > 0

            # Verify ZIP file contents
            with zipfile.ZipFile(zip_filename, "r") as zip_file:
                file_list = zip_file.namelist()
                expected_files = [
                    "browser.csv",
                    "counter.csv",
                    "country.csv",
                    "os_name.csv",
                    "referrer.csv",
                    "unique_browser.csv",
                    "unique_counter.csv",
                    "unique_country.csv",
                    "unique_os_name.csv",
                    "unique_referrer.csv",
                    "general_info.csv",
                ]

                for expected_file in expected_files:
                    assert expected_file in file_list

        finally:
            if os.path.exists(zip_filename):
                os.unlink(zip_filename)

    @mock.patch("requests.post")
    def test_export_to_csv_content_verification(
        self, mock_post, sample_statistics_data
    ):
        """Test CSV export content verification"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        zip_filename = "test_content_export.zip"

        try:
            stats.export_data(filename="test_content_export", filetype="csv")

            # Extract and verify specific CSV content
            with zipfile.ZipFile(zip_filename, "r") as zip_file:
                # Read browser CSV
                with zip_file.open("browser.csv") as browser_file:
                    browser_df = pd.read_csv(browser_file)
                    assert len(browser_df) == 3
                    assert "Browser" in browser_df.columns
                    assert "Count" in browser_df.columns

                    # Verify browser data
                    browser_data = dict(zip(browser_df["Browser"], browser_df["Count"]))
                    expected_browser_data = {
                        "Chrome": 500,
                        "Firefox": 300,
                        "Safari": 200,
                    }
                    assert browser_data == expected_browser_data

                # Read general info CSV
                with zip_file.open("general_info.csv") as general_file:
                    general_df = pd.read_csv(general_file)
                    assert general_df["TOTAL CLICKS"].iloc[0] == 1000
                    assert general_df["TOTAL UNIQUE CLICKS"].iloc[0] == 750

        finally:
            if os.path.exists(zip_filename):
                os.unlink(zip_filename)


@pytest.mark.unit
class TestExportErrors:
    """Test suite for export error handling"""

    @mock.patch("requests.post")
    def test_export_invalid_filetype(self, mock_post, sample_statistics_data):
        """Test export with invalid file type"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with pytest.raises(ValueError) as exc_info:
            stats.export_data(filename="test.invalid", filetype="invalid")

        assert "Invalid file type" in str(exc_info.value)

    @mock.patch("requests.post")
    def test_export_default_parameters(self, mock_post, sample_statistics_data):
        """Test export with default parameters"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        try:
            # Should use default filename and xlsx format
            stats.export_data()

            # Verify default Excel file was created
            assert os.path.exists("export.xlsx")
            assert os.path.getsize("export.xlsx") > 0

        finally:
            if os.path.exists("export.xlsx"):
                os.unlink("export.xlsx")

    @mock.patch("requests.post")
    @mock.patch("builtins.open", side_effect=PermissionError("Permission denied"))
    def test_export_permission_error(
        self, mock_open, mock_post, sample_statistics_data
    ):
        """Test export with permission error"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        with pytest.raises(PermissionError):
            stats.export_data(filename="protected_file.json", filetype="json")


@pytest.mark.unit
class TestExportMethods:
    """Test suite for specific export methods"""

    @mock.patch("requests.post")
    def test_export_to_excel_method(self, mock_post, sample_statistics_data):
        """Test direct export_to_excel method"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        filename = "direct_excel_export.xlsx"

        try:
            stats.export_to_excel(filename)

            # Verify file was created
            assert os.path.exists(filename)
            assert os.path.getsize(filename) > 0

        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    @mock.patch("requests.post")
    def test_export_to_csv_method(self, mock_post, sample_statistics_data):
        """Test direct export_to_csv method"""
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(sample_statistics_data)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        base_filename = "direct_csv_export"
        zip_filename = f"{base_filename}.zip"

        try:
            stats.export_to_csv(base_filename)

            # Verify ZIP file was created
            assert os.path.exists(zip_filename)
            assert os.path.getsize(zip_filename) > 0

        finally:
            if os.path.exists(zip_filename):
                os.unlink(zip_filename)


@pytest.mark.unit
class TestExportEdgeCases:
    """Test suite for export edge cases"""

    @mock.patch("requests.post")
    def test_export_with_empty_data(self, mock_post):
        """Test export with empty statistics data"""
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

        filename = "empty_data_export.json"

        try:
            # Should handle empty data gracefully
            stats.export_data(filename=filename, filetype="json")

            # Verify file was created
            assert os.path.exists(filename)

            # Verify contents
            with open(filename, "r") as f:
                exported_data = json.load(f)

            assert exported_data == empty_data

        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    @mock.patch("requests.post")
    def test_export_with_special_characters(self, mock_post):
        """Test export with special characters in data"""
        special_data = {
            "url": "https://example.com/测试",
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
            "browser": {"Chrome": 500, "Firefox Français": 300, "Safari 中文": 200},
            "os_name": {"Windows": 600, "macOS": 250, "Linux": 150},
            "country": {"USA": 400, "UK": 300, "中国": 300},
            "referrer": {"Google": 500, "Direct": 300, "Twitter": 200},
            "counter": {"2024-01-01": 50},
            "unique_browser": {"Chrome": 400},
            "unique_os_name": {"Windows": 450},
            "unique_country": {"USA": 300},
            "unique_referrer": {"Google": 400},
            "unique_counter": {"2024-01-01": 40},
            "expired": False,
            "password": None,
            "_id": "abc123",
        }

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(special_data, ensure_ascii=False)
        mock_post.return_value = mock_response

        stats = Statistics("abc123")

        filename = "special_chars_export.json"

        try:
            stats.export_data(filename=filename, filetype="json")

            # Verify file was created and contains special characters
            assert os.path.exists(filename)

            with open(filename, "r", encoding="utf-8") as f:
                exported_data = json.load(f)

            assert "测试" in exported_data["url"]
            assert "中国" in exported_data["country"]
            assert "Firefox Français" in exported_data["browser"]

        finally:
            if os.path.exists(filename):
                os.unlink(filename)
