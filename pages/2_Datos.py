import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from dateutil.relativedelta import relativedelta
from datetime import datetime

COLUMNAS = ["nombre","cif","fecha_inicio","antiguedad","pagina_web","ultimo_anyo","ventas_euros","n_empleados","provincia","ciudad","calle","descripcion","codigo","codigo_descripcion","etiqueta"]
NOMBRES = {"nombre":"Nombre",
           "cif":"CIF",
           "fecha_inicio":"Fundación",
           "antiguedad": "Antigüedad",
           "ultimo_anyo":"Último Año Registrado",
           "ventas_euros":"Ingresos por Ventas (€)",
           "n_empleados":"Número Empleados",
           "provincia":"Provincia",
           "ciudad":"Ciudad",
           "calle":"Calle",
           "descripcion":"Descripción",
           "codigo":"CNAE",
           "codigo_descripcion":"Descripción CNAE",
           "etiqueta":"Etiqueta",
           "pagina_web":"Página Web"}

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.loc[:,COLUMNAS].rename(columns = NOMBRES).to_excel(writer, index=False, sheet_name="Datos")
    return output.getvalue()

def main():
    st.set_page_config(layout = "wide")

    empresas = pd.read_csv("empresas.csv")

    empresas["antiguedad"] = empresas["fecha_inicio"].map(lambda x: relativedelta(datetime.now().date(), pd.to_datetime(x).date()).years)

    with st.sidebar:
        etiqueta_select = st.multiselect(
            "Seleccione Etiqueta",
            np.unique(empresas["etiqueta"])
        )

        n_empleados_select = st.slider(
            "Número de Empleados",
            0,
            empresas["n_empleados"].max(),
            value=(0, empresas["n_empleados"].max())
        )

        n_empleados_nulo = st.checkbox("Número de empleados nulo")

        codigo_select = st.multiselect(
            "Seleccione CNAE",
            np.unique(empresas["codigo"])
        )

        ventas_select = st.slider(
            "Ingresos por Ventas",
            0,
            empresas["ventas_euros"].max(),
            value=(0, empresas["ventas_euros"].max())
        )

        pagina_web_select = st.checkbox("Página Web Disponible")

        provincia_select = st.multiselect(
            "Seleccione Provincia",
            np.unique(empresas["provincia"])
        )

        if len(provincia_select) > 0:
            ciudades = np.unique(empresas["ciudad"][empresas["provincia"].isin(provincia_select)])
        else:
            ciudades = np.unique(empresas["ciudad"])

        ciudad_select = st.multiselect(
            "Seleccione Ciudad",
            ciudades
        )

        antiguedad_select = st.slider(
            "Antigüedad",
            0,
            empresas["antiguedad"].max(),
            value=(0,empresas["antiguedad"].max())
        )
    
    st.title("Datos")


    if n_empleados_nulo:
        indice_empleados = np.logical_or(empresas["n_empleados"] >= n_empleados_select[0], empresas["n_empleados"] == -1)
    else:
        indice_empleados = empresas["n_empleados"] >= n_empleados_select[0]

    empresas_aux = empresas[np.logical_and(indice_empleados, empresas["n_empleados"] <= n_empleados_select[1])]

    if len(etiqueta_select) > 0:
        empresas_aux = empresas_aux[empresas_aux.etiqueta.isin(etiqueta_select)]
    
    if len(codigo_select) > 0:
        empresas_aux = empresas_aux[empresas_aux.codigo.isin(codigo_select)]
    
    empresas_aux = empresas_aux[np.logical_and(empresas["ventas_euros"] >= ventas_select[0], empresas["ventas_euros"] <= ventas_select[1])]

    if pagina_web_select:
        empresas_aux = empresas_aux[~empresas_aux["pagina_web"].isna()]
    
    if len(provincia_select) > 0:
        empresas_aux = empresas_aux[empresas_aux.provincia.isin(provincia_select)]
    
    if len(ciudad_select) > 0:
        empresas_aux = empresas_aux[empresas_aux.ciudad.isin(ciudad_select)]
    
    empresas_aux = empresas_aux[np.logical_and(empresas["antiguedad"] >= antiguedad_select[0], empresas["antiguedad"] <= antiguedad_select[1])]

    st.dataframe(empresas_aux.loc[:,COLUMNAS].rename(columns = NOMBRES))

    st.write(f"Nº Registros: {empresas_aux.shape[0]}")
    st.download_button(
            label="Descargar Datos",
            data=to_excel(empresas_aux),
            file_name="datos_empresas.xlsx",
            mime="application/vnd.ms-excel"
        )
    
    return

if __name__ == "__main__":
    main()