import pandas as pd
import numpy as np
import json


df_courses = pd.read_excel("data/course/inkomna-ansokningar-2024-for-kurser.xlsx")
df_students = pd.read_csv("data/student/antal_behoriga_sokande_kurser_kon_omrade_alder_2020_2024.csv", encoding="latin1")
df_grants = pd.read_excel("data/payments/ek_1_utbet_statliga_medel_utbomr.xlsx")
df_graduates = pd.read_csv(
    "data/student/studerande_examinerade_kon_inriktning_region_form_langd_examen_2020_2024.csv",
    encoding="latin1",
    on_bad_lines="skip"
)
#added newly
filtered_df = df_courses[df_courses["Sökt antal platser 2024"] > 0]




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

# === Clean and Prepare for Map (Sunburst View) ===
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

# === Application Trend Over Time ===
def trend_applications_over_time(df):
    """Melt wide-format course data to show trends in applied seats per field and year."""
    years = [col for col in df.columns if "Sökt antal platser" in col]
    df_melted = df.melt(
        id_vars=["Sökt utbildningsområde"],
        value_vars=years,
        var_name="År",
        value_name="Platser"
    )
    df_melted["År"] = df_melted["År"].str.extract(r"(\d{4})").astype(int)
    return df_melted.groupby(["År", "Sökt utbildningsområde"])["Platser"].sum().reset_index()

if __name__ == "__main__":
    print("✅ Testing data_processing.py...")

    print("Courses:", df_courses.shape)
    print("Students:", df_students.shape)
    print("Grants:", df_grants.shape)
    print("Graduates:", df_graduates.shape)

    print("\nSample course data:")
    print(df_courses.head())

if __name__ == "__main__":
    print("data_processing.py is running")

    print("\ndf_courses:", df_courses.shape)
    print("df_students:", df_students.shape)
    print("df_grants:", df_grants.shape)
    print("df_graduates:", df_graduates.shape)

    print("\nSample rows from df_courses:")
    print(df_courses.head())

def get_top_20_schools_by_applications(df):
    top_schools = (
        df.groupby("Skola")["Antal ansökningar"]
        .sum()
        .sort_values(ascending=False)
        .head(20)
        .reset_index()
    )
    return top_schools
# adeed newly

def get_filtered_df():
    # Placeholder logic – adjust filters if needed
    return df_courses[df_courses["Sökt antal platser 2024"] > 0]

#second new 
def kpi(df):
    total_applications = df["Sökt antal platser 2024"].sum()
    approved_applications = df["Beviljade platser"].sum()
    approval_rate = (approved_applications / total_applications * 100) if total_applications > 0 else 0
    total_approved_places = df["Beviljade platser"].sum()
    unique_schools = df["Anordnare namn"].nunique()

    return {
        "total_applications": total_applications,
        "approved_applications": approved_applications,
        "approval_rate": approval_rate,
        "total_approved_places": total_approved_places,
        "unique_schools": unique_schools
    }
