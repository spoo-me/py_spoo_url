import pandas as pd
import json
import os
import shutil
import zipfile
from typing import Literal
from .utils import create_dataframes_from_data, create_general_info_dataframe, STANDARD_DATAFRAME_CONFIGS


def export_to_excel(data, filename: str = "export.xlsx") -> None:
    # Create all standard DataFrames using utility function
    dataframes = create_dataframes_from_data(data, STANDARD_DATAFRAME_CONFIGS)
    
    # Create general info DataFrame
    df_general_info = create_general_info_dataframe(data, "URL")
    
    # Excel sheet name mapping
    sheet_mapping = {
        "df_browser": "Browser",
        "df_counter": "Counter", 
        "df_country": "Country",
        "df_os_name": "OS_Name",
        "df_referrer": "Referrer",
        "df_unique_browser": "Unique_Browser",
        "df_unique_counter": "Unique_Counter",
        "df_unique_country": "Unique_Country",
        "df_unique_os_name": "Unique_OS_Name",
        "df_unique_referrer": "Unique_Referrer",
    }
    
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        # Write all standard DataFrames
        for df_name, sheet_name in sheet_mapping.items():
            if df_name in dataframes:
                dataframes[df_name].to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Write general info
        df_general_info.to_excel(writer, sheet_name="General_Info", index=False)
    
    print(f"Data successfully written to {filename}")


def export_to_csv(data, filename: str = "export.csv") -> None:
    csv_directory = "csv_files"
    os.makedirs(csv_directory, exist_ok=True)
    
    # Create all standard DataFrames using utility function
    dataframes = create_dataframes_from_data(data, STANDARD_DATAFRAME_CONFIGS)
    
    # Create general info DataFrame (with empty string for URL column in CSV)
    df_general_info = create_general_info_dataframe(data, "")
    
    # CSV file name mapping
    csv_mapping = {
        "df_browser": "browser.csv",
        "df_counter": "counter.csv",
        "df_country": "country.csv",
        "df_os_name": "os_name.csv",
        "df_referrer": "referrer.csv",
        "df_unique_browser": "unique_browser.csv",
        "df_unique_counter": "unique_counter.csv",
        "df_unique_country": "unique_country.csv",
        "df_unique_os_name": "unique_os_name.csv",
        "df_unique_referrer": "unique_referrer.csv",
    }
    
    # Save all DataFrames to CSV files
    for df_name, csv_filename in csv_mapping.items():
        if df_name in dataframes:
            dataframes[df_name].to_csv(os.path.join(csv_directory, csv_filename), index=False)
    
    # Save general info
    df_general_info.to_csv(os.path.join(csv_directory, "general_info.csv"), index=False)
    
    # Create zip file
    with zipfile.ZipFile(f"{filename}.zip", "w") as zipf:
        for root, dirs, files in os.walk(csv_directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, csv_directory)
                zipf.write(file_path, arcname=arcname)
    
    # Clean up temporary directory
    shutil.rmtree(csv_directory)
    print(f"Data successfully written to {filename}.zip")


def export_to_json(data, filename: str = "export.json") -> None:
    with open(filename, "w") as w:
        w.write(json.dumps(data, indent=4))
    print(f"Data successfully written to {filename}")


def export_data(
    data,
    filename: str = "export.xlsx",
    filetype: Literal["csv", "xlsx", "json"] = "xlsx",
) -> None:
    if filetype == "xlsx":
        export_to_excel(data, filename)
    elif filetype == "json":
        export_to_json(data, filename)
    elif filetype == "csv":
        export_to_csv(data, filename)
    else:
        raise ValueError("Invalid file type. Choose either 'csv', 'json' or 'xlsx'.")
