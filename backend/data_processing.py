import pandas as pd
import numpy as np
import json

# === Load Main Datasets ===
df_courses = pd.read_excel("data/course/inkomna-ansokningar-2024-for-kurser.xlsx")
df_students = pd.read_csv("data/student/antal_behoriga_sokande_kurser_kon_omrade_alder_2020_2024.csv", encoding="latin1")
df_grants = pd.read_excel("data/payments/ek_1_utbet_statliga_medel_utbomr.xlsx")
df_graduates = pd.read_csv(
    "data/student/studerande_examinerade_kon_inriktning_region_form_langd_examen_2020_2024.csv",
    encoding="latin1",
    on_bad_lines="skip"
)

# === Filtered Applications Dataset ===
filtered_df = df_courses[df_courses["Sökt antal platser 2024"] > 0]

# === Data Loader Functions ===
def load_course_data(path):
    return pd.read_excel(path)

def load_geojson(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# === Organizer Summary ===
def get_organizer_stats(df, organizer_name):
    df_org = df[df["Anordnare namn"] == organizer_name]
    return {
        "name": organizer_name,
        "courses": len(df_org),
        "seats": df_org["Sökt antal platser 2024"].sum(),
        "average_yh": round(df_org["YH-poäng"].mean(), 2),
        "fields": df_org["Sökt utbildningsområde"].value_counts().to_dict()
    }

# === Aggregations and Trends ===
def applications_by_field(df):
    return df.groupby("Sökt utbildningsområde")["Sökt antal platser 2024"].sum().reset_index()

def get_region_summary(df):
    return df[df["Kommun"] != 'Se "Lista flera kommuner"']

def melt_students_over_time(df):
    df_filtered = df[(df["kön"] == "totalt") & (df["region (hemlän)"] != "Samtliga län") & (df["utbildningens studietakt"] == "Totalt")]
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

def trend_applications_over_time(df):
    years = [col for col in df.columns if "Sökt antal platser" in col]
    df_melted = df.melt(
        id_vars=["Sökt utbildningsområde"],
        value_vars=years,
        var_name="År",
        value_name="Platser"
    )
    df_melted["År"] = df_melted["År"].str.extract(r"(\d{4})").astype(int)
    return df_melted.groupby(["År", "Sökt utbildningsområde"])["Platser"].sum().reset_index()

def get_top_20_schools_by_applications(df):
    return (
        df.groupby("Anordnare namn")["Sökt antal platser 2024"]
          .sum()
          .sort_values(ascending=False)
          .head(20)
          .reset_index()
          .rename(columns={"Anordnare namn": "Skola", "Sökt antal platser 2024": "Antal ansökningar"})
    )

def get_filtered_df():
    return df_courses[df_courses["Sökt antal platser 2024"] > 0]

def kpi(df):
    total_applications = df["Sökt antal platser 2024"].sum()
    approved_applications = df["Sökt antal platser 2024 (start och avslut 2024)"].sum()
    approval_rate = (approved_applications / total_applications * 100) if total_applications > 0 else 0
    total_approved_places = approved_applications
    unique_schools = df["Anordnare namn"].nunique()
    return {
        "total_applications": total_applications,
        "approved_applications": approved_applications,
        "approval_rate": approval_rate,
        "total_approved_places": total_approved_places,
        "unique_schools": unique_schools
    }

def get_educational_areas():
    return df_courses["Sökt utbildningsområde"].dropna().unique().tolist()

def get_municipalities():
    return df_courses["Kommun"].dropna().unique().tolist()

def get_schools():
    return df_courses["Anordnare namn"].dropna().unique().tolist()

def get_educations():
    return df_courses["Utbildningsnamn"].dropna().unique().tolist()

def apply_filters(df, area, municipality, school, education):
    df_filtered = df.copy()
    if area:
        df_filtered = df_filtered[df_filtered["Sökt utbildningsområde"] == area]
    if municipality:
        df_filtered = df_filtered[df_filtered["Kommun"] == municipality]
    if school:
        df_filtered = df_filtered[df_filtered["Anordnare namn"] == school]
    if education:
        df_filtered = df_filtered[df_filtered["Utbildning"] == education]
    return df_filtered, kpi(df_filtered)

# Student melt for charts
df_melted = melt_students_over_time(df_students)
category_column = "utbildningsområde MYH"


# === Region-based Beviljade Data ===

# Load Excel files
df_april = pd.read_excel("data/course/beviljade-korta-utb-kurser-kurspaket-YH-april-2020-2024.xlsx", sheet_name="Lista beviljade utbildningar")
df_july = pd.read_excel("data/course/beviljade-korta-utb-kurser-kurspaket-YH-juli-2020-2024.xlsx", sheet_name="Lista beviljade utbildningar")

# Helper function
def process_beviljade(df, year_cols_prefix, kommun_cols):
    year_cols = [col for col in df.columns if col.startswith(year_cols_prefix)]
    df_melted = df.melt(
        id_vars=["Utbildningsområde", "YH-poäng", "Anordnare"] + kommun_cols,
        value_vars=year_cols,
        var_name="År",
        value_name="Beviljade"
    )
    df_melted["År"] = df_melted["År"].str.extract(r"(\d{4})").astype(int)
    df_melted["Kommun"] = df_melted[kommun_cols].bfill(axis=1).iloc[:, 0]
    df_melted["Kommun"] = df_melted["Kommun"].replace({".": None}).fillna("Okänd")
    return df_melted[["Utbildningsområde", "YH-poäng", "Anordnare", "År", "Beviljade", "Kommun"]]

# Process both datasets
kommun_cols_april = [f"Kommun {i}" for i in range(1, 7)]
kommun_cols_july = [f"Kommun {i}" for i in range(1, 11)]

df_april_cleaned = process_beviljade(df_april, "Platser med start", kommun_cols_april)
df_july_cleaned = process_beviljade(df_july, "Platser med start och avslut", kommun_cols_july)

# Combine and calculate statsbidrag
df_combined = pd.concat([df_april_cleaned, df_july_cleaned], ignore_index=True)
df_combined["Statsbidrag"] = df_combined["YH-poäng"] * 7000

# Load GeoJSON file with regions
with open("assets/swedish_regions.geojson", encoding="utf-8") as f:
    region_geojson = json.load(f)

# Create mapping from region name to region code
region_to_code = {
    feature["properties"]["name"]: feature["properties"]["ref:se:länskod"]
    for feature in region_geojson["features"]
}

# Add a dummy mapping from kommun to region (this should come from a reliable mapping in your data)
# If not available, you might need an external CSV to map "Kommun" → "Län"
kommun_to_region = {
    "Stockholm": "Stockholms län",
    "Sundbyberg": "Stockholms län",
    "Solna": "Stockholms län",
    "Uppsala": "Uppsala län",
    "Gävle": "Gävleborgs län",
    "Västerås": "Västmanlands län",
    "Örebro": "Örebro län",
    "Linköping": "Östergötlands län",
    "Norrköping": "Östergötlands län",
    "Jönköping": "Jönköpings län",
    "Växjö": "Kronobergs län",
    "Kalmar": "Kalmar län",
    "Karlskrona": "Blekinge län",
    "Kristianstad": "Skåne län",
    "Malmö": "Skåne län",
    "Helsingborg": "Skåne län",
    "Göteborg": "Västra Götalands län",
    "Borås": "Västra Götalands län",
    "Trollhättan": "Västra Götalands län",
    "Karlstad": "Värmlands län",
    "Falun": "Dalarnas län",
    "Östersund": "Jämtlands län",
    "Umeå": "Västerbottens län",
    "Luleå": "Norrbottens län",
    "Visby": "Gotlands län"
}
    # Add more known mappings if needed


# Map to Län and Länskod
df_combined["Län"] = df_combined["Kommun"].map(kommun_to_region)
df_combined["Länskod"] = df_combined["Län"].map(region_to_code)

# Drop rows where mapping failed
df_combined = df_combined.dropna(subset=["Län", "Länskod"])

# Aggregate
df_regions = df_combined.groupby(["Län", "Länskod", "År"]).agg({
    "Beviljade": "sum",
    "Statsbidrag": "sum"
}).reset_index()
geojson_data = region_geojson

# Make sure region_geojson, df_combined, df_regions are defined earlier in the file

region_geojson = region_geojson  # already loaded from the GeoJSON file
df_combined = df_combined        # combined April + July data
df_regions = df_regions          # grouped by region

# Optional if using in chart.py
# geojson_data = region_geojson


# Load the dataset
def process_applications_data(input_path: str, output_path: str):
    # Read the file with proper encoding
    df = pd.read_csv(input_path, encoding='latin1')

    # Extract columns related to course applications
    id_vars = ['kön', 'utbildningsområde MYH']
    value_vars = [col for col in df.columns if "Antal ansökningar" in col]

    # Melt to long format
    df_long = pd.melt(df, id_vars=id_vars, value_vars=value_vars,
                      var_name='År', value_name='Antal ansökningar')

    # Extract numeric year
    df_long['År'] = df_long['År'].str.extract(r'(\d{4})').astype(int)

    # Rename columns
    df_long = df_long.rename(columns={
        'kön': 'Kön',
        'utbildningsområde MYH': 'Utbildningsområde'
    })

    # Filter out totals for better chart control
    df_filtered = df_long[
        (df_long['Kön'] != 'totalt') &
        (df_long['Utbildningsområde'] != 'Totalt')
    ]

    # Save processed data
    df_filtered.to_csv(output_path, index=False)

# Example usage
if __name__ == "__main__":
    process_applications_data(
        input_path="data/student/antal_behoriga_sokande_kurser_kon_omrade_alder_2020_2024.csv",
        output_path="data/processed_applications.csv"
    )

