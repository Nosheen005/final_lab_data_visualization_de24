import taipy.gui.builder as tgb
import plotly.express as px
import plotly.graph_objects as go
from frontend.pages.chart import application_trend_figure


from frontend.pages.chart import (
    plot_application_trends,
    application_trend_figure,
    category_column_medel,
    plot_statsbidrag_over_time,
    prepare_pie_data_filtered,
    create_pie_chart_with_title,
    create_top_20_schools_chart,
    create_bub_animated_chart,
    plot_beviljade_by_region,
    plot_statsbidrag_by_region,
    plot_beviljade_by_year,
    plot_beviljade_by_anordnare
)

from backend.data_processing import (
    df_combined,
    df_regions,
    region_geojson,
    filtered_df,
    kpi,
    get_educational_areas,
    get_municipalities,
    get_schools,
    get_educations,
    apply_filters,
    df_melted,
    category_column
)

# Initial dropdown selections and options
selected_year = "2024"
years_available = sorted(set(df_regions["År"]).union(df_melted["År"]))
selected_educational_area = ""
selected_municipality = ""
selected_school = ""
selected_education = ""

educational_areas = get_educational_areas()
municipalities = get_municipalities()
schools = get_schools()
educations = get_educations()

# KPIs
initial_kpi_results = kpi(filtered_df)
total_applications = initial_kpi_results['total_applications']
approved_applications = initial_kpi_results['approved_applications']
rejected_applications = total_applications - approved_applications
total_approved_places = initial_kpi_results['total_approved_places']
unique_schools = initial_kpi_results['unique_schools']
approval_rate = initial_kpi_results['approval_rate']

# Charts
statsbidrag_over_time_figure = plot_statsbidrag_over_time(df_combined)
pie_data, pie_title = prepare_pie_data_filtered(filtered_df)
pie_figure = create_pie_chart_with_title(pie_data, pie_title)
region_beviljade_map = plot_beviljade_by_region(df_regions, region_geojson, int(selected_year))
region_statsbidrag_map = plot_statsbidrag_by_region(df_regions, region_geojson, int(selected_year))
top_20_schools_figure = create_top_20_schools_chart(filtered_df)
bub_animated_figure = create_bub_animated_chart(df_melted, selected_year)

# Update views dynamically
def update_all_year_views(state):
    year = int(state.selected_year)
    state.region_beviljade_map = plot_beviljade_by_region(df_regions, region_geojson, year)
    state.region_statsbidrag_map = plot_statsbidrag_by_region(df_regions, region_geojson, year)
    state.bub_animated_figure = create_bub_animated_chart(df_melted, state.selected_year)

# Filter logic
def apply_filters_to_dashboard(state):
    filtered_df_local, kpi_result = apply_filters(
        filtered_df,
        state.selected_educational_area,
        state.selected_municipality,
        state.selected_school,
        state.selected_education
    )

    state.total_applications = kpi_result.get("total_applications", 0)
    state.approved_applications = kpi_result.get("approved_applications", 0)
    state.rejected_applications = state.total_applications - state.approved_applications
    state.total_approved_places = kpi_result.get("total_approved_places", 0)
    state.unique_schools = kpi_result.get("unique_schools", 0)
    state.approval_rate = kpi_result.get("approval_rate", 0.0)

    pie_data, pie_title = prepare_pie_data_filtered(filtered_df_local)
    state.pie_figure = create_pie_chart_with_title(pie_data, pie_title)
    state.top_20_schools_figure = create_top_20_schools_chart(filtered_df_local)

# Reset filters
def reset_filters(state):
    state.selected_educational_area = ""
    state.selected_municipality = ""
    state.selected_school = ""
    state.selected_education = ""
    apply_filters_to_dashboard(state)

