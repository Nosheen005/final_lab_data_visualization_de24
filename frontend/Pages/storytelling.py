import taipy.gui.builder as tgb
from frontend.pages.chart import (
    application_trend_figure,
    create_top_20_schools_chart,
    create_pie_chart_with_title,
    prepare_pie_data_filtered,
    statsbidrag_chart
)
from backend.data_processing import filtered_df, df_combined

# Generate required figures using functions defined in chart.py
pie_data, pie_title = prepare_pie_data_filtered(filtered_df)
pie_figure = create_pie_chart_with_title(pie_data, pie_title)
top_20_schools_figure = create_top_20_schools_chart(filtered_df)

# ✅ Rename column temporarily to match what statsbidrag_chart expects
df_temp = df_combined.rename(columns={"Utbildningsområde": "Sökt utbildningsområde"})
statsbidrag_story_chart = statsbidrag_chart(df_temp)

with tgb.Page() as storytelling_page:
    tgb.text("# Data Storytelling: YH Statistics", mode="md")

    tgb.text("""
**🔍 What can we learn from the data?**

- Applications have increased significantly in certain educational areas between 2020 and 2024.
- Women dominate some areas (e.g., Healthcare), while men dominate others (e.g., Technology).
- A few schools account for a large share of all applications.
- The distribution of government funding often reflects where the most approved study places are.
""", mode="md")

    tgb.text("## Trends in Educational Areas (2020–2024)", mode="md")
    tgb.chart(figure="{application_trend_figure}")

    tgb.text("## Top 20 Schools by Number of Applications", mode="md")
    tgb.text("""
These schools receive the highest number of applications across all educational areas.
It indicates strong demand, reputation, or program quality at these institutions.
""", mode="md")
    tgb.chart(figure="{top_20_schools_figure}")

    tgb.text("## Distribution of Approved Study Places by Area", mode="md")
    tgb.text("""
This pie chart shows how approved study places are allocated across different educational areas in 2024.
It reflects which sectors are prioritized for funding and capacity.
""", mode="md")
    tgb.chart(figure="{pie_figure}")

    tgb.text("## Government Grants by Educational Area", mode="md")
    tgb.text("""
This bar chart shows the estimated government grants (Statsbidrag) based on YH credits.

It highlights which fields receive the largest investments, reflecting policy priorities and national workforce needs.
""", mode="md")
    tgb.chart(figure="{statsbidrag_story_chart}")

__all__ = [
    "storytelling_page",
    "pie_figure",
    "top_20_schools_figure",
    "statsbidrag_story_chart"
]
