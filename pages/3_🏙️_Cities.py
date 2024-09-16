# Bibliotecas
import pandas as pd
import datetime
import numpy as np
from PIL import Image
import inflection
from haversine import haversine

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster


st.set_page_config( page_title='Cities', page_icon='🏙️', layout='wide' )

# -----------------------------------------
# Funções
# -----------------------------------------


########                 Nomear Países                 ######## 
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
########                 Nomear Países                  ######## 




########                 Classificação do Preço                  ######## 
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
########                 Classificação do Preço                  ######## 



########                 Nomear cores                  ######## 
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
########                 Nomear cores                   ######## 




########                 Renomear Colunas                  ######## 
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
########                  Renomear Colunas                  ######## 




########                     Clean Code                      ######## 
def clean_code(df):
    """
    Função que realiza a limpeza dos gráficos.

    Importante - Ela utiliza as seguintes funções:
        - rename_columns(dataframe)
        - color_name(color_code)
        - create_price_type(price_range)
        - country_name(country_id)
        
    Parâmetros:
    - fig: O objeto figura Plotly a ser estilizado.
    
    Retorna:
    - fig: O objeto figura Plotly estilizado.
    """
    #Copiando df
    df1 = df.copy ()
    
    # Limpando valore NaN da coluna Cuisines
    df1 = df.dropna(subset=['Cuisines'])
    
    # Retirando Linhas duplicadas
    df1 = df1.drop_duplicates()
    
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

    return df2
########                     Clean Code                      ######## 




########                  Estilos do Grafico                 ######## 
def apply_custom_styles(fig, titulo):
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
        'title': {  # Estilos para o título
            'text': titulo,  # Defina o título do gráfico
            'y': 0.95,  # Ajuste da posição vertical do título
            'x': 0.5,  # Centraliza o título horizontalmente
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'color': '#ffffff', 'size': 20}  # Define cor branca e tamanho
        }
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
        font=custom_styles['font'],
        title=custom_styles['title'], # Adiciona o título ao gráfico
        legend=dict(font=dict(color='white'))
    )

    # Remover bordas das barras
    fig.update_traces(
        marker=dict(line=dict(color='rgba(0,0,0,0)', width=0))  # Remover bordas
    )
    
    return fig
########                  Estilos do Grafico                 ######## 



########                  Cidades com + Restaurantes                 ######## 
def city_most_rest(df2):
    # Agrupar por 'cidade' e 'country' e contar o número único de 'restaurant_id'
    df_aux = df2.loc[:, ['city', 'country_name', 'restaurant_id']].groupby(['city', 'country_name']).nunique().reset_index()
    
    # Ordenar os valores do maior para o menor
    df_aux = df_aux.sort_values(by=['restaurant_id'], ascending=False)
    
    # Selecionar as 10 cidades com mais restaurantes
    df_aux = df_aux.head(10)
    
    # Obter o valor máximo da coluna 'restaurant_id'
    max_value = df_aux['restaurant_id'].max()
    
    # Definir o limite superior do eixo Y como 15% a mais do que o valor máximo
    y_max = max_value * 1.15
    
    # Criar o gráfico de barras, utilizando 'country' para definir a cor
    fig = px.bar(df_aux, x='city', y='restaurant_id', 
                 title='Cidade com maior Nº de Restaurantes',
                 labels={'city': '', 'restaurant_id': 'Nº de Restaurantes'},
                 text='restaurant_id',
                 height=450,
                 color='country_name')  # Usar a coluna 'country' para colorir as barras
    
    return fig
########                  Cidades com + Restaurantes                 ######## 



########                  Cidades com Restaurantes > 4               ######## 
def city_rest_over_4(df2):
    #Filtrar os que possuem Nota maior que 4
    df_aux = df2[df2['aggregate_rating'] >= 4]
    
    # Agrupar por 'cidade' e somar os valores de restaruantes
    df_aux = df_aux.loc[:, ['city', 'country_name', 'aggregate_rating']].groupby(['city', 'country_name']).count().reset_index()
    
    # Ordenando os valores do maio para o menbor
    df_aux = df_aux.sort_values(by=['aggregate_rating'], ascending=False)
    
    df_aux = df_aux.head(10)
    
    # Obter o valor máximo da coluna 'city_count'
    max_value = df_aux['aggregate_rating'].max()
    
    # Definir o limite superior do eixo Y como 10% a mais do que o valor máximo
    y_max = max_value * 1.15
        
    # Criar o gráfico de barras
    fig = px.bar(df_aux, x='city', y='aggregate_rating',
                 labels={'city': '', 'aggregate_rating': 'Nº de Restaurantes'},
                 text='aggregate_rating',
                 height=450,
                 color='country_name')  
    
    return fig
########                  Cidades com Restaurantes > 4               ######## 



