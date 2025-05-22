import matplotlib.pyplot as plt  # type: ignore
import matplotlib  # type: ignore
import requests  # type: ignore
import json
from datetime import datetime, timedelta
import geopandas as gpd  # type: ignore
from mpl_toolkits.axes_grid1 import make_axes_locatable  # type: ignore
from typing import Literal, Optional, Dict, Any
import pandas as pd  # type: ignore
import os
import shutil
import zipfile


class Statistics:
    def __init__(self, short_code: str, password: Optional[str] = None):
        short_code = short_code.split("/")[-1]
        self.short_code = short_code
        self.password = password
        self._url = "https://spoo.me/stats/"

        self.get()

    def get(self) -> Any:
        url = f"{self._url}{self.short_code}"

        params = {"password": self.password} if self.password else None

        r = requests.post(url, data=params)

        if r.status_code == 200:
            r = json.loads(r.text)

            self.data = r

            self.long_url = r["url"]
            self.average_daily_clicks = r["average_daily_clicks"]
            self.average_monthly_clicks = r["average_monthly_clicks"]
            self.average_weekly_clicks = r["average_weekly_clicks"]

            self.total_clicks = r["total-clicks"]
            self.total_unique_clicks = r["total_unique_clicks"]
            self.max_clicks = r["max-clicks"]

            self.last_click = r["last-click"]
            self.last_click_browser = r["last-click-browser"]
            self.last_click_platform = r["last-click-os"]

            self.created_at = r["creation-date"]
            self.creation_time = r.get("creation-time", None)

            self.browsers_analysis = r["browser"]
            self.platforms_analysis = r["os_name"]
            self.country_analysis = r["country"]
            self.referrers_analysis = r["referrer"]
            self.clicks_analysis = r["counter"]

            self.unique_browsers_analysis = r["unique_browser"]
            self.unique_platforms_analysis = r["unique_os_name"]
            self.unique_country_analysis = r["unique_country"]
            self.unique_referrers_analysis = r["unique_referrer"]
            self.unique_clicks_analysis = r["unique_counter"]

            self.expired = r["expired"]
            self.password = r.get("password", None)

            return r

        else:
            raise Exception(f"Error {r.status_code}: {r.text}")

    def make_chart(
        self,
        data: Literal[
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
            "last_n_days_analysis",
            "last_n_days_unique_analysis",
        ],
        chart_type: Literal[
            "bar", "pie", "line", "scatter", "hist", "box", "area"
        ] = "bar",
        days: int = 7,
        **kwargs,
    ) -> plt.Figure:
        data_methods = {
            "browsers_analysis": self.browsers_analysis,
            "platforms_analysis": self.platforms_analysis,
            "country_analysis": self.country_analysis,
            "referrers_analysis": self.referrers_analysis,
            "clicks_analysis": self.clicks_analysis,
            "unique_browsers_analysis": self.unique_browsers_analysis,
            "unique_platforms_analysis": self.unique_platforms_analysis,
            "unique_country_analysis": self.unique_country_analysis,
            "unique_referrers_analysis": self.unique_referrers_analysis,
            "unique_clicks_analysis": self.unique_clicks_analysis,
            "last_n_days_analysis": self.last_n_days_analysis,
            "last_n_days_unique_analysis": self.last_n_days_unique_analysis,
        }
        try:
            selected = data_methods[data]
        except KeyError:
            raise ValueError(
                "Invalid data type. Valid data types are: {}".format(
                    list(data_methods.keys())
                )
            )

        matplotlib.rcParams["font.size"] = 15
        matplotlib.rcParams["axes.labelcolor"] = "Black"

        if callable(selected):
            chart_data = selected(days=days)
        else:
            chart_data = selected

        if chart_type == "bar":
            plt.bar(chart_data.keys(), chart_data.values(), **kwargs)
            if data in [
                "last_n_days_analysis",
                "clicks_analysis",
                "unique_clicks_analysis",
            ]:
                plt.xticks(rotation=90)
        elif chart_type == "pie":
            plt.pie(chart_data.values(), labels=chart_data.keys(), **kwargs)
        elif chart_type == "line":
            plt.plot(chart_data.keys(), chart_data.values(), **kwargs)
        elif chart_type == "scatter":
            plt.scatter(chart_data.keys(), chart_data.values(), **kwargs)
        elif chart_type == "hist":
            plt.hist(list(chart_data.values()), **kwargs)
        elif chart_type == "box":
            plt.boxplot(list(chart_data.values()), **kwargs)
        elif chart_type == "area":
            plt.stackplot(chart_data.keys(), chart_data.values(), **kwargs)
        else:
            raise Exception(
                "Invalid chart type. Valid chart types are: bar, pie, line, scatter, hist, box, area"
            )

        return plt

    def _create_heatmap(
        self,
        data_analysis: Dict[str, int],
        title: str,
        merge_column: str = "NAME",
        cmap: Literal["YlOrRd", "viridis", "plasma", "inferno", "RdPu_r"] = "YlOrRd",
    ) -> plt.Figure:
        """Common function to create country heatmaps"""
        matplotlib.rcParams["font.size"] = 15
        matplotlib.rcParams["axes.labelcolor"] = "White"

        world = gpd.read_file("py_spoo_url/data/ne_110m_admin_0_countries.zip")

        world = world.merge(
            gpd.GeoDataFrame(data_analysis.items(), columns=["Country", "Value"]),
            how="left",
            left_on=merge_column,
            right_on="Country",
        )

        # Create a figure and axis (single figure creation)
        fig, ax = plt.subplots(
            1, 1, figsize=(15, 10), facecolor=(32 / 255, 34 / 255, 37 / 255, 0.5)
        )

        # Apply subplot adjustments to the created figure
        plt.subplots_adjust(left=0.05, right=0.90, bottom=0.05, top=0.95)

        for spine in ax.spines.values():
            spine.set_color((46 / 255, 48 / 255, 53 / 255))
            spine.set_linewidth(2)

        ax.tick_params(labelcolor="white")

        # Plot the world map
        world.boundary.plot(ax=ax, linewidth=1)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)

        # Plot the heatmap
        p = world.plot(
            column="Value",
            ax=ax,
            legend=True,
            cax=cax,
            cmap=cmap,
            edgecolor=None,
            legend_kwds={
                "label": "Clicks",
            },
            alpha=0.9,
        )
        p.set_facecolor((32 / 255, 34 / 255, 37 / 255, 0.5))
        cbax = cax
        cbax.tick_params(labelcolor="white")

        # Set plot title
        plt.suptitle(title, x=0.5, y=0.95, fontsize=20, fontweight=3, color="white")

        return plt

    def make_countries_heatmap(
        self,
        cmap: Literal["YlOrRd", "viridis", "plasma", "inferno", "RdPu_r"] = "YlOrRd",
    ) -> plt.Figure:
        return self._create_heatmap(
            data_analysis=self.country_analysis,
            title="Countries Heatmap",
            merge_column="NAME",
            cmap=cmap,
        )

    def make_unique_countries_heatmap(
        self,
        cmap: Literal["YlOrRd", "viridis", "plasma", "inferno", "RdPu_r"] = "YlOrRd",
    ) -> plt.Figure:
        return self._create_heatmap(
            data_analysis=self.unique_country_analysis,
            title="Unique Countries Heatmap",
            merge_column="NAME",
            cmap=cmap,
        )

    def last_n_days_analysis(self, days: int = 7) -> Dict[str, int]:
        clicks_analysis_dates = {
            date: clicks
            for date, clicks in self.clicks_analysis.items()
            if datetime.strptime(date, "%Y-%m-%d")
            >= (datetime.now() - timedelta(days=days)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        }
        if not clicks_analysis_dates:
            raise ValueError(f"No data available for the last {days} days.")
        return clicks_analysis_dates

    def last_n_days_unique_analysis(self, days: int = 7) -> Dict[str, int]:
        unique_clicks_analysis_dates = {
            date: clicks
            for date, clicks in self.unique_clicks_analysis.items()
            if datetime.strptime(date, "%Y-%m-%d")
            >= (datetime.now() - timedelta(days=days)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        }
        if not unique_clicks_analysis_dates:
            raise ValueError(f"No data available for the last {days} days.")
        return unique_clicks_analysis_dates

    def export_data(
        self,
        filename: str = "export.xlsx",
        filetype: Literal["csv", "xlsx", "json"] = "xlsx",
    ) -> None:
        if filetype == "xlsx":
            self.export_to_excel(filename)
        elif filetype == "json":
            with open(filename, "w") as w:
                w.write(json.dumps(self.data, indent=4))
        elif filetype == "csv":
            self.export_to_csv(filename)
        else:
            raise ValueError(
                "Invalid file type. Choose either 'csv', 'json' or 'xlsx'."
            )

    def export_to_excel(self, filename: str = "export.xlsx") -> None:
        df_browser = pd.DataFrame(
            self.data["browser"].items(), columns=["Browser", "Count"]
        )
        df_counter = pd.DataFrame(
            self.data["counter"].items(), columns=["Date", "Count"]
        )
        df_country = pd.DataFrame(
            self.data["country"].items(), columns=["Country", "Count"]
        )
        df_os_name = pd.DataFrame(
            self.data["os_name"].items(), columns=["OS_Name", "Count"]
        )
        df_referrer = pd.DataFrame(
            self.data["referrer"].items(), columns=["Referrer", "Count"]
        )
        df_unique_browser = pd.DataFrame(
            self.data["unique_browser"].items(), columns=["Browser", "Count"]
        )
        df_unique_counter = pd.DataFrame(
            self.data["unique_counter"].items(), columns=["Date", "Count"]
        )
        df_unique_country = pd.DataFrame(
            self.data["unique_country"].items(), columns=["Country", "Count"]
        )
        df_unique_os_name = pd.DataFrame(
            self.data["unique_os_name"].items(), columns=["OS_Name", "Count"]
        )
        df_unique_referrer = pd.DataFrame(
            self.data["unique_referrer"].items(), columns=["Referrer", "Count"]
        )

        df_general_info = pd.DataFrame(
            {
                "TOTAL CLICKS": [self.data["total-clicks"]],
                "TOTAL UNIQUE CLICKS": [self.data["total_unique_clicks"]],
                "URL": [self.data["url"]],
                "SHORT CODE": [self.data["_id"]],
                "MAX CLICKS": [self.data["max-clicks"]],
                "PASSWORD": [self.data["password"]],
                "CREATION DATE": [self.data["creation-date"]],
                "EXPIRED": [self.data["expired"]],
                "AVERAGE DAILY CLICKS": [self.data["average_daily_clicks"]],
                "AVERAGE MONTHLY CLICKS": [self.data["average_monthly_clicks"]],
                "AVERAGE WEEKLY CLICKS": [self.data["average_weekly_clicks"]],
                "LAST CLICK": [self.data["last-click"]],
                "LAST CLICK BROSWER": [self.data["last-click-browser"]],
                "LAST CLICK OS": [self.data["last-click-os"]],
            }
        )

        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            df_browser.to_excel(writer, sheet_name="Browser", index=False)
            df_counter.to_excel(writer, sheet_name="Counter", index=False)
            df_country.to_excel(writer, sheet_name="Country", index=False)
            df_os_name.to_excel(writer, sheet_name="OS_Name", index=False)
            df_referrer.to_excel(writer, sheet_name="Referrer", index=False)
            df_unique_browser.to_excel(writer, sheet_name="Unique_Browser", index=False)
            df_unique_counter.to_excel(writer, sheet_name="Unique_Counter", index=False)
            df_unique_country.to_excel(writer, sheet_name="Unique_Country", index=False)
            df_unique_os_name.to_excel(writer, sheet_name="Unique_OS_Name", index=False)
            df_unique_referrer.to_excel(
                writer, sheet_name="Unique_Referrer", index=False
            )

            df_general_info.to_excel(writer, sheet_name="General_Info", index=False)

        print(f"Data successfully written to {filename}")

    def export_to_csv(self, filename: str = "export.csv") -> None:
        # Create a directory to store CSV files
        csv_directory = "csv_files"
        os.makedirs(csv_directory, exist_ok=True)

        df_browser = pd.DataFrame(
            self.data["browser"].items(), columns=["Browser", "Count"]
        )
        df_counter = pd.DataFrame(
            self.data["counter"].items(), columns=["Date", "Count"]
        )
        df_country = pd.DataFrame(
            self.data["country"].items(), columns=["Country", "Count"]
        )
        df_os_name = pd.DataFrame(
            self.data["os_name"].items(), columns=["OS_Name", "Count"]
        )
        df_referrer = pd.DataFrame(
            self.data["referrer"].items(), columns=["Referrer", "Count"]
        )
        df_unique_browser = pd.DataFrame(
            self.data["unique_browser"].items(), columns=["Browser", "Count"]
        )
        df_unique_counter = pd.DataFrame(
            self.data["unique_counter"].items(), columns=["Date", "Count"]
        )
        df_unique_country = pd.DataFrame(
            self.data["unique_country"].items(), columns=["Country", "Count"]
        )
        df_unique_os_name = pd.DataFrame(
            self.data["unique_os_name"].items(), columns=["OS_Name", "Count"]
        )
        df_unique_referrer = pd.DataFrame(
            self.data["unique_referrer"].items(), columns=["Referrer", "Count"]
        )

        df_general_info = pd.DataFrame(
            {
                "TOTAL CLICKS": [self.data["total-clicks"]],
                "TOTAL UNIQUE CLICKS": [self.data["total_unique_clicks"]],
                "": [self.data["url"]],
                "SHORT CODE": [self.data["_id"]],
                "MAX CLICKS": [self.data["max-clicks"]],
                "PASSWORD": [self.data["password"]],
                "CREATION DATE": [self.data["creation-date"]],
                "EXPIRED": [self.data["expired"]],
                "AVERAGE DAILY CLICKS": [self.data["average_daily_clicks"]],
                "AVERAGE MONTHLY CLICKS": [self.data["average_monthly_clicks"]],
                "AVERAGE WEEKLY CLICKS": [self.data["average_weekly_clicks"]],
                "LAST CLICK": [self.data["last-click"]],
                "LAST CLICK BROSWER": [self.data["last-click-browser"]],
                "LAST CLICK OS": [self.data["last-click-os"]],
            }
        )

        # Save DataFrames to CSV in the directory
        df_browser.to_csv(os.path.join(csv_directory, "browser.csv"), index=False)
        df_counter.to_csv(os.path.join(csv_directory, "counter.csv"), index=False)
        df_country.to_csv(os.path.join(csv_directory, "country.csv"), index=False)
        df_os_name.to_csv(os.path.join(csv_directory, "os_name.csv"), index=False)
        df_referrer.to_csv(os.path.join(csv_directory, "referrer.csv"), index=False)
        df_unique_browser.to_csv(
            os.path.join(csv_directory, "unique_browser.csv"), index=False
        )
        df_unique_counter.to_csv(
            os.path.join(csv_directory, "unique_counter.csv"), index=False
        )
        df_unique_country.to_csv(
            os.path.join(csv_directory, "unique_country.csv"), index=False
        )
        df_unique_os_name.to_csv(
            os.path.join(csv_directory, "unique_os_name.csv"), index=False
        )
        df_unique_referrer.to_csv(
            os.path.join(csv_directory, "unique_referrer.csv"), index=False
        )

        df_general_info.to_csv(
            os.path.join(csv_directory, "general_info.csv"), index=False
        )

        # Create a zip file
        with zipfile.ZipFile(f"{filename}.zip", "w") as zipf:
            for root, dirs, files in os.walk(csv_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, csv_directory)
                    zipf.write(file_path, arcname=arcname)

        # Remove the temporary directory
        shutil.rmtree(csv_directory)

        print(f"Data successfully written to {filename}.zip")

    def __str__(self) -> str:
        return f"<Statistics {self.short_code}>"

    def __repr__(self) -> str:
        return f"<Statistics {self.short_code}>"
