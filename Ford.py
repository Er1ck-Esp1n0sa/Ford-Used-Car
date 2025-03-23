import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

#--- IMPORT DATA WITH ERROR HANDLING ---#
try:
    df = pd.read_csv("dataset/ford.csv")
except FileNotFoundError:
    st.error("Error: No se encontró el archivo de datos.")
    st.stop()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

#--- PAGE CONFIG ---#
st.set_page_config(page_title="Ford Used Car Listing", page_icon=":car:") 
st.title("Ford Used Car Listing")
st.write("Autor: Erick Juarez Espinosa")
st.write("Matricula: S20006728")

st.header("Descripción del sitio")
st.markdown(
    "Este sitio permite listar autos de la marca Ford con su año de fabricación, "
    "precio, tipo de combustible, transmisión, entre otras características."
)

#--- LOGO ---#
st.sidebar.image("img/logo.png")
st.sidebar.markdown("##")

#--- FUNCIONES ---#
@st.cache_data
def load_data(nrows=None):
    return df if nrows is None else df.head(nrows)

def load_data_byname(name):
    filtered_data = df[df['model'].str.contains(name, case=False, na=False)]
    return filtered_data

def load_data_bytransmission(transmission):
    return df[df['transmission'] == transmission]

#--- DATA DISPLAY ---#
st.header("Todos los carros")
data_load_state = st.text('Cargando datos...')
data = load_data()

#--- SIDEBAR FILTERS ---#
sidebar = st.sidebar
if sidebar.checkbox("Mostrar todos los modelos de autos"):
    st.dataframe(data)

#--- FILTER BY MODEL ---#
model_name = sidebar.text_input('Modelo del auto:')
btn_search = sidebar.button('Buscar auto')

if btn_search:
    filtered_data = load_data_byname(model_name)
    count_row = filtered_data.shape[0]
    if count_row > 0:
        st.write(f"Total de autos encontrados: {count_row}")
        st.dataframe(filtered_data)
    else:
        st.warning("No se encontraron autos con ese modelo.")

#--- FILTER BY TRANSMISSION ---#
selected_transmission = sidebar.selectbox("Seleccionar transmisión:", df['transmission'].unique())
btn_filter_transmission = sidebar.button('Filtrar por transmisión')

if btn_filter_transmission:
    filtered_data = load_data_bytransmission(selected_transmission)
    count_row = filtered_data.shape[0]
    if count_row > 0:
        st.write(f"Total de autos encontrados: {count_row}")
        st.dataframe(filtered_data)
    else:
        st.warning("No se encontraron autos con esa transmisión.")

#--- GRÁFICOS ---#
if st.sidebar.checkbox('Distribución de Precios por Modelo'):
    fig, ax = plt.subplots(figsize=(10, 5))
    df.groupby('model')['price'].mean().plot(kind='bar', ax=ax)
    plt.xticks(rotation=90)
    ax.set_xlabel('Modelo del auto')
    ax.set_ylabel('Precio Promedio')
    ax.set_title('Distribución de Precios por Modelo')
    st.pyplot(fig)

#--- SCATTER PLOT: PRECIO VS AÑO ---#
if st.sidebar.checkbox('Dispersión Precio vs Año'):
    fig = px.scatter(df, x="year", y="price", color="fuelType",
                     title="Variación del Precio según Año",
                     template="plotly_white")
    st.plotly_chart(fig)

#--- MULTISELECT FILTRADO ---#
selected_fuel = st.sidebar.multiselect("Tipo de Combustible", sorted(df["fuelType"].dropna().unique()))
selected_model = st.sidebar.multiselect("Modelo del Auto", sorted(df["model"].dropna().unique()))

if st.sidebar.button("Filtrar Autos"):
    st.markdown("Mostrando autos filtrados por modelo y tipo de combustible.")
    mask = df["fuelType"].isin(selected_fuel) & df["model"].isin(selected_model)
    filtered_data = df[mask]
    if not filtered_data.empty:
        st.dataframe(filtered_data)
    else:
        st.warning("No se encontraron autos con esos filtros.")
