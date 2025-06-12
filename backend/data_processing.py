# data_processing.py
import pandas as pd
import numpy as np
import json

# === Load Course Application Data ===
def load_course_data(path):
    return pd.read_excel(path)

# === Load GeoJSON Region Map ===
def load_geojson(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# === Prepare Organizer Summary ===
def get_organizer_stats(df, organizer_name):
    df_org = df[df["Anordnare namn"] == organizer_name]
    total_courses = len(df_org)
    total_seats = df_org["Sökt antal platser 2024"].sum()
    avg_yh = round(df_org["YH-poäng"].mean(), 2)
    fields = df_org["Sökt utbildningsområde"].value_counts().to_dict()

    return {
        "name": organizer_name,
        "courses": total_courses,
        "seats": total_seats,
        "average_yh": avg_yh,
        "fields": fields
    }

# === Grouped Applications by Field ===
def applications_by_field(df):
    return df.groupby("Sökt utbildningsområde")["Sökt antal platser 2024"].sum().reset_index()

# === Clean and Prepare for Map ===
def get_region_summary(df):
    df_clean = df[df["Kommun"] != 'Se "Lista flera kommuner"']
    return df_clean

# === Students Over Time Format (Multiple Years) ===
def melt_students_over_time(df):
    df_filtered = df[
        (df["kön"] == "totalt") &
        (df["region (hemlän)"] != "Samtliga län") &
        (df["utbildningens studietakt"] == "Totalt")
    ]

    df_melted = df_filtered.melt(
        id_vars=["region (hemlän)", "utbildningsområde MYH"],
        value_vars=[
            "Antal behöriga sökande 2020",
            "Antal behöriga sökande 2021",
            "Antal behöriga sökande 2022",
            "Antal behöriga sökande 2023",
            "Antal behöriga sökande 2024"
        ],
        var_name="År",
        value_name="Antal behöriga"
    )
    df_melted["År"] = df_melted["År"].str.extract(r"(\d{4})").astype(int)
    return df_melted
