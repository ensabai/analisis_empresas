import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

COLUMNAS = ["nombre","pagina_web","ultimo_anyo","ventas_euros","n_empleados","ciudad","calle","descripcion","codigo","codigo_descripcion","etiqueta"]
NOMBRES = {"nombre":"Nombre",
           "ultimo_anyo":"Último Año Registrado",
           "ventas_euros":"Ingresos por Ventas (€)",
           "n_empleados":"Número Empleados",
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

    with st.sidebar:
        etiqueta_select = st.multiselect(
            "Selecciona Etiqueta",
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
            "Selecciona CNAE",
            np.unique(empresas["codigo"])
        )

        ventas_select = st.slider(
            "Ingresos por Ventas",
            0,
            empresas["ventas_euros"].max(),
            value=(0, empresas["ventas_euros"].max())
        )

        pagina_web_select = st.checkbox("Página Web Disponible")
    
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

    st.dataframe(empresas_aux.loc[:,COLUMNAS].rename(columns = NOMBRES))

    st.download_button(
            label="Descargar Datos",
            data=to_excel(empresas_aux),
            file_name="datos_empresas.xlsx",
            mime="application/vnd.ms-excel"
        )
    
    return

if __name__ == "__main__":
    main()