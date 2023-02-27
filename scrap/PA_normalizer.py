from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sqlite3

#conectando ao banco criando tabela
conn = sqlite3.connect('firewall.db')


scrapy_file = "scrap\pa.txt"
# abrindo a saida do spider que foi salva como textp
with open(scrapy_file, "r") as file:
    content = file.read()
    #corrigindo 1 linha que esta em branco
    content = content.replace('Traffic - 40/100Gbps QSFP+/QSFP28<span class="pull-right"></span>',
                        'Traffic - 40/100Gbps QSFP+/QSFP28<span class="pull-right">NA</span>')
    soup = BeautifulSoup(content, "html.parser")



hw = soup.find_all('div', class_='col-md-8')
# selecionando modelos dentro do HTML 'Parseando corretamento os valores'
data = []
for modelo in hw:
    model = modelo.find('a').text
    features = modelo.find('div', class_='more-features')
    feature = features.find_all('div', class_='spec')
    for spec in feature:
        name = spec.text
        value = spec.find('span', class_= "pull-right").text
        #corrigindo valores unidos pelo SPAN 
        name = name.rsplit(value)
        name = list(filter(lambda x: x != '', name))
        data.append([model, str(name).strip('["]'), value])

#criando o dataframe 
df = pd.DataFrame(data, columns=['Modelo', 'Feature', 'Valor'])
#invertendo de colunas para linha unica com o nome do equipamento
df = df.pivot(index='Modelo', columns='Feature', values='Valor')
#convertendo valorese string em float, o carcter separador era virgula agora e ponto
df = df.applymap(lambda x: x.replace(',', '.') if isinstance(x, str) else x)
#removendo asteriscos
df = df.applymap(lambda x: x.replace('*', '') if isinstance(x, str) else x)
#trocando valores str.NA para str.0
df =df.replace('NA', '0')
# corrigindo um erro de aspas simples duplicadas nos nomes de colunas
df.columns = df.columns.str.strip("'")
#selecionando colunas com valores em GB ou MB e mudando para valores numericos, para gerar graficos
colunas = ['App-ID firewall throughput', 'Threat prevention throughput', 'IPSec VPN throughput']
for col in colunas:
    df[col] = df[col].apply(lambda x: float(x.rstrip(" Gbps")) * 10**9 if "Gbps" in x else float(x.rstrip(" Mbps")) * 10**6)

def convert_to_bytes(valor):
    gb = valor / (10**9)
    return gb

for i in colunas:
  #valores normalizados  em giga
  df[i] = df[i].apply(convert_to_bytes)

# #salvando Arquivo CSV separado por";""
df.to_sql(name='pa', con=conn)
# #print(df.dtypes)

        

