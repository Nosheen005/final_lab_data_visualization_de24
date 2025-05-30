import pandas as pd
import plotly.express as px
import streamlit as st


# === Streamlit-inställningar ===
st.set_page_config(page_title="YH Dashboard", layout="wide")
st.title("📊 Statistik för beviljade YH-utbildningar med start 2024")
st.markdown("---")

# === Filinställningar ===
filename = "data/course/resultat-2024-for-kurser-inom-yh.xlsx"
sheet = "Lista ansökningar"

# Import pandas 
# Import plotly
# Filtrera data för de beviljade kurser 2024
df = pd.read_excel(filename, sheet_name=sheet, engine="openpyxl")

# Här har jag filtrerat endast beviljade kurser som startar 2024
df_2024 = df[df["Antal beviljade platser start 2024"] > 0].copy()

# Renamn så att det blir ett ord i dashboard 
df_2024.rename(columns={
    "Anordnare namn": "anordnare",
    "Utbildningsområde": "utbildningsområde",
    "Kommun": "kommun",
    "Län": "län",
    "Totalt antal beviljade platser": "antal_platser"
}, inplace=True)

# KPI:er visas överst i dashboard
col1, col2, col3 = st.columns(3)
col1.metric("Totalt antal utbildningar", len(df_2024))
col2.metric("Totalt antal platser", df_2024['antal_platser'].sum())
col3.metric("Medel platser per utbildning", round(df_2024['antal_platser'].mean(), 2))

# Dashboard kommer ser ut så här:
st.markdown("## 🏫 Topp 10 anordnare")
top10 = (
    df_2024.groupby("anordnare")["antal_platser"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .head(10)
)
top10["rank"] = range(1, 11)  # Lägg till kolumn med Top 1–10

st.dataframe(top10[["rank", "anordnare", "antal_platser"]], use_container_width=True)

# Visualisering 1: Top 10 anordnare med siffror på staplarna 
fig1 = px.bar(
    top10,
    x="anordnare",
    y="antal_platser",
    text="rank",
    title="🏆 Topp 10 anordnare – antal beviljade platser (2024)",
    labels={"anordnare": "Anordnare", "antal_platser": "Antal platser"}
)
fig1.update_traces(textposition="outside")
fig1.update_layout(xaxis_tickangle=-45, showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

# Visualisering 2: Antal platser per utbildningsområde
st.markdown("## 🎓 Antal platser per utbildningsområde")
fig2 = px.bar(
    df_2024.groupby("utbildningsområde")["antal_platser"].sum().reset_index(),
    x="utbildningsområde",
    y="antal_platser",
    title="🎓 Antal beviljade platser per utbildningsområde (2024)",
    labels={"utbildningsområde": "Utbildningsområde", "antal_platser": "Antal platser"}
)
fig2.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig2, use_container_width=True)

# Visualisering 3: Topp 10 kommuner med flest beviljade platser
st.markdown("## 🏙️ Topp 10 kommuner")
top_kommuner = (
    df_2024.groupby("kommun")["antal_platser"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .head(10)
)
top_kommuner["rank"] = range(1, 11)

fig3 = px.bar(
    top_kommuner,
    x="kommun",
    y="antal_platser",
    text="rank",
    title="🏙️ Topp 10 kommuner – beviljade platser 2024",
    labels={"kommun": "Kommun", "antal_platser": "Antal platser"}
)
fig3.update_traces(textposition="outside")
fig3.update_layout(xaxis_tickangle=-45, showlegend=False)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("## 📊 Fördelning per utbildningsområde")
andelar = (
    df_2024.groupby("utbildningsområde")["antal_platser"]
    .sum()
    .reset_index()
)
fig4 = px.pie(
    andelar,
    names="utbildningsområde",
    values="antal_platser",
    title="📊 Fördelning av beviljade platser per utbildningsområde"
)
st.plotly_chart(fig4, use_container_width=True)


#Karta
