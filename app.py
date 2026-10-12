import streamlit as st
import requests

st.set_page_config(page_title="CODEX Ubá 100% - Final", page_icon="💊")
st.title("💊 CODEX 100% - Sem Bloqueio - Ubá MG")
st.caption("CEP 36503-000 | CliqueFarma + Consulta Remédios via Google Shopping")

# --- CONFIGURAÇÃO ---
API_KEY = st.secrets.get("SERPAPI_KEY", "SUA_CHAVE_AQUI") # Cola sua chave aqui ou no Secrets do Streamlit
CEP = "36503-000"

def buscar_google_shopping(termo):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_shopping",
        "q": termo,
        "location": "Ubá, Minas Gerais, Brazil",
        "hl": "pt-br",
        "gl": "br",
        "api_key": API_KEY
    }
    r = requests.get(url, params=params, timeout=15)
    data = r.json()
    return data.get("shopping_results", [])

# --- INTERFACE ---
produto = st.text_input("Remédio:", "Drusolol colirio 5ml")
frete = st.number_input(f"Frete médio pra {CEP} (R$)", value=13.50)

if st.button("🔍 BUSCAR AGORA - SEM BLOQUEIO"):
    if "SUA_CHAVE" in API_KEY:
        st.error("⚠️ Cola sua chave do SerpAPI na linha API_KEY =...")
        st.stop()

    with st.spinner(f"Buscando {produto} no Brasil todo..."):
        resultados = buscar_google_shopping(produto)

        if not resultados:
            st.error("Nenhum resultado. Verifique sua chave.")
            st.stop()

        # Processa e calcula final
        lista_final = []
        for item in resultados[:10]:
            preco = item.get("extracted_price", 0)
            if preco > 0:
                lista_final.append({
                    "Loja": item.get("source", "Farmácia"),
                    "Produto": item.get("title", "")[:60],
                    "Preço Produto": f"R$ {preco:.2f}",
                    "Preço Final p/ Ubá": f"R$ {preco + frete:.2f}",
                    "Link": item.get("product_link", ""),
                    "preco_float": preco,
                    "final_float": preco + frete,
                    "venda_sugerida": (preco + frete) * 1.35
                })

        # Ordena pelo final
        lista_final = sorted(lista_final, key=lambda x: x['final_float'])

        if lista_final:
            st.success(f"✅ MENOR PREÇO FINAL PRA UBÁ: {lista_final[0]['Loja']} - {lista_final[0]['Preço Final p/ Ubá']}")
            st.balloons()

            for i, item in enumerate(lista_final, 1):
                col1, col2 = st.columns([3,1])
                with col1:
                    st.write(f"**{i}º {item['Loja']}** - {item['Produto']}")
                    st.write(f"Produto: {item['Preço Produto']} + Frete R$ {frete} = **{item['Preço Final p/ Ubá']}** | Venda sugerida: R$ {item['venda_sugerida']:.2f}")
                    st.link_button("Ir pra loja", item['Link'])
                with col2:
                    st.metric("Final Ubá", item['Preço Final p/ Ubá'])
                st.divider()

            st.dataframe(lista_final)

st.divider()
st.info(f"💡 Dica: Esse modo busca em CliqueFarma, Consulta Remédios, Droga Raia, Pague Menos, etc - tudo via Google Shopping. Nunca é bloqueado.")
