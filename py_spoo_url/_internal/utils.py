import pandas as pd
from typing import Dict, List, Tuple


def create_dataframes_from_data(data: Dict, dataframe_configs: List[Tuple[str, str, List[str]]]) -> Dict[str, pd.DataFrame]:
    """
    Create multiple DataFrames from data dictionary based on configuration.
    
    Args:
        data: Raw data dictionary
        dataframe_configs: List of tuples (data_key, df_name, column_names)
    
    Returns:
        Dictionary mapping DataFrame names to DataFrames
    """
    dataframes = {}
    for data_key, df_name, columns in dataframe_configs:
        if data_key in data:
            dataframes[df_name] = pd.DataFrame(data[data_key].items(), columns=columns)
    return dataframes


def create_general_info_dataframe(data: Dict, url_column_name: str = "URL") -> pd.DataFrame:
    """
    Create the general info DataFrame with standardized structure.
    
    Args:
        data: Raw data dictionary
        url_column_name: Name for the URL column (use "" for CSV export)
    
    Returns:
        DataFrame with general information
    """
    return pd.DataFrame({
        "TOTAL CLICKS": [data["total-clicks"]],
        "TOTAL UNIQUE CLICKS": [data["total_unique_clicks"]],
        url_column_name: [data["url"]],
        "SHORT CODE": [data["_id"]],
        "MAX CLICKS": [data["max-clicks"]],
        "PASSWORD": [data["password"]],
        "CREATION DATE": [data["creation-date"]],
        "EXPIRED": [data["expired"]],
        "AVERAGE DAILY CLICKS": [data["average_daily_clicks"]],
        "AVERAGE MONTHLY CLICKS": [data["average_monthly_clicks"]],
        "AVERAGE WEEKLY CLICKS": [data["average_weekly_clicks"]],
        "LAST CLICK": [data["last-click"]],
        "LAST CLICK BROSWER": [data["last-click-browser"]],
        "LAST CLICK OS": [data["last-click-os"]],
    })


# Configuration for standard DataFrames
STANDARD_DATAFRAME_CONFIGS = [
    ("browser", "df_browser", ["Browser", "Count"]),
    ("counter", "df_counter", ["Date", "Count"]),
    ("country", "df_country", ["Country", "Count"]),
    ("os_name", "df_os_name", ["OS_Name", "Count"]),
    ("referrer", "df_referrer", ["Referrer", "Count"]),
    ("unique_browser", "df_unique_browser", ["Browser", "Count"]),
    ("unique_counter", "df_unique_counter", ["Date", "Count"]),
    ("unique_country", "df_unique_country", ["Country", "Count"]),
    ("unique_os_name", "df_unique_os_name", ["OS_Name", "Count"]),
    ("unique_referrer", "df_unique_referrer", ["Referrer", "Count"]),
] 