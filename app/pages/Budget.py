import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
from shapely.geometry import Polygon
import json
from model.data_prep import SelectData

st.set_page_config(layout="wide")

st.title("Loyer à Paris")
st.subheader("Est-ce que mon budget me permet de vivre à Paris?")
st.info(
    "Ce site vous permet de savoir si votre budget vous permet de vivre à Paris selon l'indice des des loyers 2022. Lire l'onglet méthode pour plus d'informations"
)
data_paris_last_year = SelectData().select_last_year()
methode, resultat = st.tabs(["Méthode", "Résultat"])
with methode:
    st.write(
        "Afin de savoir si votre budget vous permet de vivre à Paris, nous avons utilisé l'indice des loyers 2022"
    )
with resultat:
    col, col2 = st.columns(2)
    with col:
        bud = st.text_input("Votre budget", value=600)
        budjet = int(bud)

        surface = st.text_input("Surface en m2", value=20)
        surface = int(surface)

    with col2:
        type_loc = sorted(data_paris_last_year["Type de location"].unique())
        select_loc = st.selectbox("Type de location", type_loc)

        piece = data_paris_last_year["Nombre de pièces principales"].unique()
        select_piece = st.selectbox("Nombre de pièces", piece)

        df_filtered = data_paris_last_year.copy()
        df_filtered["Loyers de référence majorés"] = df_filtered[
            "Loyers de référence majorés"
        ].fillna(0)
        df_filtered["loyer_budget"] = (
            df_filtered["Loyers de référence majorés"].astype(float) * surface
        )

        conditions = (
            (df_filtered["loyer_budget"].notnull())
            & (df_filtered["loyer_budget"] <= budjet)
            & (df_filtered["Type de location"] == select_loc)
            & (df_filtered["Nombre de pièces principales"] == select_piece)
        )

    df_filtered = df_filtered.loc[conditions]
    df_filtered.to_csv("data/loyer_budget.csv", index=False)
    loyer_map = df_filtered[["Nom du quartier", "loyer_budget"]]
    quartier = list(loyer_map["Nom du quartier"].unique())
    quartier_str = ", ".join(quartier)
    st.write("Quartiers:", quartier_str)

    df = gpd.read_file(
        "/Users/camille/repo/projet_perso/loyer/app/data/quartier_paris.geojson"
    )
    df.rename(columns={"l_qu": "Nom du quartier"}, inplace=True)
    df_l_qu = df[["Nom du quartier", "geometry"]]

    full_data = pd.merge(
        df_filtered,
        df_l_qu,
        on="Nom du quartier",
        how="inner")
    full_data = gpd.GeoDataFrame(full_data)

    fig = px.choropleth_mapbox(
        full_data,
        geojson=full_data.geometry,
        locations=full_data.index,
        hover_data=["Nom du quartier"],
        color="loyer_budget",
        mapbox_style="carto-darkmatter",
        center={"lat": 48.8566, "lon": 2.3522},
        opacity=0.5,
        zoom=11,
        width=1000,
        height=800,
    )

    st.plotly_chart(fig, use_container_width=True)
