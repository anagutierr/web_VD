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
        gdf_ccaa = gpd.read_file("Inicio/src/mapa/se89_3_admin_ccaa_a_x.shp")
        #gdf_prov = gpd.read_file("Inicio/src/mapa/recintos_provinciales_inspire_peninbal_etrs89.shp")
        return gdf_ccaa
