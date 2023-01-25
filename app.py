import streamlit as st
import pandas as pd



df = pd.read_csv('fw.csv', sep=';',keep_default_na=False)

#Filtrando Fabricantes e modelos
_pa= df.loc[df['Fabricante'] == 'Palo Alto']
modelo_pa = _pa['modelo'].unique()

_ck = df.loc[df['Fabricante'] == "Checkpoint"]
modelo_ck = _ck['modelo']

_fg = df.loc[df['Fabricante'] == 'Fortigate']
modelo_fg = _fg['modelo']

#setup da Pagina WEB
st.set_page_config(page_title="Firewall compare tool", layout="wide")
#esconde menu hamburguer
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


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

#tabela que será apresntada na pagina central
select = df.query("modelo == @model_pa")
select_ck = df.query("modelo == @model_ck" )
select_fg = df.query("modelo == @model_fg")

#combinado as tabelas
select_all = select.merge(select_ck, how = 'outer').merge(select_fg, how ='outer')
#df_conbine = pd.merge(select, select_ck, select_fg, how = 'outer')

#adiciona o fabricante como index
df_conbine = select_all.set_index('Fabricante')

#adiciona grafico com trhoughput
#primeiro filtra colunas com info sobre troughtput
df_bar = select_all[['Fabricante',
                    'modelo',
                    'Throughput(HTTP)GB',
                    'Throughput(APPMIX)GB',
                    'Threat Prevention(HTTP)GB',
                    'Threat Prevention(APPMIX)GB'
                    ]]


#apresntação do dataframe T inverte linhas para colunas
st.dataframe(df_conbine.T, use_container_width=True)