# Build the Taipy dashboard
with tgb.Page() as dashboard_page:
    with tgb.part(class_name="container-card"):
        tgb.navbar()

        with tgb.part(class_name="title-card"):
            tgb.text("# MYH Dashboard", mode="md")

        with tgb.part(class_name="main-container"):
            with tgb.part(class_name="left-column"):
                with tgb.part(class_name="filter-section"):
                    with tgb.part(class_name="filter-grid"):
                        with tgb.part(class_name="card"):
                            tgb.text("# Filter", mode="md")
                            tgb.selector("{selected_educational_area}", lov="{educational_areas}", label="Välj utbildningsområde", dropdown=True)
                            tgb.selector("{selected_municipality}", lov="{municipalities}", label="Välj kommun", dropdown=True)
                            tgb.selector("{selected_school}", lov="{schools}", label="Välj skola", dropdown=True)
                            tgb.selector("{selected_education}", lov="{educations}", label="Välj utbildning", dropdown=True)
                            tgb.selector("{selected_year}", lov="{years_available}", label="Välj år:", dropdown=True, on_change=update_all_year_views)
                            tgb.button("Filtrera", on_action=apply_filters_to_dashboard, class_name="button-primary")
                            tgb.button("Rensa alla filter", on_action=reset_filters, class_name="button-secondary")

                with tgb.part(class_name="kpi-section"):
                    with tgb.part(class_name="filter-grid"):
                        with tgb.part(class_name="card highlight-card"):
                            tgb.text("# KPI", mode="md")
                            tgb.text("**Totalt antal ansökningar:** {total_applications:,}", mode="md", class_name="kpi-value")
                            tgb.text("**Beviljade ansökningar:** {approved_applications:,} ({approval_rate:.1f}%)", mode="md", class_name="kpi-value")
                            tgb.text("**Avslagna ansökningar:** {rejected_applications:,}", mode="md", class_name="kpi-value")
                            tgb.text("**Totalt beviljade platser:** {total_approved_places:,}", mode="md", class_name="kpi-value")
                            tgb.text("**Antal anordnare:** {unique_schools}", mode="md", class_name="kpi-value")
                            tgb.text("*Värdena uppdateras baserat på valda filter*", mode="md", class_name="filter-note")

            with tgb.part(class_name="middle-column"):
                with tgb.part(class_name="middle-grid"):
                    with tgb.part(class_name="map-card"):
                        tgb.text("### Fördelning av beviljade platser", mode="md")
                        tgb.chart(figure="{pie_figure}")

                    with tgb.part(class_name="map-card"):
                        tgb.text("### Geografisk fördelning per region", mode="md")
                        tgb.chart(figure="{region_beviljade_map}")

            with tgb.part(class_name="right-column"):
                with tgb.part(class_name="map-card"):
                    tgb.text("### Statsbidrag per region", mode="md")
                    tgb.chart(figure="{region_statsbidrag_map}")

                with tgb.part(class_name="map-card"):
                    tgb.text("### Studerande per utbildningsområde", mode="md")
                    tgb.chart(figure="{bub_animated_figure}")

                with tgb.part(class_name="map-card"):
                    tgb.text("### Utbetalda statliga medel (miljoner kronor)", mode="md")
                    tgb.chart(figure="{statsbidrag_over_time_figure}")

                with tgb.part(class_name="map-card"):
                    tgb.text("### Topp 20 skolor efter antal ansökningar", mode="md")
                    tgb.chart(figure="{top_20_schools_figure}")

                with tgb.part(class_name="map-card"):
                    tgb.text("### Ansökningstrender per utbildningsområde (2020–2024)", mode="md")
                    tgb.chart(figure="{application_trend_figure}")

__all__ = [
    "dashboard_page",
    "selected_year",
    "years_available",
    "selected_educational_area",
    "selected_municipality",
    "selected_school",
    "selected_education",
    "educational_areas",
    "municipalities",
    "schools",
    "educations",
    "total_applications",
    "approved_applications",
    "rejected_applications",
    "total_approved_places",
    "unique_schools",
    "approval_rate",
    "statsbidrag_over_time_figure",
    "pie_figure",
    "region_beviljade_map",
    "region_statsbidrag_map",
    "top_20_schools_figure",
    "bub_animated_figure",
    "application_trend_figure"
]
