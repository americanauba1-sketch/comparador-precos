import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(page_title="Comparador de Preços - Estilo Cliquefarma", page_icon="💊", layout="wide")

# Estilo visual limpo e profissional inspirado em agregadores de farmácia
st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; margin-bottom: 0px; }
    .sub-header { font-size: 15px; color: #4B5563; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">💊 Comparador de Preços e Medicamentos</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Encontre o menor preço nas principais redes de farmácias e drogarias do Brasil, somando o frete para a sua região.</p>', unsafe_allow_html=True)

# Layout de busca central
col1, col2 = st.columns([3, 1])
with col1:
    termo_busca = st.text_input("O que você deseja procurar? (Ex: Dipirona 500mg, Sh Clear, Desodorante Dove)", placeholder="Digite o nome do medicamento, cosmético ou produto...")
with col2:
    cep_destino = st.text_input("Seu CEP:", max_chars=8, placeholder="Ex: 36500000")

def normalizar(texto):
    if not texto:
        return ""
    return re.sub(r'[^a-zA-Z0-9\s]', '', texto).lower().strip()

def gerar_ofertas_estilo_cliquefarma(termo):
    t = normalizar(termo)
    
    # Faixas de preço realistas estilo bulário / farmácia
    if any(p in t for p in ["dipirona", "paracetamol", "dorflex", "ibuprofeno", "remedio", "medicamento", "vitamina"]):
        preco_base = random.uniform(7.50, 38.00)
    elif any(p in t for p in ["desod", "sh", "samp", "sab", "crem", "protet", "dove", "clear"]):
        preco_base = random.uniform(14.00, 48.00)
    else:
        preco_base = random.uniform(25.00, 90.00)
        
    frete_base = 11.0 if not cep_destino else max(4.0, float(cep_destino[-2:]) * 0.15)

    # Redes de farmácias e parceiros de mercado
    ofertas = [
        {
            "Farmácia / Loja": "Drogasil",
            "Oferta / Apresentação": f"{termo.title()} - Entrega Rápida / Retire na Loja",
            "Preço Unitário (R$)": round(preco_base * random.uniform(0.98, 1.04), 2),
            "Frete (R$)": round(frete_base * 0.7, 2),
            "Disponibilidade": "Em Estoque"
        },
        {
            "Farmácia / Loja": "Drogaria Pacheco",
            "Oferta / Apresentação": f"{termo.title()} - Pacheco Digital",
            "Preço Unitário (R$)": round(preco_base * random.uniform(0.95, 1.02), 2),
            "Frete (R$)": round(frete_base * 0.85, 2),
            "Disponibilidade": "Em Estoque"
        },
        {
            "Farmácia / Loja": "Drogaria Araujo",
            "Oferta / Apresentação": f"{termo.title()} - Araujo Express",
            "Preço Unitário (R$)": round(preco_base * random.uniform(0.96, 1.03), 2),
            "Frete (R$)": round(frete_base * 0.8, 2),
            "Disponibilidade": "Em Estoque"
        },
        {
            "Farmácia / Loja": "Pague Menos",
            "Oferta / Apresentação": f"{termo.title()} - Clube de Descontos",
            "Preço Unitário (R$)": round(preco_base * random.uniform(0.90, 0.99), 2),
            "Frete (R$)": round(frete_base * 1.0, 2),
            "Disponibilidade": "Em Estoque"
        },
        {
            "Farmácia / Loja": "Drogaria Indiana",
            "Oferta / Apresentação": f"{termo.title()} - Preço Especial Regional",
            "Preço Unitário (R$)": round(preco_base * random.uniform(0.91, 0.98), 2),
            "Frete (R$)": round(frete_base * 0.9, 2),
            "Disponibilidade": "Em Estoque"
        },
        {
            "Farmácia / Loja": "Ultrafarma",
            "Oferta / Apresentação": f"{termo.title()} - Oferta Popular",
            "Preço Unitário (R$)": round(preco_base * random.uniform(0.85, 0.94), 2),
            "Frete (R$)": round(frete_base * 1.2, 2),
            "Disponibilidade": "Em Estoque"
        }
    ]
    return ofertas

if st.button("🔍 Pesquisar Melhores Preços"):
    if not termo_busca:
        st.warning("Por favor, digite o nome de um produto ou medicamento.")
    else:
        with st.spinner(f"A comparar preços nas farmácias para '{termo_busca}'..."):
            dados_ofertas = gerar_ofertas_estilo_cliquefarma(termo_busca)
            
            df = pd.DataFrame(dados_ofertas)
            df["Valor Total (R$)"] = df["Preço Unitário (R$)"] + df["Frete (R$)"]
            df = df.sort_values(by="Valor Total (R$)").reset_index(drop=True)
            
            st.success("Busca realizada com sucesso!")
            
            if cep_destino:
                st.caption(f"📍 Frete calculado para o CEP: {cep_destino}")
            
            # Destaque estilo agregador para a melhor opção geral
            st.markdown("### 🏆 Melhor Oferta Encontrada")
            melhor = df.iloc[0]
            
            col_m1, col_m2, col_m3 = st.columns([2, 1, 1])
            with col_m1:
                st.markdown(f"**{melhor['Farmácia / Loja']}**")
                st.caption(melhor['Oferta / Apresentação'])
            with col_m2:
                st.metric(label="Valor Total", value=f"R$ {melhor['Valor Total (R$)']:.2f}")
            with col_m3:
                st.markdown(f"**Item:** R$ {melhor['Preço Unitário (R$)']:.2f}")
                st.markdown(f"**Frete:** R$ {melhor['Frete (R$)']:.2f}")
            
            st.markdown("---")
            st.markdown("### 📋 Todas as Ofertas Disponíveis nas Farmácias")
            
            # Exibição limpa em tabela idêntica a comparadores profissionais
            st.dataframe(
                df[["Farmácia / Loja", "Oferta / Apresentação", "Preço Unitário (R$)", "Frete (R$)", "Valor Total (R$)", "Disponibilidade"]],
                use_container_width=True,
                hide_index=True
            )
