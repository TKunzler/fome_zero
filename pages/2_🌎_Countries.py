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


st.set_page_config( page_title='Countries', page_icon='🌎', layout='wide' )

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
        title=custom_styles['title']  # Adiciona o título ao gráfico
    )

    # Remover bordas das barras
    fig.update_traces(
        marker=dict(line=dict(color='rgba(0,0,0,0)', width=0))  # Remover bordas
    )
    
    return fig
########                  Estilos do Grafico                 ######## 




########          Gráfico de Barra  Restaurantes x País      ######## 
def chart_rest_country(df2):
    """
    Cria um gráfico de barras que mostra a quantidade de restaurantes por país.

    Parâmetros:
    - df2: DataFrame contendo as colunas 'country_name' e 'restaurant_id'.

    Retorna:
    - fig: O objeto gráfico Plotly criado.
    """
    # Agrupar por 'país' e somar os valores de restaurantes
    df_aux = df2.loc[:, ['country_name', 'restaurant_id']].groupby('country_name').count().reset_index()
    
    # Ordenando os valores do maior para o menor
    df_aux = df_aux.sort_values(by=['restaurant_id'], ascending=False)
    
    # Obter o valor máximo da coluna 'restaurant_id'
    max_value = df_aux['restaurant_id'].max()
    
    # Definir o limite superior do eixo Y como 15% a mais do que o valor máximo
    y_max = max_value * 1.15
    
    # Criar o gráfico de barras
    fig = px.bar(df_aux, x='country_name', y='restaurant_id', 
                 labels={'country_name': '', 'restaurant_id': 'Nº de Restaurantes'},
                 text='restaurant_id',
                 height=450,
                 color_discrete_sequence=['#F87F22'])
    
    # Aplicar o texto em negrito
    fig.update_traces(
        texttemplate='<b>%{text}</b>'  # Definir o texto em negrito
    )
    
    return fig 
########          Gráfico de Barra  Restaurantes x País      ######## 

########          Gráfico de Barra  Restaurantes x Cidade      ######## 
def chart_rest_city(df2):
    """
    Cria um gráfico de barras que mostra a quantidade de restaurantes por país.

    Parâmetros:
    - df2: DataFrame contendo as colunas 'country_name' e 'restaurant_id'.

    Retorna:
    - fig: O objeto gráfico Plotly criado.
    """
    # Agrupar por 'país' e somar os valores de restaurantes
    df_aux = df2.loc[:, ['country_name', 'city']].groupby('country_name').nunique().reset_index()
    
    # Ordenando os valores do maior para o menor
    df_aux = df_aux.sort_values(by=['city'], ascending=False)
    
    # Obter o valor máximo da coluna 'restaurant_id'
    max_value = df_aux['city'].max()
    
    # Definir o limite superior do eixo Y como 15% a mais do que o valor máximo
    y_max = max_value * 1.15
    
    # Criar o gráfico de barras
    fig = px.bar(df_aux, x='country_name', y='city', 
                 labels={'country_name': '', 'city': 'Nº de Cidades'},
                 text='city',
                 height=450, 
                 color_discrete_sequence=['#F87F22'])

     # Aplicar o texto em negrito
    fig.update_traces(
        texttemplate='<b>%{text}</b>'  # Definir o texto em negrito
    )
    
    return fig 
########          Gráfico de Barra  Restaurantes x Cidade      ######## 



########          Gráfico de Médias                            ######## 
def plot_average_by_country(df, column_to_aggregate, y_label):
    """
    Cria um gráfico de barras que mostra a média de uma coluna por país.

    Parâmetros:
    - df: DataFrame contendo os dados.
    - column_to_aggregate: Nome da coluna para calcular a média.
    - y_label: Rótulo do eixo Y.

    Retorna:
    - fig: O gráfico Plotly gerado.
    """
    # Agrupar por país e calcular a média da coluna especificada
    df_aux = df.groupby('country_name')[column_to_aggregate].mean().reset_index()
    
    # Ordenar os valores do maior para o menor
    df_aux = df_aux.sort_values(by=[column_to_aggregate], ascending=False)
    
    # Obter o valor máximo da coluna agregada
    max_value = df_aux[column_to_aggregate].max()
    
    # Definir o limite superior do eixo Y como 15% a mais do que o valor máximo
    y_max = max_value * 1.15
    
    # Criar o título automaticamente com base na coluna agregada
    generated_title = f'Média de {y_label} por Restaurante em Cada País'
    
    # Criar o gráfico de barras
    fig = px.bar(df_aux, x='country_name', y=column_to_aggregate, 
                 labels={'country_name': '', column_to_aggregate: y_label},
                 text=column_to_aggregate,
                 height=450,
                 color_discrete_sequence=['#F87F22'])

    
    # Atualizar o layout para formatar os valores das barras com 2 casas decimais
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    
    
    return fig
########          Gráfico de Médias                            ######## 



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
st.header('Metricas Países')


with st.container():
    fig = chart_rest_country(df2) # Chamar a função bar_plot e salvar o gráfico retornado em uma variável
    fig = apply_custom_styles(fig, titulo='Quantidade de Restaurantes Cadastrados por País')  # Aplicar os estilos e título
    st.plotly_chart(fig) # Exibir o gráfico no Streamlit


with st.container():
    fig = chart_rest_city(df2) # Chamar a função bar_plot e salvar o gráfico retornado em uma variável
    fig = apply_custom_styles(fig, titulo='Quantidade de Restaurantes Cadastrados por Cidade')  # Aplicar os estilos e título
    st.plotly_chart(fig) # Exibir o gráfico no Streamlit

with st.container():
    col1, col2= st.columns(2)
    
    with col1:           
        fig = plot_average_by_country(df2, 
                                        column_to_aggregate='votes', 
                                        y_label='Avaliações')
        fig = apply_custom_styles(fig, titulo='Média de Avaliações por Páis')  # Aplicar os estilos e título
        st.plotly_chart(fig) # Exibir o gráfico no Streamlit
        
    with col2:
        fig = plot_average_by_country(df2, 
                                       column_to_aggregate='average_cost_for_two', 
                                       y_label='Preço Prato para Dois')
        fig = apply_custom_styles(fig, titulo='Média de Preço Prato para Dois por Páis')  # Aplicar os estilos e título
        st.plotly_chart(fig) # Exibir o gráfico no Streamlit











