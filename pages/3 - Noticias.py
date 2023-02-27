import feedparser
import streamlit as st
from bs4 import BeautifulSoup

# Defina as URLs dos feeds RSS que você deseja analisar
urls = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.securityweek.com/feed"
]

# Crie duas colunas no Streamlit
col1, col2 = st.columns(2)
col2.header(':blue[Security Week]')
col1.header(':blue[The Hacker News]')


# Iterar por cada URL
for i, url in enumerate(urls):
    # Analisar o feed RSS com o feedparser
    feed = feedparser.parse(url)

    # Obter os primeiros 3 itens do feed
    items = feed.entries[:5]

    # Itere pelos itens no feed
    for item in items:
        # Extrair o título, link e descrição de cada item
        title = item.title
        link = item.link
        description = item.description

        # Remover as tags HTML da descrição usando BeautifulSoup
        soup = BeautifulSoup(description, 'html.parser')
        description_sem_tags = soup.get_text()

        # Adicionar o item à coluna correspondente
        if i == 0:
            col1.subheader(title)
            col1.write(description_sem_tags)
            col1.write(f"[Link]({link})")
        else:
            col2.subheader(title)
            col2.write(description_sem_tags)
            col2.write(f"[Link]({link})")


        # Adicionar uma linha em branco para separar os itens
        #st.write("---")