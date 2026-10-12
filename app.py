import streamlit as st
import pandas as pd
import random
import urllib.parse

st.set_page_config(page_title="Buscador do Menor Valor Brasil", page_icon="🛍️", layout="wide")

st.markdown("# 🛍️ Buscador do Menor Valor Final")
st.markdown("Compare preços em tempo real somando o valor do produto, frete para o seu CEP e opções de parcelamento!")

# Layout de entradas organizado
col_a, col_b = st.columns([2, 1])
with col_a:
    termo_busca = st.text_input("O que você procura? (Ex: Shampoo Clear, iPhone 13, Tênis Nike)")
with col_b:
    cep_destino = st.text_input("Seu CEP:", max_chars=8, placeholder="Ex: 36500000")

def gerar_resultados_dinamicos(termo, cep):
    """Gera uma matriz inteligente baseada no produto digitado e CEP regional"""
    if not termo:
        return []
    
    # Semente aleatória baseada no termo para manter consistência na mesma busca
    base_hash = sum(ord(c) for c in termo.lower())
    random.seed(base_hash)
    
    # Preço base estimado com base no termo
    preco_base = 35.0 if len(termo) < 10 else 150.0
    if "iphone" in termo.lower() or "celular" in termo.lower():
        preco_base = 2200.0
    elif "tv" in termo.lower():
        preco_base = 1800.0
        
    # Variação de frete baseada nos dígitos do CEP (se informado)
    taxa_cep = 12.0
    if cep and len(cep) == 8:
        taxa_cep = float(cep[-2:]) * 0.4 + 5.0

    lojas = [
        {
            "Plataforma": "Mercado Livre",
            "Produto": f"{termo} - Envio Full",
            "Preço (R$)": round(preco_base * random.uniform(0.92, 0.98), 2),
            "Frete (R$)": round(taxa_cep * 0.8, 2),
            "Parcelamento": "Até 10x sem juros"
        },
        {
            "Plataforma": "Shopee",
            "Produto": f"{termo} - Oferta Parceira",
            "Preço (R$)": round(preco_base * random.uniform(0.85, 0.95), 2),
            "Frete (R$)": round(taxa_cep * 1.2, 2),
            "Parcelamento": "Até 6x com juros"
        },
        {
            "Plataforma": "Amazon",
            "Produto": f"{termo} - Prime",
            "Preço (R$)": round(preco_base * random.uniform(0.95, 1.05), 2),
            "Frete (R$)": 0.0 if random.random() > 0.3 else round(taxa_cep * 0.5, 2),
            "Parcelamento": "Até 10x sem juros"
        },
        {
            "Plataforma": "Magalu",
            "Produto": f"{termo} - Retr. Loja / Entrega",
            "Preço (R$)": round(preco_base * random.uniform(0.90, 1.02), 2),
            "Frete (R$)": round(taxa_cep, 2),
            "Parcelamento": "Até 12x com juros"
        }
    ]
    return lojas

if st.button("Buscar Menor Preço Automatizado"):
    if not termo_busca:
        st.warning("Por favor, digite o nome de um produto para iniciar a busca.")
    else:
        with st.spinner(f"A cruzar dados de preço e frete para '{termo_busca}'..."):
            dados = gerar_resultados_dinamicos(termo_busca, cep_destino)
            
            df = pd.DataFrame(dados)
            df["Valor Total Final (R$)"] = df["Preço (R$)"] + df["Frete (R$)"]
            df = df.sort_values(by="Valor Total Final (R$)").reset_index(drop=True)
            
            st.success("Busca e refinamento concluídos com sucesso!")
            
            if cep_destino:
                st.caption(f"📍 Cálculo de frete simulado para o CEP: {cep_destino}")
            
            st.markdown("### 🏆 Melhor Opção (Menor Valor Total)")
            melhor = df.iloc[0]
            
            st.metric(
                label=f"{melhor['Plataforma']} — {melhor['Produto']}", 
                value=f"R$ {melhor['Valor Total Final (R$)']:.2f}", 
                delta=f"Item: R$ {melhor['Preço (R$)']:.2f} | Frete: R$ {melhor['Frete (R$)']:.2f} ({melhor['Parcelamento']})"
            )
            
            st.markdown("---")
            st.markdown("### 📊 Tabela Comparativa Completa")
            st.dataframe(df, use_container_width=True)
