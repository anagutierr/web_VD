import pandas as pd
import geopandas as gpd
import streamlit as st
import os

@st.cache_data
def cargar_datos():
    with st.spinner('Cargando datos...'):
        return pd.read_csv("Inicio/data/dataset_final_formateado.csv.gz", parse_dates=["fecha"], low_memory=False, compression="gzip")

@st.cache_data
def cargar_geodatos():
    with st.spinner('Cargando datos geográficos...'):
        st.write("Archivos en mapa:")
        st.write(os.listdir("Inicio/src/mapa"))

        try:
            # Intentar cargar el shapefile con pyogrio
            gdf_ccaa = gpd.read_file("Inicio/src/mapa/se89_3_admin_ccaa_a_x.shp", engine="ESRI Shapefile")
        except ImportError:
            # Si pyogrio no está disponible, usar el motor por defecto
            st.warning("pyogrio no está instalado. Usando el motor por defecto para cargar los datos geográficos.")
            gdf_ccaa = gpd.read_file("Inicio/src/mapa/se89_3_admin_ccaa_a_x.shp")

        #gdf_prov = gpd.read_file("Inicio/src/mapa/recintos_provinciales_inspire_peninbal_etrs89.shp")
        return gdf_ccaa
