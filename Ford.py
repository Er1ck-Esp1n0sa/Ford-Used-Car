import pandas as pd
import streamlit as st
import base64

st.title('Ford Used Car Listing')

DATA_URL=('dataset/ford.csv')

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL)
    return data

def load_data_byname(name):
    data = pd.read_csv(DATA_URL)
    filtered_data_byname = data[data['model'].str.contains(name)]
    return filtered_data_byname

def load_data_bytransmission(transmission):
    data = pd.read_csv(DATA_URL)
    filtered_data_bytras = data[data[ 'transmission' ] == transmission]

    return filtered_data_bytras

st.header('Erick Juaerz Espinosa')
st.header('ZS20006728')

data_load_state = st.text('Data cargada')
data = load_data(500)
st.header("Todos los carros")

st.sidebar.image("img/logo.png")
st.sidebar.markdown("##")

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
        st.write(f"Buscar autos : {count_row}")
        st.dataframe(filterbyname)

selected_transmission = sidebar.selectbox("Seleccionar transmicion: ", data ['transmission'].unique())
btnFilterbyTransmission = sidebar.button('Filtrar por transmicion')

if (btnFilterbyTransmission):
    filterbyTransmission = load_data_bytransmission(selected_transmission)
    count_row = filterbyTransmission.shape[0]
    st.write(f"Total items : {count_row}")
    st.dataframe(filterbyTransmission)