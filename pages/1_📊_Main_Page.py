!pip install inflection

# Bibliotecas
import pandas as pd
import datetime
import numpy as np
from PIL import Image
from haversine import haversine
import inflection

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster


st.set_page_config( page_title='Main Page', page_icon='📊', layout='wide' )

# -----------------------------------------
# Funções
# -----------------------------------------

#def clean_code(df1):

def apply_custom_styles(fig):
    """
    Aplica estilos personalizados ao gráfico Plotly.

    Parâmetros:
    - fig: O objeto figura Plotly a ser estilizado.
    
    Retorna:
    - fig: O objeto figura Plotly estilizado.
    """
    # Definir os estilos personalizados
    custom_styles = {
        'plot_bgcolor': '#12171C',  # Cor de fundo do gráfico
        'paper_bgcolor': '#222C36',  # Cor de fundo da área do "papel"
        'xaxis': {
            'title_font': {'color': '#ffffff'},  # Cor do título do eixo X
            'tickfont': {'color': '#ffffff'},    # Cor dos ticks do eixo X
            'gridcolor': '#222C36'               # Cor da grade do eixo X
        },
        'yaxis': {
            'title_font': {'color': '#ffffff'},  # Cor do título do eixo Y
            'tickfont': {'color': '#ffffff'},    # Cor dos ticks do eixo Y
            'gridcolor': '#222C36'               # Cor da grade do eixo Y
        },
        'colorway': ['#F87F22'],  # Define a cor das barras (sequência de cores)
        'font': {'color': '#ffffff'},  # Cor padrão dos rótulos (labels)
        
    }
    
    # Aplicar estilos ao gráfico
    fig.update_layout(
        plot_bgcolor=custom_styles['plot_bgcolor'],
        paper_bgcolor=custom_styles['paper_bgcolor'],
        xaxis=dict(
            title_font=custom_styles['xaxis']['title_font'],
            tickfont=custom_styles['xaxis']['tickfont'],
            gridcolor=custom_styles['xaxis']['gridcolor']
        ),
        yaxis=dict(
            title_font=custom_styles['yaxis']['title_font'],
            tickfont=custom_styles['yaxis']['tickfont'],
            gridcolor=custom_styles['yaxis']['gridcolor']
        ),
        colorway=custom_styles['colorway'],
        font=custom_styles['font']
    )

    # Remover bordas das barras
    fig.update_traces(
        marker=dict(line=dict(color='rgba(0,0,0,0)', width=0))  # Remover bordas
    )
    return fig




def map_plot(df2):
    # Criar um mapa centralizado nas coordenadas médias do seu DataFrame
    media_lat = df2['latitude'].mean()
    media_lon = df2['longitude'].mean()
    
    # Inicializar o mapa
    mapa = folium.Map(location=[media_lat, media_lon], zoom_start=1.2)
    
    # Adicionar um agrupador de marcadores (opcional, útil para muitos pontos)
    marker_cluster = MarkerCluster().add_to(mapa)
    
    # Adicionar os marcadores para cada local
    for idx, row in df2.iterrows():
        folium.Marker(location=[row['latitude'], row['longitude']],
                      popup=f"Restaurante: {row['restaurant_name']}, Avaliação: {row['aggregate_rating']}").add_to(marker_cluster)
    
    # Exibir o mapa
    folium_static(mapa, width=750, height=425)





# -----------------------------------Início da Estrutura Lógica do Código ----------------------------------
# ---------------------
# Import dataset
# ---------------------
df = pd.read_csv('dataset/zomato.csv')

# ---------------------
# Limpeza do dataset
# ---------------------
#df1 = clean_code( df )

#Copiando df
df1 = df.copy ()

# Limpando valore NaN da coluna Cuisines
df1 = df.dropna(subset=['Cuisines'])

# Retirando Linhas duplicadas
df1 = df1.drop_duplicates()




#Numeração dos Países
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}

def country_name(country_id):
    return COUNTRIES[country_id]


# Classificação do Preço
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"


#Cores
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]


# Renomear Colunas
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df




# Nova coluna Contry Name
df1.loc[:, 'Country Name'] = df1['Country Code'].apply(country_name)

# Criar uma nova coluna 'Price Type' com as categorias de preço
df1.loc[:, 'Price Type'] = df1['Price range'].apply(create_price_type)

# Criar uma nova coluna 'Price Type' com as categorias de preço
df1.loc[:, 'Color name'] = df1['Rating color'].apply(color_name)

# Ajustando somente colinaria primaria do restaruante
df1["Cuisines"] = df1.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])

#Ajustando nome de variáveis longas:
df1['Country Name'] = df1['Country Name'].replace({
    'United States of America': 'USA',
    'United Arab Emirates': 'Arab Emirates'
})


# Renomeando as colunas do Dataframe
df2 = rename_columns(df1)

# Excluir valores preenchidos incorretamente
df2 = df2[~((df2['country_name'] == 'Australia') & (df2['average_cost_for_two'] > 1000))]




# ---------------------
# Cores do página do StreamLit
# ---------------------

# Custom CSS
page_bg_color = '''
    <style>
        /* Cor de fundo da página */
        .stApp {
            background-color: #222C36;  /* Mude aqui a cor do fundo da página */
        }
    
        /* Cor de fundo da barra lateral */
        section[data-testid="stSidebar"] {
            background-color: #12171C;  /* Mude aqui a cor da barra lateral */
        }
    
        /* Cor da fonte da barra lateral */
        section[data-testid="stSidebar"] * {
            color: #ffffff;  /* Mude aqui a cor da fonte da barra lateral */
        }
    
        /* Cor da fonte do resto da página */
        .stApp * {
            color: #FFFFFF  /* Mude aqui a cor da fonte da página */
        }
    </style>
    '''

# Aplicar o CSS no Streamlit
st.markdown(page_bg_color, unsafe_allow_html=True)


# ---------------------
# Cores dos gráficos
# ---------------------


# =====================================
# Barra Lateral
# ====================================+

image = Image.open('logo.png')
st.sidebar.image( image, use_column_width=True)

st.sidebar.markdown('# Fome Zero!')
st.sidebar.markdown('## Zere sua fome em qualquer lugar')
st.sidebar.markdown("""---""")

st.sidebar.markdown( '### Desenvolvido por Thomas Kunzler' )


# =====================================
# Layout Streamlit Tabs
# ====================================

#Título
st.header('Fome Zero!')
st.markdown('#### Milhares de opções para zerar sua fome')
st.markdown('##### Principais métricas da plataforma:')


with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:           
        restaurantes = len(df2['restaurant_id'].unique())
        col1.metric( 'N° Restaurantes', restaurantes )
        
    with col2:
        paises = len(df2['country_code'].unique())
        col2.metric( 'N° Países', paises )

    with col3:
        cidades = len(df2['city'].unique())
        col3.metric( 'N° Cidades', cidades )

    with col4:
        avaliacoes = df2['votes'].sum()
        col4.metric( 'N° Avaliações', avaliacoes )

    with col5:
        culinarias = len(df2['cuisines'].unique())
        col5.metric( 'N° Culinárias', culinarias )



with st.container():
    #Plotar Mapa
    map_plot(df2)



