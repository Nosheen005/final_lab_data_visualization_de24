# main.py
from taipy.gui.builder import Gui, Markdown, Dropdown, notify, Toggle, Slider
import pandas as pd
import plotly.express as px
import json
from data_processing import (
    load_course_data,
    load_geojson,
    get_organizer_stats,
    applications_by_field,
    get_region_summary,
    melt_students_over_time
)

# === Load data ===
df_courses = load_course_data("data/inkomna-ansokningar-2024-for-kurser.xlsx")
df_students = pd.read_csv("data/student/antal_behoriga_sokande_kurser_kon_omrade_alder_2020_2024.csv", encoding="latin1")
geojson_data = load_geojson("assets/swedish_regions.geojson")

organizers = sorted(df_courses["Anordnare namn"].unique())
education_areas = sorted(df_courses["Sökt utbildningsområde"].unique())
student_years = [2020, 2021, 2022, 2023, 2024]

# === State ===
selected_view = "Applications"
selected_organizer = organizers[0]
selected_year = 2024
selected_area = education_areas[0]
chart = None
stats_md = ""

view_options = [
    "Applications",
    "Students Over Time",
    "Map View",
    "Organizer Stats",
    "Statsbidrag"
]

# === Chart/Markdown logic ===
def update_view(state):
    if state.selected_view == "Applications":
        data = applications_by_field(df_courses)
        state.chart = px.bar(data, x="Sökt utbildningsområde", y="Sökt antal platser 2024",
                              title="Total Seats by Education Area")

    elif state.selected_view == "Students Over Time":
        df_melted = melt_students_over_time(df_students)
        df_area = df_melted[df_melted["utbildningsområde MYH"] == state.selected_area]
        df_year = df_area[df_area["År"] == state.selected_year]
        df_grouped = df_year.groupby("region (hemlän)")["Antal behöriga"].sum().reset_index()
        fig = px.choropleth(
            df_grouped,
            geojson=geojson_data,
            featureidkey="properties.name",
            locations="region (hemlän)",
            color="Antal behöriga",
            color_continuous_scale="Viridis",
            title=f"Qualified Students in {state.selected_area} - {state.selected_year}"
        )
        fig.update_geos(fitbounds="locations", visible=False)
        state.chart = fig

    elif state.selected_view == "Map View":
        data = get_region_summary(df_courses)
        state.chart = px.sunburst(data, path=["Län", "Kommun", "Anordnare namn"],
                                  values="Sökt antal platser 2024", title="Seats by Region")

    elif state.selected_view == "Organizer Stats":
        stats = get_organizer_stats(df_courses, state.selected_organizer)
        lines = [
            f"### 📊 Organizer: **{stats['name']}**",
            f"- **Courses:** {stats['courses']}",
            f"- **Total Seats:** {stats['seats']}",
            f"- **Avg YH Points:** {stats['average_yh']}",
            "\n**Fields:**"
        ] + [f"- {k}: {v}" for k, v in stats['fields'].items()]
        state.stats_md = "\n".join(lines)

    elif state.selected_view == "Statsbidrag":
        grouped = df_courses.groupby("Sökt utbildningsområde")["YH-poäng"].sum().reset_index()
        grouped["Statsbidrag"] = grouped["YH-poäng"] * 7000
        state.chart = px.bar(grouped, x="Sökt utbildningsområde", y="Statsbidrag",
                             title="Statsbidrag per Education Area (YH-poäng * 7000)")

# === Dashboard layout ===
page = """
# 🏫 YH Dashboard

<|dropdown|value=selected_view|lov=view_options|label=Select View|on_change=update_view|>

<|part|render={selected_view=="Organizer Stats"}|
<|dropdown|value=selected_organizer|lov=organizers|label=Choose Organizer|on_change=update_view|>
<|markdown|content=stats_md|>
|>

<|part|render={selected_view=="Students Over Time"}|
<|dropdown|value=selected_area|lov=education_areas|label=Education Area|on_change=update_view|>
<|slider|value=selected_year|min=2020|max=2024|step=1|label=Year|on_change=update_view|>
|>

<|part|render={selected_view!="Organizer Stats"}|
<|chart|figure=chart|>
|>
"""

# === Run app ===
Gui(page).run()
            