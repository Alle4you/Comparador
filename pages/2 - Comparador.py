import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px

# 1 - setup da Pagina WEB
st.set_page_config(page_title="Firewall Handler", layout="wide")
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


# 2.1 - montando o main menu com sidebar
# with st.sidebar:
#     selected = option_menu(
#         menu_title= 'Main Menu', #item requerido, para remover adicionar 'none'
#         options = ['Comparador', 'Dimensionador', 'Noticias'],
#         icons = ['bar-chart-fill', 'basket', 'book'], # buscar no site bootstrap o nome dos icones https://icons.getbootstrap.com/
#         menu_icon = 'cast',
#         default_index= 0,
#         orientation= 'none'
#     )
# 2.2- opção de main menu on top page horizontal
# selected = option_menu(
#     menu_title= None, #item requerido, para remover adicionar 'none'
#     options = ['Comparador', 'Dimensionador', 'Noticias'],
#     icons = ['bar-chart-fill', 'basket', 'book'], # buscar no site bootstrap o nome dos icones https://icons.getbootstrap.com/
#     menu_icon = 'cast',
#     default_index= 0,
#     orientation= 'horizontal'
# )




#lendo o arquivo com dados local
#df = pd.read_csv('fw.csv', sep=';',keep_default_na=False)
#lendo o arquivo com dados no google sheets
df = pd.read_csv('https://docs.google.com/spreadsheets/d/1FesrY4LztyBAolgBuQbi_XwcIhspMffjzfOoLJfzRjI/export?format=csv')

#tratamento de caractere separador da planillha de "," para "." para float
df['Throughput(HTTP)GB'] = df['Throughput(HTTP)GB'].str.replace(",",".").astype(float)
df['Throughput(APPMIX)GB'] = df['Throughput(APPMIX)GB'].str.replace(",",".").astype(float)
df['Threat Prevention(HTTP)GB'] = df['Threat Prevention(HTTP)GB'].str.replace(",",".").astype(float)
df['Threat Prevention(APPMIX)GB'] = df['Threat Prevention(APPMIX)GB'].str.replace(",",".").astype(float)

#Filtrando Fabricantes e modelos
_pa= df.loc[df['Fabricante'] == 'Palo Alto']
modelo_pa = _pa['modelo'].unique()

_ck = df.loc[df['Fabricante'] == "Checkpoint"]
modelo_ck = _ck['modelo']

_fg = df.loc[df['Fabricante'] == 'Fortigate']
modelo_fg = _fg['modelo']



#setup da Sidebar com filtros
st.sidebar.header("FW DATASHEET compare tool: ")

#menu de palo alto
model_pa= st.sidebar.selectbox("Selecione o Modelo Palo Alto Networks: ",
                               options=modelo_pa)

#menu de Checkpoint
model_ck = st.sidebar.selectbox("Selecione o Modelo Checkpoint: ",
                                options= modelo_ck)

#menu de Fortigate
model_fg = st.sidebar.selectbox('Selecione o Modelo Fortigate',
                                options= modelo_fg)

#tabela que será apresentada na pagina central
select = df.query("modelo == @model_pa")
select_ck = df.query("modelo == @model_ck" )
select_fg = df.query("modelo == @model_fg")

#combinado as tabelas para apresentação final
select_all = select.merge(select_ck, how = 'outer').merge(select_fg, how ='outer')
#df_conbine = pd.merge(select, select_ck, select_fg, how = 'outer')

#adiciona o fabricante como index
df_combine = select_all.set_index('Fabricante')

#adiciona grafico com trhoughput
#primeiro filtra colunas com info sobre troughtput
df_barx = select_all[['Fabricante',
                    'Throughput(HTTP)GB',
                    'Throughput(APPMIX)GB',
                    'Threat Prevention(HTTP)GB',
                    'Threat Prevention(APPMIX)GB'
                    ]]
fig = px.bar(df_barx, x="Fabricante", 
             y=['Throughput(HTTP)GB',
            'Throughput(APPMIX)GB',
            'Threat Prevention(HTTP)GB',
            'Threat Prevention(APPMIX)GB'
            ],barmode='group',
            text_auto=True,
            labels={'value':'Throughput em GB'})

fig.update_layout(
    legend=dict(
        x=0,
        y=1.0,
        orientation='h',
        yanchor='bottom',
        xanchor='left',
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    legend_title_text='',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)
config = {'displayModeBar': False}

st.plotly_chart(fig,config=config)


#apresntação do dataframe T inverte linhas para colunas
st.dataframe(df_combine.T, use_container_width=True)