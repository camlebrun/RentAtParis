import pandas as pd
import datetime
import geopandas as gpd
import plotly.express as px


class SelectData:
    def select_last_year(self):
        current_year = datetime.datetime.now().year
        last_year_data = None

        # Essayer de sélectionner les données de l'année précédente
        last_year = current_year - 1
        data_paris = pd.read_csv("app/data/logement-encadrement-des-loyers.csv", sep=";")
        data_paris.drop(
            columns=["geo_shape", "geo_point_2d", "Numéro INSEE du quartier", "Ville"],
            inplace=True,
        )
        last_year_data = data_paris[data_paris["Année"] == last_year]

        # Si les données de l'année précédente ne sont pas disponibles,
        # sélectionner les données de l'année d'avant
        if last_year_data.empty:
            second_last_year = current_year - 2
            last_year_data = data_paris[data_paris["Année"] == second_last_year]
        return last_year_data

    def with_maps(self):
        df = gpd.read_file(
            "app/data/quartier_paris.geojson"
        )
        df_l_qu = df[["l_qu", "geometry"]]

        fig = px.choropleth_mapbox(
            df_l_qu,
            geojson=df_l_qu.geometry,
            locations=df_l_qu.index,
            color="l_qu",
            mapbox_style="open-street-map",
            center={"lat": 48.8566, "lon": 2.3522},
            opacity=0.5,
            zoom=11,
            width=1000,
            height=800,
        )

        return fig


class map(SelectData):
    def color_map(self):
        df = gpd.read_file(
            "app/data/quartier_paris.geojson"
        )
        df_l_qu = df[["l_qu", "geometry"]]

        fig = px.choropleth_mapbox(
            df_l_qu,
            geojson=df_l_qu.geometry,
            locations=df_l_qu.index,
            color="l_qu",
            mapbox_style="open-street-map",
            center={"lat": 48.8566, "lon": 2.3522},
            opacity=0.5,
            zoom=11,
            width=1000,
            height=800,
        )

        return fig
