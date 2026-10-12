import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

st.set_page_config(page_title="BuscaMenor", page_icon="🛍️", layout="wide")

st.markdown("# 🛍️ Buscador do Menor Valor Final")
termo = st.text_input("O que você procura?")
cep = st.text_input("Seu CEP:")
if st.button("Buscar"):
    st.write("Buscando produtos...")
