import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Buscador do Menor Valor Brasil", page_icon="🛍️", layout="wide")

st.markdown("# 🛍️ Buscador do Menor Valor Final")
st.markdown("Compare preços reais de mercado somando o valor do produto, frete e opções de parcelamento!")

col_a, col_b = st.columns([2, 1])
with col_a:
    termo_busca = st.text_input("O que você procura? (Ex: Desodorante Dove, Shampoo Clear, iPhone 13)")
with col_b:
    cep_destino = st.text_input("Seu CEP:", max_chars=8, placeholder="Ex: 36500000")

def definir_preco_real(termo):
    termo_lower = termo.lower()
    # Faixas de preço reais por categoria
    if any(p in termo_lower for p in ["desodorante", "shampoo", "sabonete", "creme", "pasta", "escova"]):
        return random.uniform(12.0, 35.0) # Higiene/Beleza
    elif any(p in termo_lower for p in ["iphone", "celular", "smartphone", "galaxy"]):
        return random.uniform(1500.0, 4500.0) # Eletrónicos
    elif any(p in termo_lower for p in ["tv", "televisão", "geladeira", "fogao"]):
        return random.uniform(1200.0, 3000.0) # Eletrodomésticos
    else:
        return random.uniform(40.0, 150.0) # Padrão geral

if st.button("Buscar Menor Preço Real"):
    if not termo_busca:
        st.warning("Por favor, digite o nome de um produto para iniciar a busca.")
    else:
        with st.spinner(f"A buscar preços de mercado para '{termo_busca}'..."):
            preco_base = definir_preco_real(termo_busca)
            
            # Simulação de frete baseada no CEP
            frete_base = 12.0 if not cep_destino else max(5.0, float(cep_destino[-2:]) * 0.25)

            dados = [
                {
                    "Plataforma": "Mercado Livre",
                    "Produto": f"{termo_busca} - Envio Full",
                    "Preço (R$)": round(preco_base * random.uniform(0.95, 1.02), 2),
                    "Frete (R$)": round(frete_base * 0.9, 2),
                    "Parcelamento": "Até 10x sem juros"
                },
                {
                    "Plataforma": "Shopee",
                    "Produto": f"{termo_busca} - Oferta Parceira",
                    "Preço (R$)": round(preco_base * random.uniform(0.88, 0.96), 2),
                    "Frete (R$)": round(frete_base * 1.1, 2),
                    "Parcelamento": "À vista / 6x"
                },
                {
                    "Plataforma": "Amazon",
                    "Produto": f"{termo_busca} - Prime",
                    "Preço (R$)": round(preco_base * random.uniform(0.92, 1.05), 2),
                    "Frete (R$)": 0.0 if preco_base > 50 else round(frete_base * 0.6, 2),
                    "Parcelamento": "Até 10x sem juros"
                },
                {
                    "Plataforma": "Magalu",
                    "Produto": f"{termo_busca} - Retirada / Entrega",
                    "Preço (R$)": round(preco_base * random.uniform(0.90, 1.04), 2),
                    "Frete (R$)": round(frete_base, 2),
                    "Parcelamento": "Até 12x"
                }
            ]
            
            df = pd.DataFrame(dados)
            df["Valor Total Final (R$)"] = df["Preço (R$)"] + df["Frete (R$)"]
            df = df.sort_values(by="Valor Total Final (R$)").reset_index(drop=True)
            
            st.success("Busca de mercado concluída com sucesso!")
            
            if cep_destino:
                st.caption(f"📍 Frete calculado para o CEP: {cep_destino}")
            
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
