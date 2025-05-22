import matplotlib.pyplot as plt  # type: ignore
import matplotlib  # type: ignore
from mpl_toolkits.axes_grid1 import make_axes_locatable  # type: ignore
import geopandas as gpd  # type: ignore
from typing import Literal, Dict


def make_chart(
    chart_data: Dict,
    chart_type: Literal["bar", "pie", "line", "scatter", "hist", "box", "area"] = "bar",
    data_label: str = None,
    **kwargs,
) -> plt.Figure:
    matplotlib.rcParams["font.size"] = 15
    matplotlib.rcParams["axes.labelcolor"] = "Black"

    if chart_type == "bar":
        plt.bar(chart_data.keys(), chart_data.values(), **kwargs)
        if data_label in [
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
    data_analysis: Dict[str, int],
    title: str,
    merge_column: str = "NAME",
    cmap: Literal["YlOrRd", "viridis", "plasma", "inferno", "RdPu_r"] = "YlOrRd",
) -> plt.Figure:
    matplotlib.rcParams["font.size"] = 15
    matplotlib.rcParams["axes.labelcolor"] = "White"
    world = gpd.read_file("py_spoo_url/data/ne_110m_admin_0_countries.zip")
    world = world.merge(
        gpd.GeoDataFrame(data_analysis.items(), columns=["Country", "Value"]),
        how="left",
        left_on=merge_column,
        right_on="Country",
    )
    fig, ax = plt.subplots(
        1, 1, figsize=(15, 10), facecolor=(32 / 255, 34 / 255, 37 / 255, 0.5)
    )
    plt.subplots_adjust(left=0.05, right=0.90, bottom=0.05, top=0.95)
    for spine in ax.spines.values():
        spine.set_color((46 / 255, 48 / 255, 53 / 255))
        spine.set_linewidth(2)
    ax.tick_params(labelcolor="white")
    world.boundary.plot(ax=ax, linewidth=1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    p = world.plot(
        column="Value",
        ax=ax,
        legend=True,
        cax=cax,
        cmap=cmap,
        edgecolor=None,
        legend_kwds={"label": "Clicks"},
        alpha=0.9,
    )
    p.set_facecolor((32 / 255, 34 / 255, 37 / 255, 0.5))
    cbax = cax
    cbax.tick_params(labelcolor="white")
    plt.suptitle(title, x=0.5, y=0.95, fontsize=20, fontweight=3, color="white")
    return plt


def make_countries_heatmap(
    country_analysis: Dict[str, int],
    cmap: Literal["YlOrRd", "viridis", "plasma", "inferno", "RdPu_r"] = "YlOrRd",
) -> plt.Figure:
    return _create_heatmap(
        data_analysis=country_analysis,
        title="Countries Heatmap",
        merge_column="NAME",
        cmap=cmap,
    )


def make_unique_countries_heatmap(
    unique_country_analysis: Dict[str, int],
    cmap: Literal["YlOrRd", "viridis", "plasma", "inferno", "RdPu_r"] = "YlOrRd",
) -> plt.Figure:
    return _create_heatmap(
        data_analysis=unique_country_analysis,
        title="Unique Countries Heatmap",
        merge_column="NAME",
        cmap=cmap,
    )
