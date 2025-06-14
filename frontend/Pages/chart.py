import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from difflib import get_close_matches


def application_by_field_chart(df: pd.DataFrame):
    """Bar chart: Total seats by education area."""
    return px.bar(
        df,
        x="Sökt utbildningsområde",
        y="Sökt antal platser 2024",
        title="Total Seats by Education Area",
        labels={"Sökt utbildningsområde": "Education Area", "Sökt antal platser 2024": "Seats"},
    )


def students_over_time_map(df_grouped: pd.DataFrame, geojson_data: dict, year: int, area: str):
    """Choropleth map of qualified students by region and year."""
    fig = px.choropleth(
        df_grouped,
        geojson=geojson_data,
        featureidkey="properties.name",
        locations="region (hemlän)",
        color="Antal behöriga",
        color_continuous_scale="Viridis",
        title=f"Qualified Students in {area} - {year}"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    return fig


def seats_by_region_sunburst(df: pd.DataFrame):
    """Sunburst chart of seats by Län, Kommun, and Anordnare."""
    return px.sunburst(
        df,
        path=["Län", "Kommun", "Anordnare namn"],
        values="Sökt antal platser 2024",
        title="Seats by Region"
    )


def statsbidrag_chart(df: pd.DataFrame, multiplier: int = 7000):
    """Bar chart of estimated government grants (Statsbidrag)."""
    df["Statsbidrag"] = df["YH-poäng"] * multiplier
    return px.bar(
        df,
        x="Sökt utbildningsområde",
        y="Statsbidrag",
        title=f"Statsbidrag per Education Area (YH-poäng × {multiplier})",
        labels={"Sökt utbildningsområde": "Education Area", "Statsbidrag": "SEK"}
    )


def trend_over_time_chart(df: pd.DataFrame):
    """Line chart showing application trends by field over years."""
    return px.line(
        df,
        x="År",
        y="Platser",
        color="Sökt utbildningsområde",
        title="Trends in Applications Over Time"
    )


def choropleth_mapbox_chart(df: pd.DataFrame, geojson_data: dict, selected_year: int):
    """Mapbox choropleth using region codes and dropdown year selection."""
    # Create region code mapping from GeoJSON
    region_codes = {
        feature["properties"]["name"]: feature["properties"]["ref:se:länskod"]
        for feature in geojson_data["features"]
    }

    # Fuzzy match regions in the data
    region_codes_map = []
    for name in df["region (hemlän)"]:
        match = get_close_matches(name, region_codes.keys(), n=1)
        region_codes_map.append(region_codes[match[0]] if match else None)

    df["Länskod"] = region_codes_map
    df["log_val"] = np.log(df["Antal behöriga"] + 1)

    # Filter by year
    df_year = df[df["År"] == selected_year]

    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=df_year["Länskod"],
        z=df_year["log_val"],
        featureidkey="properties.ref:se:länskod",
        colorscale="YlGnBu",
        marker_line_width=0.3,
        text=df_year["region (hemlän)"],
        customdata=df_year["Antal behöriga"],
        hovertemplate="<b>%{text}</b><br>Students: %{customdata}<extra></extra>"
    ))

    fig.update_layout(
        mapbox=dict(style="carto-positron", zoom=3.3, center=dict(lat=62.7, lon=13.9)),
        title=f"Qualified Students per Region ({selected_year})",
        width=800,
        height=600,
        margin=dict(r=0, t=40, l=0, b=0)
    )
    return fig


def empty_figure():
    """Returns an empty Plotly figure."""
    return go.Figure()

import plotly.express as px

# added newly

def create_top_20_schools_chart(df):
    top_schools_df = get_top_20_schools_by_applications(df)
    fig = px.bar(
        top_schools_df,
        x="Antal ansökningar",
        y="Skola",
        orientation="h",
        title="Topp 20 skolor baserat på antal ansökningar",
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig
