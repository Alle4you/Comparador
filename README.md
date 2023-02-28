# Comparador

App Desenvolvido em Streamlit com opção DOCKER.

São 2 abas
dimension - ferramenta para dimensionar firewall Palo Alto, com base de dados do site comparador oficial.
comparador - objetivo é comparar rapidamente datasheets de equipamentos de firewall dos fabricantes Fortigate, Checkpoint e Palo Alto.
noticias - apenas um cetralizador de rssfeed de noticias de segurança 

LIB:
beautifulsoup4==4.11.2
bs4==0.0.1
humanize==4.5.0
matplotlib==3.6.3
matplotlib-inline==0.1.6
numpy==1.24.0
pandas==1.5.2
plotly==5.13.0
requests==2.28.2
streamlit==1.17.0
streamlit-option-menu==0.3.2
urllib3==1.26.14
feedparser==6.0.10

Comando para iniciar o app:
streamlit run app.py no diretorio

comando para iniciar o docker:
docker run -p 80:8501 {nome da imagem} --theme.base=dark 

os dados de hardware Palo ALto são um scrap do site https://www.paloaltonetworks.com/products/product-comparison
estes dados depois de normalizados estão salvos em um bando de dados sqlite com nome firewall.db na tabela "pa"

Os dados do comparador são alimentados na planilha dentro do google sheets
https://docs.google.com/spreadsheets/d/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
