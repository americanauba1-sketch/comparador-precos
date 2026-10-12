import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

st.set_page_config(page_title="Buscador do Menor Valor", page_icon="🛍️", layout="wide")

st.markdown("# 🛍️ Buscador do Menor Valor Final")
st.markdown("Encontre o produto mais barato comparando o preço do item somado ao frete!")

termo_busca = st.text_input("O que você procura? (Ex: iPhone 13, Smart TV 50)")
cep_destino = st.text_input("Seu CEP (apenas números para cálculo de frete):", max_chars=8)

if st.button("Buscar Menor Preço"):
    if not termo_busca:
        st.warning("Por favor, digite o nome de um produto para buscar.")
    else:
        st.info(f"A a pesquisar por '{termo_busca}'...")
        
        # Simulação de resultados para demonstração estruturada
        # Na versão completa, faremos o Web Scraping direto nas plataformas
        dados_mock = [
            {"Plataforma": "Mercado Livre", "Produto": f"{termo_busca} - Oferta Oficial", "Preço (R$)": 1499.00, "Frete (R$)": 15.00, "Parcelamento": "10x de R$ 155,00"},
            {"Plataforma": "Shopee", "Produto": f"{termo_busca} - Loja Parceira", "Preço (R$)": 1450.00, "Frete (R$)": 45.00, "Parcelamento": "6x de R$ 255,00"},
            {"Plataforma": "Amazon", "Produto": f"{termo_busca} - Prime", "Preço (R$)": 1520.00, "Frete (R$)": 0.00, "Parcelamento": "10x de R$ 152,00"}
        ]
        
        df = pd.DataFrame(dados_mock)
        df["Valor Total Final (R$)"] = df["Preço (R$)"] + df["Frete (R$)"]
        df = df.sort_values(by="Valor Total Final (R$)").reset_index(drop=True)
        
        st.success("Busca concluída com sucesso!")
        st.markdown("### 🏆 Melhor Opção (Menor Valor Total)")
        
        melhor = df.iloc[0]
        st.metric(label=f"{melhor['Plataforma']} - {melhor['Produto']}", 
                  value=f"R$ {melhor['Valor Total Final (R$)]:.2f}", 
                  delta=f"Preço: R$ {melhor['Preço (R$)]:.2f} + Frete: R$ {melhor['Frete (R$)]:.2f}")
        
        st.markdown("---")
        st.markdown("### 📊 Comparativo Completo de Lojas")
        st.dataframe(df, use_container_width=True)
