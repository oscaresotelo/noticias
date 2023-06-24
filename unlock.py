import requests
from bs4 import BeautifulSoup
import streamlit as st

def scrape_lagaceta():
    url = "https://www.lagaceta.com.ar/"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    enlaces = soup.find_all("a")

    palabras_no_deseadas = ["Clasificados", "funebres", "Club La Gaceta", "Newsletters", "Contacto", "Suscribite", "Ingresar"]

    # Dividir la pantalla en 4 columnas: botones, texto y audio
    col1, col2, col3, col4 = st.columns(4)

    for i, enlace in enumerate(enlaces):
        titulo = enlace.text.strip()
        if not titulo:
            siguiente_linea = enlace.find_next_sibling("a")
            if siguiente_linea:
                titulo = siguiente_linea.text.strip()
            else:
                continue

        if "href" in enlace.attrs:
            link = enlace["href"]
        else:
            link = "Enlace no encontrado"

        # Verificar si el título del enlace contiene palabras no deseadas
        if any(palabra in titulo for palabra in palabras_no_deseadas):
            continue

        # Distribuir los botones en las tres primeras columnas
        if i % 3 == 0:
            button = col1.button(titulo, key=i)
        elif i % 3 == 1:
            button = col2.button(titulo, key=i)
        else:
            button = col3.button(titulo, key=i)

        if button:
            response_link = requests.get(link)
            soup_link = BeautifulSoup(response_link.content, "html.parser")
            paragraphs = soup_link.find_all("p")
            text = ' '.join([p.get_text() for p in paragraphs])
            col4.write("Texto extraído:")
            col4.write(text)
            col4.write("---")

            # Buscar el elemento de audio en el HTML
            audio = soup_link.find("amp-audio", src=True)

            if audio:
                audio_url = audio["src"]
                col4.audio(audio_url)
            else:
                col4.write("No se encontró ningún audio.")

# Llamada a la función scrape_lagaceta()
scrape_lagaceta()