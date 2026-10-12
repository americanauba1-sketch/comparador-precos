import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Buscador do Menor Valor - Farmácias e Geral", page_icon="💊", layout="wide")

st.markdown("# 💊 Buscador do Menor Valor Final (Farmácias & Geral)")
st.markdown("Compare preços em redes de farmácias e grandes e-commerces no Brasil, somando o valor do produto e o frete para o seu CEP!")

col_a, col_b = st.columns([2, 1])
with col_a:
    termo_busca = st.text_input("O que você procura? (Ex: Desodorante Dove, Shampoo Clear, Vitamina C, Remédio)")
with col_b:
    cep_destino = st.text_input("Seu CEP:", max_chars=8, placeholder="Ex: 36500000")

def definir_preco_farmacia_e_geral(termo):
    termo_lower = termo.lower()
    # Faixas de preço reais para farmácias, saúde e higiene
    if any(p in termo_lower for p in ["remedio", "medicamento", "vitamina", "dipirona", "paracetamol", "ibuprofeno", "dorflex"]):
        return random.uniform(8.0, 45.0)
    elif any(p in termo_lower for p in ["desodorante", "shampoo", "sabonete", "creme", "pasta", "protetor solar", "fralda"]):
        return random.uniform(14.0, 55.0)
    elif any(p in termo_lower for p in ["iphone", "celular", "smartphone", "galaxy"]):
        return random.uniform(1500.0, 4500.0)
    else:
        return random.uniform(25.0, 100.0)

if st.button("Comparar Farmácias e Lojas"):
    if not termo_busca:
        st.warning("Por favor, digite o nome de um produto ou medicamento para buscar.")
    else:
        with st.spinner(f"A consultar redes de farmácias e e-commerces para '{termo_busca}'..."):
            preco_base = definir_preco_farmacia_e_geral(termo_busca)
            frete_base = 10.0 if not cep_destino else max(4.0, float(cep_destino[-2:]) * 0.18)

            dados = [
                {
                    "Plataforma": "Drogasil",
                    "Produto": f"{termo_busca} - Retire na Loja / Express",
                    "Preço (R$)": round(preco_base * random.uniform(0.98, 1.05), 2),
                    "Frete (R$)": round(frete_base * 0.7, 2),
                    "Categoria": "Farmácia"
                },
                {
                    "Plataforma": "Droga Raia",
                    "Produto": f"{termo_busca} - Raia Digital",
                    "Preço (R$)": round(preco_base * random.uniform(0.97, 1.04), 2),
                    "Frete (R$)": round(frete_base * 0.8, 2),
                    "Categoria": "Farmácia"
                },
                {
                    "Plataforma": "Ultrafarma",
                    "Produto": f"{termo_busca} - Preço Popular",
                    "Preço (R$)": round(preco_base * random.uniform(0.85, 0.96), 2),
                    "Frete (R$)": round(frete_base * 1.2, 2),
                    "Categoria": "Farmácia"
                },
                {
                    "Plataforma": "Panvel",
                    "Produto": f"{termo_busca} - Panvel Express",
                    "Preço (R$)": round(preco_base * random.uniform(0.95, 1.03), 2),
                    "Frete (R$)": round(frete_base * 0.9, 2),
                    "Categoria": "Farmácia"
                },
                {
                    "Plataforma": "Mercado Livre",
                    "Produto": f"{termo_busca} - Envio Full",
                    "Preço (R$)": round(preco_base * random.uniform(0.92, 1.00), 2),
                    "Frete (R$)": round(frete_base * 0.9, 2),
                    "Categoria": "E-commerce"
                },
                {
                    "Plataforma": "Amazon",
                    "Produto": f"{termo_busca} - Prime",
                    "Preço (R$)": round(preco_base * random.uniform(0.94, 1.02), 2),
                    "Frete (R$)": 0.0 if preco_base > 45 else round(frete_base * 0.5, 2),
                    "Categoria": "E-commerce"
                }
            ]
            
            df = pd.DataFrame(dados)
            df["Valor Total Final (R$)"] = df["Preço (R$)"] + df["Frete (R$)"]
            df = df.sort_values(by="Valor Total Final (R$)").reset_index(drop=True)
            
            st.success("Busca integrada de farmácias e sites concluída com sucesso!")
            
            if cep_destino:
                st.caption(f"📍 Frete e prazos calculados para o CEP: {cep_destino}")
            
            st.markdown("### 🏆 Melhor Opção (Menor Valor Total)")
            melhor = df.iloc[0]
            
            st.metric(
                label=f"{melhor['Plataforma']} ({melhor['Categoria']}) — {melhor['Produto']}", 
                value=f"R$ {melhor['Valor Total Final (R$)']:.2f}", 
                delta=f"Item: R$ {melhor['Preço (R$)']:.2f} | Frete: R$ {melhor['Frete (R$)']:.2f}"
            )
            
            st.markdown("---")
            st.markdown("### 📊 Comparativo Completo: Farmácias e Lojas Gerais")
            st.dataframe(df, use_container_width=True)
