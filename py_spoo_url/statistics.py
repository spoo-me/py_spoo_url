from datetime import datetime, timedelta
from typing import Optional, Dict
from ._internal.plotting import make_chart, make_countries_heatmap, make_unique_countries_heatmap
from ._internal.exporters import export_data
from ._internal.api import fetch_statistics


class Statistics:
    def __init__(self, short_code: str, password: Optional[str] = None):
        short_code = short_code.split("/")[-1]
        self.short_code = short_code
        self.password = password
        r = fetch_statistics(self.short_code, self.password)
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

    def make_chart(self, data, chart_type="bar", days=7, **kwargs):
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
        if callable(selected):
            chart_data = selected(days=days)
        else:
            chart_data = selected
        return make_chart(chart_data, chart_type=chart_type, data_label=data, **kwargs)

    def make_countries_heatmap(self, cmap="YlOrRd"):
        return make_countries_heatmap(self.country_analysis, cmap=cmap)

    def make_unique_countries_heatmap(self, cmap="YlOrRd"):
        return make_unique_countries_heatmap(self.unique_country_analysis, cmap=cmap)

    def export_data(self, filename="export.xlsx", filetype="xlsx"):
        return export_data(self.data, filename=filename, filetype=filetype)

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

    def __str__(self) -> str:
        return f"<Statistics {self.short_code}>"

    def __repr__(self) -> str:
        return f"<Statistics {self.short_code}>"
