import taipy.gui.builder as tgb
import plotly.express as px
import plotly.graph_objects as go
from backend.data_processing import (
    filtered_df,
    kpi,
    get_educational_areas,
    get_municipalities,
    get_schools,
    get_educations,
    apply_filters,
    df_melted,
    category_column,
    map_processing
)

#df_melted_medel,
from .charts import (
    category_column_medel,
    create_initial_chart_medel,
    prepare_pie_data_filtered,
    create_pie_chart_with_title,
    create_map
)

# Initial values and lists
selected_year_kpi_pie = "2024"
selected_year_map = "2024"
years_map = ["2022", "2023", "2024"]
years_kpi_pie = ["2023", "2024"]
selected_year_students = "2024"
selected_year_medel = "2024"

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
medel_animated_figure = create_initial_chart_medel()
pie_data, pie_title = prepare_pie_data_filtered(filtered_df)
pie_figure = create_pie_chart_with_title(pie_data, pie_title)
map_figure = create_map(selected_year_map)
from .charts import create_top_20_schools_chart

top_20_schools_figure = create_top_20_schools_chart(filtered_df)


# Page layout with Taipy GUI Builder
dashboard_page = tgb.Page()

with dashboard_page:
    with tgb.part(class_name="container-card"):
        tgb.navbar()

        with tgb.part(class_name="title-card"):
            tgb.text("# MYH Dashboard", mode="md")

        with tgb.part(class_name="main-container"):
            # Filters
            with tgb.part(class_name="left-column"):
                with tgb.part(class_name="filter-section"):
                    with tgb.part(class_name="filter-grid"):
                        with tgb.part(class_name="card"):
                            tgb.text("# Filter", mode="md")
                            tgb.selector("{selected_educational_area}", lov="{educational_areas}", label="Välj utbildningsområde", dropdown=True)
                            tgb.selector("{selected_municipality}", lov="{municipalities}", label="Välj kommun", dropdown=True)
                            tgb.selector("{selected_school}", lov="{schools}", label="Välj skola", dropdown=True)
                            tgb.selector("{selected_education}", lov="{educations}", label="Välj utbildning", dropdown=True)
                            tgb.selector("{selected_year_kpi_pie}", lov="{years_kpi_pie}", label="Välj år:", dropdown=True)
                            tgb.button("Filtrera", class_name="button-primary")
                            tgb.button("Rensa alla filter", class_name="button-secondary")

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

            # Visualizations
            with tgb.part(class_name="middle-column"):
                with tgb.part(class_name="middle-grid"):
                    with tgb.part(class_name="map-card"):
                        tgb.text("### Fördelning av beviljade platser", mode="md")
                        tgb.chart(figure="{pie_figure}")

                    with tgb.part(class_name="map-card"):
                        tgb.text("### Geografisk fördelning (2022-2024)", mode="md")
                        tgb.selector("{selected_year_map}", lov="{years_map}", label="Välj år:", dropdown=True)
                        tgb.chart(figure="{map_figure}")

            with tgb.part(class_name="right-column"):
                with tgb.part(class_name="map-card"):
                    tgb.text("### Studerande per utbildningsområde", mode="md")
                    tgb.selector("{selected_year_students}", lov="{years_map}", label="Välj år", dropdown=True)
                    tgb.chart(figure="{bub_animated_figure}")

                with tgb.part(class_name="map-card"):
                    tgb.text("### Utbetalda statliga medel (miljoner kronor)", mode="md")
                    tgb.selector("{selected_year_medel}", lov="{years_map}", label="Välj år", dropdown=True)
                    tgb.chart(figure="{medel_animated_figure}")
                    with tgb.part(class_name="map-card"):
                        tgb.text("### Topp 20 skolor efter antal ansökningar", mode="md")
                        tgb.chart(figure="{top_20_schools_figure}")
        





#Total Number of Applications
#Approved Applications
#Rejected Applications
#Total Approved Places



#Analyze application rounds for courses
#Visualize number of students over time by education area
#Map visualization 
#Filter by organizer and show stats
#Filter map between years
#Visualize trends over time
#Filter between years