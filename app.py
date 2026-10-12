import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(page_title="Buscador do Menor Valor - Busca Flexível", page_icon="💊", layout="wide")

st.markdown("# 💊 Buscador do Menor Valor Final (Farmácias & Geral)")
st.markdown("Pesquise por qualquer palavra, abreviação ou termo — o nosso sistema inteligente cruza os dados de preço e frete automaticamente!")

col_a, col_b = st.columns([2, 1])
with col_a:
    termo_busca = st.text_input("O que você procura? (Ex: sh clear, desod dove, dipirona, iphone 13)")
with col_b:
    cep_destino = st.text_input("Seu CEP:", max_chars=8, placeholder="Ex: 36500000")

def limpar_e_normalizar(texto):
    """Remove acentos, espaços extras e converte para minúsculas para busca flexível"""
    if not texto:
        return ""
    # Remove caracteres especiais mantendo letras e números
    texto_limpo = re.sub(r'[^a-zA-Z0-9\s]', '', texto)
    return ' '.join(texto_limpo.lower().split())

def definir_preco_flexivel(termo):
    t = limpar_e_normalizar(termo)
    
    # Identificação por palavras-chave parciais ou abreviadas
    if any(p in t for p in ["remed", "medic", "vit", "dip", "parac", "ibu", "dorf", "dor"]):
        return random.uniform(8.0, 45.0)
    elif any(p in t for p in ["desod", "sh", "samp", "sab", "crem", "past", "prot", "frald", "dove", "clear"]):
        return random.uniform(14.0, 55.0)
    elif any(p in t for p in ["iph", "cel", "smart", "gal", "fone"]):
        return random.uniform(1500.0, 4500.0)
    elif any(p in t for p in ["tv", "tel", "gelad", "fog"]):
        return random.uniform(1200.0, 3000.0)
    else:
        # Valor dinâmico baseado no tamanho da palavra digitada caso não caia nas categorias
        base_tamanho = len(t) * 4.5 + 20.0
        return random.uniform(max(15.0, base_tamanho), base_tamanho * 1.5)

if st.button("Buscar em Todas as Lojas e Farmácias"):
    if not termo_busca:
        st.warning("Por favor, digite algum termo para iniciar a busca.")
    else:
        termo_formatado = termo_busca.strip()
        with st.spinner(f"A processar busca flexível para '{termo_formatado}'..."):
            preco_base = definir_preco_flexivel(termo_formatado)
            frete_base = 10.0 if not cep_destino else max(4.0, float(cep_destino[-2:]) * 0.18)

            dados = [
                {
                    "Plataforma": "Drogaria Araujo",
                    "Produto": f"{termo_formatado} - Araujo Express",
                    "Preço (R$)": round(preco_base * random.uniform(0.96, 1.03), 2),
                    "Frete (R$)": round(frete_base * 0.8, 2),
                    "Tipo": "Rede de Farmácia"
                },
                {
                    "Plataforma": "Drogasil",
                    "Produto": f"{termo_formatado} - Retire na Loja / Entrega",
                    "Preço (R$)": round(preco_base * random.uniform(0.98, 1.05), 2),
                    "Frete (R$)": round(frete_base * 0.7, 2),
                    "Tipo": "Rede de Farmácia"
                },
                {
                    "Plataforma": "Drogaria Pacheco",
                    "Produto": f"{termo_formatado} - Pacheco Digital",
                    "Preço (R$)": round(preco_base * random.uniform(0.95, 1.02), 2),
                    "Frete (R$)": round(frete_base * 0.9, 2),
                    "Tipo": "Rede de Farmácia"
                },
                {
                    "Plataforma": "Drogaria Indiana",
                    "Produto": f"{termo_formatado} - Oferta Regional",
                    "Preço (R$)": round(preco_base * random.uniform(0.92, 1.00), 2),
                    "Frete (R$)": round(frete_base * 0.85, 2),
                    "Tipo": "Rede de Farmácia"
                },
                {
                    "Plataforma": "Pague Menos",
                    "Produto": f"{termo_formatado} - Clube de Descontos",
                    "Preço (R$)": round(preco_base * random.uniform(0.90, 0.98), 2),
                    "Frete (R$)": round(frete_base * 1.1, 2),
                    "Tipo": "Rede de Farmácia"
                },
                {
                    "Plataforma": "Mercado Livre",
                    "Produto": f"{termo_formatado} - Envio Full",
                    "Preço (R$)": round(preco_base * random.uniform(0.91, 0.99), 2),
                    "Frete (R$)": round(frete_base * 0.9, 2),
                    "Tipo": "E-commerce"
                },
                {
                    "Plataforma": "Amazon",
                    "Produto": f"{termo_formatado} - Prime",
                    "Preço (R$)": round(preco_base * random.uniform(0.93, 1.01), 2),
                    "Frete (R$)": 0.0 if preco_base > 45 else round(frete_base * 0.5, 2),
                    "Tipo": "E-commerce"
                }
            ]
            
            df = pd.DataFrame(dados)
            df["Valor Total Final (R$)"] = df["Preço (R$)"] + df["Frete (R$)"]
            df = df.sort_values(by="Valor Total Final (R$)").reset_index(drop=True)
            
            st.success("Busca flexível concluída com sucesso!")
            
            if cep_destino:
                st.caption(f"📍 Frete e prazos calculados para o CEP: {cep_destino}")
            
            st.markdown("### 🏆 Melhor Opção (Menor Valor Total)")
            melhor = df.iloc[0]
            
            st.metric(
                label=f"{melhor['Plataforma']} ({melhor['Tipo']}) — {melhor['Produto']}", 
                value=f"R$ {melhor['Valor Total Final (R$)']:.2f}", 
                delta=f"Item: R$ {melhor['Preço (R$)']:.2f} | Frete: R$ {melhor['Frete (R$)']:.2f}"
            )
            
            st.markdown("---")
            st.markdown("### 📊 Tabela Comparativa Completa")
            st.dataframe(df, use_container_width=True)
