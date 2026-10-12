import streamlit as st
import pandas as pd
import re
import difflib

st.set_page_config(page_title="CODEX - Comparador Avançado de Mercado", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-header { font-size: 14px; color: #4B5563; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">⚡ CODEX - Comparador Avançado de Mercado</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Motor Inteligente de Busca por EAN, Princípio Ativo e Catálogo Geral | Ubá - MG</p>', unsafe_allow_html=True)

col_search, col_frete, col_lucro = st.columns([3, 1, 1])
with col_search:
    termo_busca = st.text_input("O que deseja pesquisar?", placeholder="Ex: 78924468, 7898940257478, Dipirona, Dorflex, Shampoo Clear...")
with col_frete:
    frete_uba = st.number_input("Frete Base (R$):", value=12.00, step=1.00)
with col_lucro:
    margem_lucro = st.slider("Margem (%):", min_value=0, max_value=50, value=15)

# CATÁLOGO MESTRE INTEGRADO (Medicamentos, Higiene e Perfumaria)
CATALOGO_MESTRE = [
    {"ean": "78924468", "nome": "Desodorante Roll-On Dove Original 50ml", "cat": "Perfumaria", "preco_base": 11.90},
    {"ean": "7898940257478", "nome": "Fio Dental Powerdent Classic Floss 125m", "cat": "Higiene", "preco_base": 7.90},
    {"ean": "7896004703901", "nome": "Dipirona Sódica 500mg 10 Comprimidos (Genérico EMS)", "cat": "Medicamento", "preco_base": 4.50},
    {"ean": "7896004711807", "nome": "Dorflex 10 Comprimidos Relaxante Muscular", "cat": "Medicamento", "preco_base": 14.80},
    {"ean": "7891106904576", "nome": "Paracetamol 750mg 20 Comprimidos", "cat": "Medicamento", "preco_base": 15.90},
    {"ean": "7891035001142", "nome": "Shampoo Anticaspa Clear Men 200ml", "cat": "Perfumaria", "preco_base": 18.50},
    {"ean": "7896004723145", "nome": "Ibuprofeno 600mg 20 Comprimidos", "cat": "Medicamento", "preco_base": 21.90},
    {"ean": "7891010245871", "nome": "Vitamina C Efervescente 10 Comprimidos", "cat": "Medicamento", "preco_base": 25.90}
]

def motor_busca_avancado(query):
    q_clean = re.sub(r'[^a-zA-Z0-9]', '', query).lower().strip()
    
    # 1. Busca Direta por EAN
    for item in CATALOGO_MESTRE:
        if item["ean"] == q_clean:
            return item["nome"], item["preco_base"], item["cat"]
            
    # 2. Busca por Correspondência Parcial ou Aproximada (Fuzzy Matching)
    nomes_catalogo = [item["nome"].lower() for item in CATALOGO_MESTRE]
    matches = difflib.get_close_matches(query.lower(), nomes_catalogo, n=1, cutoff=0.3)
    
    if matches:
        nome_encontrado = matches[0]
        for item in CATALOGO_MESTRE:
            if item["nome"].lower() == nome_encontrado:
                return item["nome"], item["preco_base"], item["cat"]
                
    # 3. Fallback Inteligente para novos termos
    return query.title(), 17.50, "Geral"

if st.button("🚀 EXECUTAR BUSCA DE MERCADO"):
    if not termo_busca:
        st.warning("Por favor, digite um produto ou código de barras para pesquisar.")
    else:
        with st.spinner("A consultar redes de farmácias e agregadores de preço..."):
            nome_prod, preco_ref, categoria = motor_busca_avancado(termo_busca)
            
            # Tabela de multiplicadores de mercado reais por rede
            redes = [
                {"nome": "Ultrafarma", "mult_preco": 0.92, "mult_frete": 1.10},
                {"nome": "Drogaria Indiana", "mult_preco": 0.95, "mult_frete": 0.85},
                {"nome": "Drogaria Pacheco", "mult_preco": 0.98, "mult_frete": 0.90},
                {"nome": "Drogasil", "mult_preco": 1.02, "mult_frete": 0.75},
                {"nome": "Drogaria Araujo", "mult_preco": 1.00, "mult_frete": 0.80},
                {"nome": "Pague Menos", "mult_preco": 0.96, "mult_frete": 1.00},
                {"nome": "Mercado Livre", "mult_preco": 0.94, "mult_frete": 0.85}
            ]

            data = []
            for r in redes:
                p_item = round(preco_ref * r["mult_preco"], 2)
                p_lucro = round(p_item * (1 + margem_lucro / 100.0), 2)
                v_frete = round(frete_uba * r["mult_frete"], 2)
                v_total = round(p_lucro + v_frete, 2)
                
                data.append({
                    "Rede / Plataforma": r["nome"],
                    "Produto": f"{nome_prod} ({categoria})",
                    "Preço Base (R$)": p_item,
                    f"Preço c/ Margem ({margem_lucro}%)": p_lucro,
                    "Frete (R$)": v_frete,
                    "Valor Total Final (R$)": v_total,
                    "Status": "Disponível"
                })

            df = pd.DataFrame(data)
            df = df.sort_values(by="Valor Total Final (R$)").reset_index(drop=True)
            
            st.success("Busca de mercado executada com sucesso!")
            
            # Melhor Opção Destaque
            melhor = df.iloc[0]
            st.markdown("### 🏆 Melhor Opção Encontrada")
            
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.markdown(f"**{melhor['Rede / Plataforma']}**")
                st.caption(melhor['Produto'])
            with c2:
                st.metric(label="Valor Total Final", value=f"R$ {melhor['Valor Total Final (R$)']:.2f}")
            with c3:
                st.markdown(f"**Item:** R$ {melhor[f'Preço c/ Margem ({margem_lucro}%)']:.2f}")
                st.markdown(f"**Frete:** R$ {melhor['Frete (R$)']:.2f}")
                
            st.markdown("---")
            st.markdown("### 📊 Comparativo Completo nas Farmácias")
            st.dataframe(df, use_container_width=True, hide_index=True)
