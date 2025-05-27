import pandas as pd
import plotly.express as px

# === Filinställningar ===
filename = filename = "data/course/resultat-2024-for-kurser-inom-yh.xlsx"
sheet = "Lista ansökningar"

df = pd.read_excel(filename, sheet_name=sheet, engine="openpyxl")


# Här har jag filtrerat endast beviljade kurser som startar 2024
df_2024 = df[df["Antal beviljade platser start 2024"] > 0].copy()




#Namn på kolumner
df_2024.rename(columns={
    "Anordnare namn": "anordnare",
    "Utbildningsområde": "utbildningsområde",
    "Kommun": "kommun",
    "Län": "län",
    "Totalt antal beviljade platser": "antal_platser"
}, inplace=True)


# Dashboard kommer ser ut så här:
print("📊 Statistik för beviljade YH-utbildningar med start 2024:")
print("---------------------------------------------------------")
print("Totalt antal utbildningar:", len(df_2024))
print("Totalt antal platser:", df_2024['antal_platser'].sum())
print("Medel platser per utbildning:", round(df_2024['antal_platser'].mean(), 2))

# Topp 10 anordnare efter antal platser (1-10) 
top10 = (
    df_2024.groupby("anordnare")["antal_platser"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .head(10)
)
top10["rank"] = range(1, 11)  # Lägg till kolumn med Top 1–10

print("\n🏫 Topp 10 anordnare:\n")
print(top10[["rank", "anordnare", "antal_platser"]])

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
fig1.show()

# Visualisering 2: Antal platser per utbildningsområde
fig2 = px.bar(
    df_2024.groupby("utbildningsområde")["antal_platser"].sum().reset_index(),
    x="utbildningsområde",
    y="antal_platser",
    title="🎓 Antal beviljade platser per utbildningsområde (2024)",
    labels={"utbildningsområde": "Utbildningsområde", "antal_platser": "Antal platser"}
)
fig2.update_layout(xaxis_tickangle=-45)
fig2.show()

# Import pandas 
# Import plotly
# Filtrera data för de beviljade kurser 2024
# Renamn så att det blir ett ord i dashboard 
# Skapa dashboard som visar top 10 anordnare
# Skapa dashboard som visar antal platser per utbildningsområde. 

#-------------------------------------------------------------------#

# Nästa steg som jag tänker göra är att 
# Lägga till olika typ av diagram, grafer och karta/kartor i dashboard