########                  Cidades com Restaurantes <= 2.5               ######## 
def city_rest_bellow_2(df2):
    # Filtrar os que possuem Nota menor que 2.5
    df_aux = df2[df2['aggregate_rating'] <= 2.5]
    
    # Agrupar por 'cidade', 'country_name' e contar o número de restaurantes com nota < 2.5
    df_aux = df_aux.loc[:, ['city', 'country_name', 'aggregate_rating']].groupby(['city', 'country_name']).count().reset_index()
    
    # Ordenar os valores do maior para o menor, sem considerar o país
    df_aux = df_aux.sort_values(by=['aggregate_rating'], ascending=False)
    
    # Selecionar o top 10 cidades com mais restaurantes com nota < 2.5
    df_aux = df_aux.head(10)
    
    # Obter o valor máximo da coluna 'aggregate_rating'
    max_value = df_aux['aggregate_rating'].max()
    
    # Definir o limite superior do eixo Y como 15% a mais do que o valor máximo
    y_max = max_value * 1.15
    
    # Criar o gráfico de barras, utilizando 'country_name' para definir a cor
    fig = px.bar(df_aux, x='city', y='aggregate_rating', 
                 labels={'city': 'Cidade', 'aggregate_rating': 'Nº de Restaurantes'},
                 text='aggregate_rating',
                 height=450,
                 color='country_name')
    return fig
########                  Cidades com Restaurantes <= 2.5                ######## 



########                  Cidades com Restaurantes Culinaria                ########
def city_rest_cuisines(df2):
    # Agrupar por 'cidade', 'country_name' e contar o número de restaurantes com nota < 2.5
    df_aux = df2.loc[:, ['city', 'country_name', 'cuisines']].groupby(['city', 'country_name']).nunique().reset_index()
    
    # Ordenar os valores do maior para o menor, sem considerar o país
    df_aux = df_aux.sort_values(by=['cuisines'], ascending=False)
    
    # Selecionar o top 10 cidades com mais restaurantes com nota < 2.5
    df_aux = df_aux.head(10)
    
    # Obter o valor máximo da coluna 'aggregate_rating'
    max_value = df_aux['cuisines'].max()
    
    # Definir o limite superior do eixo Y como 15% a mais do que o valor máximo
    y_max = max_value * 1.15
    
    # Criar o gráfico de barras, utilizando 'country_name' para definir a cor
    fig = px.bar(df_aux, x='city', y='cuisines', 
                 labels={'city': '', 'cuisines': 'Nº de Restaurantes'},
                 text='cuisines',
                 height=450,
                 color='country_name')
    
    return fig
########                  Cidades com Restaurantes Culinaria                ########
# -----------------------------------Início da Estrutura Lógica do Código ----------------------------------
# ---------------------
# Import dataset
# ---------------------

df = pd.read_csv('dataset/zomato.csv')

# ---------------------
# Limpeza do dataset
# ---------------------

df2 = clean_code(df)  # Chamar a função e salvar o DataFrame processado em 'df2'

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



# =====================================
# Barra Lateral
# ====================================+

image = Image.open('logo.png')
st.sidebar.image( image, use_column_width=True)

st.sidebar.markdown('# Fome Zero!')
st.sidebar.markdown('## Zere sua fome em qualquer lugar')
st.sidebar.markdown("""---""")

#Seleção dos países
countries_options = st.sidebar.multiselect(
    'Selecione o país para análise:',
    ['Arab Emirates',
     'Australia',
     'Brazil',
     'Canada',
     'England',
     'India',
     'Indonesia',
     'New Zeland',
     'Philippines',
     'Qatar',
     'Singapure',
     'South Africa',
     'Sri Lanka',
     'Turkey',
     'USA'],
    default=['Australia', 'Brazil', 'Canada', 'England', 'Philippines','South Africa', 'USA'])

st.sidebar.markdown( """---""" )
st.sidebar.markdown( '### Desenvolvido por Thomas Kunzler' )

#filtro de data

# Filtro de Transito
linhas_selecionadas = df2['country_name'].isin ( countries_options )
df2 = df2.loc[linhas_selecionadas ,:]



# =====================================
# Layout Streamlit Tabs
# ====================================

#Título
st.header('Metricas Cidades')


with st.container():
    fig = city_most_rest(df2)
    fig = apply_custom_styles(fig, titulo='Cidade com mais Restaurantes')  # Aplicar os estilos e título
    st.plotly_chart(fig) 



with st.container():
    col1, col2= st.columns(2)
    
    with col1:
        fig = city_rest_over_4(df2)
        fig = apply_custom_styles(fig, titulo='Restaurantes com Nota > 4 por Cidade')  # Aplicar os estilos e título
        st.plotly_chart(fig) 
        
    with col2:
        fig = city_rest_bellow_2(df2)
        fig = apply_custom_styles(fig, titulo='Restaurantes com Nota < 2.5 por Cidade')  # Aplicar os estilos e título
        st.plotly_chart(fig)



with st.container():
    fig = city_rest_cuisines(df2)
    fig = apply_custom_styles(fig, titulo='Cidades com Mais Culinárias Distintas')  # Aplicar os estilos e título
    st.plotly_chart(fig) # Exibir o gráfico no Streamlit












