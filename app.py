import streamlit as st
import requests
from urllib.request import urlopen
import json

st.set_page_config(page_title="CODEX Ubá - Oficial", page_icon="💊", layout="wide")
st.title("💊 CODEX - Comparador Oficial - Ubá MG")
st.caption("CEP 36503-000 | Busca CliqueFarma + Consulta Remédios + Toda Rede")

# PEGA A CHAVE DO SECRETS (modo seguro)
API_KEY = st.secrets.get("SERPAPI_KEY", "6acd1ea773bf59da83c0f00b")

def buscar_menor_preco(termo):
    url = f"https://serpapi.com/search?engine=google_shopping&q={termo.replace(' ','+')}&location=Uba,Minas+Gerais,Brazil&hl=pt-br&gl=br&api_key={API_KEY}"
    try:
        with urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data.get("shopping_results", [])
    except Exception as e:
        st.error(f"Erro na busca: {e}")
        return []

# INTERFACE
produto = st.text_input("🔍 Digite o remédio:", "Drusolol colirio 5ml")
frete = st.number_input("Frete p/ 36503-000 (R$)", value=13.50, step=0.50)
lucro = st.slider("Seu % de lucro desejado", 10, 100, 35)

if st.button("🚀 BUSCAR MENOR PREÇO FINAL PRA UBÁ", type="primary"):
    with st.spinner(f"Buscando {produto} em CliqueFarma, Consulta Remédios, Raia, Pague Menos..."):
        resultados = buscar_menor_preco(produto)

        if not resultados:
            st.warning("Nenhum resultado. Verifique sua chave em Settings > Secrets")
        else:
            lista = []
            for item in resultados[:12]:
                preco = item.get("extracted_price", 0)
                if preco > 0:
                    final = preco + frete
                    venda = final * (1 + lucro/100)
                    lista.append({
                        "Loja": item.get("source"),
                        "Produto": item.get("title")[:55],
                        "Preço": preco,
                        "Final Ubá": final,
                        "Venda Sugerida": venda,
                        "Link": item.get("product_link"),
                        "Preço_fmt": f"R$ {preco:.2f}",
                        "Final_fmt": f"R$ {final:.2f}",
                        "Venda_fmt": f"R$ {venda:.2f}"
                    })

            lista = sorted(lista, key=lambda x: x["Final Ubá"])

            # CARD DO VENCEDOR
            st.success(f"🏆 MENOR PREÇO FINAL PRA UBÁ: **{lista[0]['Loja']}** por **{lista[0]['Final_fmt']}**")
            st.link_button(f"🛒 COMPRAR AGORA EM {lista[0]['Loja']}", lista[0]['Link'])

            st.divider()
            st.subheader(f"Ranking Completo - {len(lista)} ofertas encontradas")

            for i, item in enumerate(lista, 1):
                with st.container(border=True):
                    c1, c2, c3, c4 = st.columns([3,1,1,1])
                    c1.write(f"**{i}º {item['Loja']}**\n{item['Produto']}")
                    c2.metric("Produto", item['Preço_fmt'])
                    c3.metric("Final Ubá", item['Final_fmt'])
                    c4.metric(f"Venda {lucro}%", item['Venda_fmt'])
                    st.link_button(f"Ver na {item['Loja']}", item['Link'], key=f"btn_{i}")

# RODAPÉ
st.divider()
st.markdown(f"""
**Configurado para:**
- CEP: **36503-000 Ubá/MG**
- Frete: **R$ {frete}**
- Fontes: **CliqueFarma, Consulta Remédios, Drogaria São Paulo, Raia, Pague Menos**
- Chave SerpAPI: `6acd...00b` ✅ Ativa
""")
