import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

#--- IMPORT DATA ---#
df=pd.read_csv("dataset/ford.csv")

#--- PAGE CONFIG ---#
st.set_page_config(page_title="Ford Used Car Listing",
                    page_icon=":busts_in_silhouette:")

st.title("Ford Used Car Listing")
st.write("Autor: Erick Juarez Espinosa")
st.write("Matricula: S20006728")
st.header("Descripcion del sitio")
st.markdown("Este sitio sirve para poder listar los autos de la marca ford con su año de fabricacion y su precio hasta la actualidad")

#--- LOGO ---#
st.sidebar.image("img/logo.png")
st.sidebar.markdown("##")

#--- FUNCIONES ---#
@st.cache_data
def load_data(nrows):
    data = df 
    return data

def load_data_byname(name):
    data = df
    filtered_data_byname = data[data['model'].str.contains(name, case = False)]
    return filtered_data_byname

def load_data_bytransmission(transmission):
    data = df
    filtered_data_bytras = data[data[ 'transmission' ] == transmission]

    return filtered_data_bytras

st.header("Todos los carros")
data_load_state = st.text('Data cargada . . .')
data = load_data(100)

#--- SIDEBAR FILTERS ---#
sidebar = st.sidebar
agree = sidebar.checkbox("Mostrar todos los Modelos de auntos")
if agree:
    st.dataframe(data)

myname = sidebar.text_input('Modelo del auto :')
btnRange = sidebar.button('Buscar auto')

if (myname):
    if (btnRange):
        filterbyname = load_data_byname(myname)
        count_row = filterbyname.shape[0]
        st.write(f"Total de autos : {count_row}")
        st.dataframe(filterbyname)

selected_transmission = sidebar.selectbox("Seleccionar transmicion: ", data ['transmission'].unique())
btnFilterbyTransmission = sidebar.button('Filtrar por transmicion')

if (btnFilterbyTransmission):
    filterbyTransmission = load_data_bytransmission(selected_transmission)
    count_row = filterbyTransmission.shape[0]
    st.write(f"Total items : {count_row}")
    st.dataframe(filterbyTransmission)


#--- GRAFICAS ---#
com_precio = df['model']
if st.sidebar.checkbox('Autos y sus Precios'):
    fig, ax = plt.subplots()
    plt.xticks(rotation=90)
    ax.hist(com_precio, bins=20, range=(0, 20))
    ax.set_xlabel('Modelo del auto')
    ax.set_ylabel('Precio')
    ax.set_title('Grafica que compara el precio de n autos')
    st.pyplot(fig)

com = st.sidebar.multiselect("Combustible", sorted(data["fuelType"].unique()))
mod = st.sidebar.multiselect("Modelo auto", sorted(data["model"].unique()))

if st.sidebar.button("Filtrar auto"):
    st.markdown("Se selecciona el numero de goles de visitante y local y muesta los resultados de  partidos con ese numero de goles")
    mask = (df["fuelType"].isin(com)) & (df["model"].isin(mod))
    juegos_seleccionados = df[mask]
    st.write("Goles Seleccionados:")
    st.write(juegos_seleccionados)
