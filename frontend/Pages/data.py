import taipy.gui.builder as tgb
from backend.data_processing import df_courses, df_students, df_grants, df_graduates

with tgb.Page() as data_page:
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()

        tgb.text("# Rådata", mode="md")

        with tgb.part(class_name="card"):
            tgb.text("### Ansökningar för kurser 2024", mode="md")
            tgb.table("{df_courses}")

        with tgb.part(class_name="card"):
            tgb.text("### Behöriga studerande 2020–2024", mode="md")
            tgb.table("{df_students}")

        with tgb.part(class_name="card"):
            tgb.text("### Utbetalda statsbidrag per år", mode="md")
            tgb.table("{df_grants}")

        with tgb.part(class_name="card"):
            tgb.text("### Examinerade inom yrkesområden", mode="md")
            tgb.table("{df_graduates}")
