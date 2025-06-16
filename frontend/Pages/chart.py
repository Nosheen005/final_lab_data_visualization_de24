import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from difflib import get_close_matches

from backend.data_processing import df_combined, df_regions, region_geojson
geojson_data = region_geojson



category_column_medel = "Sökt utbildningsområde"  # or whatever your correct column name is



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


# added newly
from backend.data_processing import get_top_20_schools_by_applications


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

# fixed 
def plot_statsbidrag_over_time(df_combined):
    df_grouped = df_combined.groupby("År")["Statsbidrag"].sum().reset_index()
    df_grouped["Statsbidrag"] = df_grouped["Statsbidrag"] / 1_000_000  # millions
    fig = px.bar(
        df_grouped,
        x="År", y="Statsbidrag",
        title="Utbetalda statliga medel per år (miljoner kronor)",
        labels={"Statsbidrag": "Miljoner kronor", "År": "År"}
    )
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    return fig
#-----------

def prepare_pie_data_filtered(df):
    df_grouped = df.groupby("Sökt utbildningsområde")["Sökt antal platser 2024 (start och avslut 2024)"].sum().reset_index()
    df_grouped = df_grouped[df_grouped["Sökt antal platser 2024 (start och avslut 2024)"] > 0]
    title = "Beviljade platser per utbildningsområde"
    return df_grouped, title



def create_bub_animated_chart(df, selected_year):
    filtered = df[df["År"] == int(selected_year)]
    grouped = filtered.groupby("utbildningsområde MYH")["Antal behöriga"].sum().reset_index()

    fig = px.bar(
        grouped.sort_values("Antal behöriga", ascending=True),
        x="Antal behöriga",
        y="utbildningsområde MYH",
        orientation="h",
        color="Antal behöriga",
        color_continuous_scale=[[0, 'rgb(0,50,25)'], [1, 'rgb(0,100,50)']],
        title=f"Studerande per utbildningsområde ({selected_year})",
        labels={"Antal behöriga": "Antal studerande", "utbildningsområde MYH": "Utbildningsområde"}
    )

    fig.update_layout(showlegend=False, height=600)
    return fig





def create_pie_chart_with_title(df, title):
    fig = px.pie(
        df,
        values="Sökt antal platser 2024 (start och avslut 2024)",
        names="Sökt utbildningsområde",
        title=title
    )
    return fig



#Map

def plot_beviljade_by_year(df_combined):
    df_grouped = df_combined.groupby("År", as_index=False)["Beviljade"].sum()
    fig = px.bar(
        df_grouped,
        x="År", y="Beviljade",
        title="Totalt antal beviljade platser per år",
        labels={"Beviljade": "Antal platser", "År": "År"}
    )
    fig.update_layout(bargap=0.2, margin={"r": 0, "t": 40, "l": 0, "b": 0})
    return fig


def plot_beviljade_by_region(df_regions, geojson_data, year):
    df_year = df_regions[df_regions["År"] == year].copy()
    df_year = df_year.dropna(subset=["Länskod"])
    df_year["Länskod"] = df_year["Länskod"].astype(str)

    fig = px.choropleth(
        df_year,
        geojson=geojson_data,
        locations="Länskod",
        featureidkey="properties.ref:se:länskod",
        color="Beviljade",
        hover_name="Län",
        color_continuous_scale="Blues",
        title=f"Beviljade platser per region ({year})"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    return fig


def plot_statsbidrag_by_region(df_regions, geojson_data, year):
    df_year = df_regions[df_regions["År"] == year].copy()
    df_year = df_year.dropna(subset=["Länskod"])
    df_year["Länskod"] = df_year["Länskod"].astype(str)

    fig = px.choropleth(
        df_year,
        geojson=geojson_data,
        locations="Länskod",
        featureidkey="properties.ref:se:länskod",
        color="Statsbidrag",
        hover_name="Län",
        color_continuous_scale="Viridis",
        title=f"Statsbidrag per region ({year})"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    return fig

def plot_beviljade_by_anordnare(df_combined, top_n=10):
    df_top = (
        df_combined.groupby("Anordnare")["Beviljade"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    fig = px.bar(
        df_top,
        x="Beviljade", y="Anordnare",
        orientation="h",
        title=f"Topp {top_n} utbildningsanordnare (antal beviljade platser)",
        labels={"Beviljade": "Antal platser", "Anordnare": "Utbildningsanordnare"}
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return fig


# trend_applications_over_time

# === Application Trend Line Chart ===
df = pd.read_csv("data/processed_applications.csv")

# Extract dropdown options
genders = df["Kön"].dropna().unique().tolist()
areas = df["Utbildningsområde"].dropna().unique().tolist()


# Load the processed applications data
df_trends = pd.read_csv("data/processed_applications.csv")

def plot_application_trends():
    fig = px.line(
        df_trends,
        x="År",
        y="Antal ansökningar",
        color="Utbildningsområde",
        line_dash="Kön",
        title="Ansökningstrender per utbildningsområde (2020–2024)",
        labels={"År": "År", "Antal ansökningar": "Antal ansökningar"}
    )
    fig.update_layout(xaxis=dict(dtick=1))
    return fig

# Create a static figure (used in dashboard.py)
application_trend_figure = plot_application_trends()
