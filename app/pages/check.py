import streamlit as st
import pandas as pd
import plotly.express as px

st.write("Hello World")
data_paris = pd.read_csv(
    "/app/data/logement-encadrement-des-loyers.csv",
    sep=";",
)
data_paris_2022 = data_paris[data_paris["Année"] == 2022]

piece = data_paris_2022["Nombre de pièces principales"].unique()
select_piece = st.selectbox("Nombre de pièces", piece)
epoque = data_paris_2022["Epoque de construction"].unique()
select_epoque = st.selectbox("Epoque de construction", epoque)
quartier = data_paris_2022["Nom du quartier"].unique()
type_loc = data_paris_2022["Type de location"].unique()
select_loc = st.selectbox("Type de location", type_loc)
select_quartier = st.selectbox("Quartier", quartier)
df_filtered = data_paris_2022[
    (data_paris_2022["Nombre de pièces principales"] == select_piece)
    & (data_paris_2022["Epoque de construction"] == select_epoque)
    & (data_paris_2022["Nom du quartier"] == select_quartier)
    & (data_paris_2022["Type de location"] == select_loc)
]

loyer = df_filtered[
    [
        "Loyers de référence majorés",
        "Loyers de référence",
        "Loyers de référence minorés",
    ]
]

st.dataframe(loyer)
input_m2 = st.number_input(
    "Surface en m2", min_value=9, max_value=1000, value=20, step=1
)
input_m2 = int(input_m2)
your_loyer = st.text_input("Votre loyer", value=800)
your_loyer = int(your_loyer)
max = round(loyer["Loyers de référence majorés"] * input_m2,1)
ref = loyer["Loyers de référence"] * input_m2
min = loyer["Loyers de référence minorés"] * input_m2
max_val = round(loyer["Loyers de référence majorés"] * input_m2, 0)
max_val_formatted = [f'{x:.1f}' for x in max_val]

if (your_loyer > max).all():
    st.warning("Votre loyer est supérieur au loyer de référence majoré")
    st.write(f'Votre loyer devrait être au maximum de {", ".join(max_val_formatted)} €')  
elif (your_loyer < min).all():
    st.write("Votre loyer est inférieur au loyer de référence minoré")
elif (your_loyer > ref).all():
    st.warning("Votre loyer est supérieur au loyer de référence")
    st.write(f'Votre loyer devrait être au maximum de {", ".join(max_val_formatted)} €') 
elif (your_loyer < ref).all():
    st.write("Votre loyer est inférieur au loyer de référence")
elif (your_loyer == ref).all():
    st.write("Votre loyer est égal au loyer de référence")


