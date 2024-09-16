import streamlit as st
from PIL import Image

st.set_page_config( page_title='Home', page_icon='🏠', layout='wide' )

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
        /* Estilos para a tabela */
        .dataframe {
            background-color: #12171C;  /* Cor de fundo da tabela */
            color: #ffffff;  /* Cor da fonte da tabela */
        }
    </style>
    '''

# Aplicar o CSS no Streamlit
st.markdown(page_bg_color, unsafe_allow_html=True)



image = Image.open('logo.png')
st.sidebar.image( image, use_column_width=True)

st.sidebar.markdown('# Fome Zero!')
st.sidebar.markdown('## Zere sua fome em qualquer lugar')
st.sidebar.markdown("""---""")

st.write ( "# Fome Zero Dashboard" )

st.markdown(
    """
    Este Dahshboard foi construído para acompanhar as métricas de crescimento do app Fome Zero.
    ### Como utulizar o Dashboard?
    - Main Page:
        - Métricas absolutas da plataforma e geolocalização dos restaurantes.
    - Countries:
        - Indicadores na perspectiva dos páises.
    - Cities:
        - Indicadores na perspectiva das cidades.
    - Cuisines:
        - Indicadores na perspectiva dos tipos de culinárias.

     #### Contato:
     - Linkedin: https://www.linkedin.com/in/thomas-kunzler/
    """
)    
