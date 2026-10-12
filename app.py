import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Comparador Ubá - CODEX", page_icon="💊")
st.title("💊 CODEX - Menor Preço Final - Ubá MG")
st.caption("CEP 36503-000 | Busca em CliqueFarma + Consulta Remédios")

# --- FUNÇÕES DE BUSCA ---

def buscar_cliquefarma(produto):
    try:
        url = f"https://www.cliquefarma.com.br/busca?term={produto.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')

        ofertas = []
        # CliqueFarma lista preços em cards
        for item in soup.select(".product-card,.item-produto")[:5]:
            nome = item.get_text()[:80]
            preco_texto = re.search(r'R\$\s*[\d.,]+', item.get_text())
            if preco_texto:
                preco = float(preco_texto.group().replace('R$','').replace('.','').replace(',','.'))
                ofertas.append({"loja": "CliqueFarma - Rede", "produto": nome.strip(), "preco": preco, "fonte": "CliqueFarma"})
        return ofertas
    except Exception as e:
        return [{"loja": "CliqueFarma", "produto": f"Erro: {e}", "preco": 0, "fonte": "CliqueFarma"}]

def buscar_consulta_remedios(produto):
    try:
        url = f"https://consultaremedios.com.br/busca?termo={produto.replace(' ', '%20')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')

        ofertas = []
        for item in soup.select(".product-item,.result-item")[:5]:
            preco_texto = re.search(r'R\$\s*[\d.,]+', item.get_text())
            if preco_texto:
                preco = float(preco_texto.group().replace('R$','').replace('.','').replace(',','.'))
                ofertas.append({"loja": "Consulta Remédios - Melhor", "produto": produto, "preco": preco, "fonte": "CR"})
        return ofertas
    except Exception as e:
        return [{"loja": "Consulta Remédios", "produto": f"Erro: {e}", "preco": 0, "fonte": "CR"}]

# --- INTERFACE ---
produto = st.text_input("Digite o remédio:", "Dorflex 50 comprimidos")
cep = st.text_input("Seu CEP:", "36503-000")
frete_medio = st.slider("Frete médio pra Ubá (R$)", 0, 30, 13)

if st.button("🔍 BUSCAR MENOR PREÇO FINAL"):
    with st.spinner(f'Buscando {produto} em CliqueFarma e Consulta Remédios...'):

        # Busca nas duas fontes
        resultados_cf = buscar_cliquefarma(produto)
        resultados_cr = buscar_consulta_remedios(produto)

        todos = resultados_cf + resultados_cr
        # Filtra só com preço válido
        todos_validos = [x for x in todos if x['preco'] > 0]

        if not todos_validos:
            st.warning("Os sites bloquearam a busca automática. Isso é normal. Use a API oficial deles ou o modo manual abaixo.")
            st.info("DICA: CliqueFarma e Consulta Remédios bloqueiam robô. O jeito 100% que funciona é com SerpAPI.")
        else:
            # Calcula final
            for o in todos_validos:
                o['final'] = o['preco'] + frete_medio
                o['venda_sugerida'] = o['final'] * 1.35 # 35% lucro

            # Ordena pelo final
            ordenados = sorted(todos_validos, key=lambda x: x['final'])

            st.success(f"✅ MENOR PREÇO FINAL PRA {cep}: R$ {ordenados[0]['final']:.2f} em {ordenados[0]['loja']}")

            st.dataframe(ordenados)

            # Ranking visual
            st.subheader("🏆 Ranking Final com Frete pra Ubá")
            for i, o in enumerate(ordenados, 1):
                st.write(f"{i}º **{o['loja']}** | Produto R$ {o['preco']:.2f} + Frete R$ {frete_medio} = **R$ {o['final']:.2f}** | Venda sugerida R$ {o['venda_sugerida']:.2f}")

st.divider()
st.markdown("**Como fazer funcionar 100% sem bloqueio:** 1. Cria conta grátis no serpapi.com 2. Me fala que eu integro em 2 minutos no seu app.")
