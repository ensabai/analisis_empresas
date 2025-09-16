import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import folium
import math
from streamlit_folium import st_folium
import streamlit.components.v1 as components

def main():

    st.title("Inicio")
    
    st.set_page_config(layout = "wide")

    empresas = pd.read_csv("empresas.csv")

    f = open("grafico.html", "r", encoding = 'utf-8')
    grafico = f.read()

    components.html(grafico, height=800)

    # centro = [39.47, -0.376389]
    # mapa = folium.Map(location= centro, zoom_start=13)

    # for _, fila in empresas.iterrows():
    #     if not math.isnan(fila["lat"]) and not math.isnan(fila["lon"]):
    #         folium.Marker([fila["lat"],fila["lon"]], popup = fila["nombre"]).add_to(mapa)

    # st_folium(mapa)

if __name__ == "__main__":
    main()