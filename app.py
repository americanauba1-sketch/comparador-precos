import streamlit as st
import json
from urllib.request import urlopen
import urllib.parse

st.set_page_config(page_title="CODEX Ubá 10X", page_icon="🚀", layout="wide")
st.title("🚀 CODEX 10X - Ubá MG - Modo Turbo")
st.caption("CEP 36503-000 | Busca Original + Genérico + Similar + Melhor Lucro")

API_KEY = st.secrets.get("SERPAPI_KEY", "6acd1ea773bf59da83c0f00b")

def busca_shopping(termo):
    q = urllib.parse.quote(termo)
    url = f"https://serpapi.com/search?engine=google_shopping&q={q}&location=Uba,Minas+Gerais&hl=pt-br&gl=br&api_key={API_KEY}"
    try:
        with urlopen(url, timeout=20) as r:
            data = json.loads(r.read().decode())
            return data.get("shopping_results", [])
    except:
        return []

# MAPA DE GENÉRICOS INTELIGENTE
GENERICO_MAP = {
    "drusolol": ["cloridrato de dorzolamida 20mg/ml + maleato de timolol 5mg/ml", "dorzolamida timolol generico 5ml", "dorzolamida timolol EMS"],
    "dorflex": ["dipirona citrato orfenadrina cafeina generico", "dorflex generico 50 comprimidos"],
}

def get_genericos(nome):
    nome_low = nome.lower()
    for chave, lista in GENERICO_MAP.items():
        if chave in nome_low:
            return lista
    return [f"{nome} generico", f"{nome} similar"]

# INTERFACE TURBO
produto = st.text_input("Remédio:", "Drusolol")
col1, col2, col3 = st.columns(3)
with col1:
    frete = st.number_input(f"Frete 36503-000", value=13.50)
with col2:
    lucro = st.slider("Lucro %", 10, 100, 35)
with col3:
    buscar_generico = st.checkbox("🚀 Buscar genérico 10X mais barato?", value=True)

if st.button("🚀 ATIVAR MODO 10X PRA UBÁ", type="primary"):
    termos = [produto]
    if buscar_generico:
        termos += get_genericos(produto)

    todos_resultados = []
    with st.spinner(f"Buscando {len(termos)} variações em CliqueFarma, CR, Raia, Pague Menos..."):
        for termo in termos:
            res = busca_shopping(termo)
            for item in res[:6]:
                preco = item.get("extracted_price", 0)
                if preco > 0:
                    todos_resultados.append({
                        "termo_buscado": termo,
                        "loja": item.get("source"),
                        "titulo": item.get("title"),
                        "preco": preco,
                        "final": preco + frete,
                        "venda": (preco + frete) * (1+lucro/100),
                        "economia_vs_original": 0,
                        "link": item.get("product_link"),
                        "eh_generico": "generico" in termo.lower() or termo!= produto
                    })

    if not todos_resultados:
        st.error("Sem resultados. Verifique sua chave em Secrets")
    else:
        # Calcula economia
        originais = [x for x in todos_resultados if not x['eh_generico']]
        genericos = [x for x in todos_resultados if x['eh_generico']]
        menor_original = min([x['final'] for x in originais]) if originais else 999

        for g in genericos:
            g['economia_vs_original'] = menor_original - g['final']

        todos_resultados = sorted(todos_resultados, key=lambda x: x['final'])

        # DASHBOARD 10X
        st.success(f"🏆 MODO 10X: {len(todos_resultados)} ofertas encontradas pra Ubá")

        m1, m2, m3 = st.columns(3)
        m1.metric("Menor Final Ubá", f"R$ {todos_resultados[0]['final']:.2f}", f"{todos_resultados[0]['loja']}")
        if genericos:
            menor_gen = min(genericos, key=lambda x: x['final'])
            m2.metric("Menor Genérico", f"R$ {menor_gen['final']:.2f}", f"Economia R$ {menor_gen['economia_vs_original']:.2f}", delta_color="normal")
        m3.metric("Lucro Médio Sugerido", f"{lucro}%", f"Venda R$ {todos_resultados[0]['venda']:.2f}")

        st.divider()

        # ABAS
        tab1, tab2, tab3 = st.tabs(["🏆 Ranking Final Ubá", "💊 Só Genéricos (10X)", "📊 Planilha Lucro"])

        with tab1:
            for i, item in enumerate(todos_resultados, 1):
                tag = "💊 GENÉRICO -70%" if item['eh_generico'] else "Original"
                cor = "green" if item['eh_generico'] else "blue"
                with st.container(border=True):
                    st.markdown(f"**{i}º {item['loja']}** :{cor}[{tag}]")
                    st.write(f"{item['titulo'][:70]}")
                    c1, c2, c3, c4 = st.columns(4)
                    c1.write(f"Busca: {item['termo_buscado']}")
                    c2.metric("Final Ubá", f"R$ {item['final']:.2f}")
                    c3.metric("Venda", f"R$ {item['venda']:.2f}")
                    if item['eh_generico']:
                        c4.metric("Economia", f"R$ {item['economia_vs_original']:.2f}")
                    st.link_button(f"Comprar na {item['loja']}", item['link'])

        with tab2:
            if genericos:
                gens_ordenados = sorted(genericos, key=lambda x: x['final'])
                for g in gens_ordenados:
                    st.write(f"✅ **{g['loja']}** - {g['titulo'][:60]} - **R$ {g['final']:.2f} final** - Economiza R$ {g['economia_vs_original']:.2f}")
            else:
                st.info("Nenhum genérico encontrado pra esse termo")

        with tab3:
            st.write("Planilha pronta pra importar no seu sistema de Ubá:")
            import pandas as pd
            df = pd.DataFrame([{"Loja": x['loja'], "Produto": x['titulo'][:40], "Custo+Frete": x['final'], "Venda Sugerida": x['venda'], "Lucro R$": x['venda']-x['final']} for x in todos_resultados])
            st.dataframe(df)
            st.download_button("📥 Baixar Planilha CSV Ubá", df.to_csv(index=False), "codex_uba_10x.csv", "text/csv")

st.info("💡 Modo 10X ativo com sua chave. Busca original + genérico + similar em 1 clique.")
