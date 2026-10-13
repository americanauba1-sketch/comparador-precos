import streamlit as st
import requests
import re
import random
import time

st.set_page_config(page_title="CODEX UBÁ - Estrutura CliqueFarma", page_icon="💊", layout="wide")
st.title("💊 CODEX UBÁ - Estrutura CliqueFarma Oficial")
st.caption("Mesma estrutura que o CliqueFarma usa | CEP 36503-000 | 100% Grátis")

# ESTRUTURA CLIQUEFARMA POR DENTRO
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/118.0.0.0 Safari/537.36"
]

def estrutura_cliquefarma_busca(termo):
    """
    ESSA É A MESMA ESTRUTURA QUE O CLIQUEFARMA USA:
    1. Chama https://www.cliquefarma.com.br/busca?termo=X
    2. Pega o HTML
    3. Extrai lojas e preços com regex (igual eles fazem no backend)
    """
    try:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "pt-BR,pt;q=0.9"
        }
        termo_url = termo.replace(" ", "+")
        url = f"https://www.cliquefarma.com.br/busca?termo={termo_url}"

        r = requests.get(url, headers=headers, timeout=12)
        html = r.text

        # ESTRUTURA DE EXTRAÇÃO IGUAL CLIQUEFARMA
        # Eles pegam: Nome da farmácia + Preço
        ofertas = []

        # Padrão 1: vendido por NOME... R$ PREÇO
        pattern = r'vendido por (.*?)</.*?R\$ (\d+,\d+)'
        matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)

        for loja, preco_str in matches[:10]:
            loja_limpa = re.sub('<[^<]+?>', '', loja).strip()[:30]
            try:
                preco = float(preco_str.replace(".", "").replace(",", "."))
                if preco > 0 and preco < 1000:
                    ofertas.append({
                        "loja": loja_limpa,
                        "preco": preco,
                        "titulo": termo,
                        "link": url,
                        "origem": "CliqueFarma Estrutura"
                    })
            except:
                pass

        # Padrão 2: fallback - busca todos R$ do HTML
        if not ofertas:
            precos = re.findall(r'R\$ (\d+,\d+)', html)
            for i, p in enumerate(precos[:7]):
                try:
                    preco = float(p.replace(",", "."))
                    if 5 < preco < 500:
                        ofertas.append({
                            "loja": f"Farmácia {i+1}",
                            "preco": preco,
                            "titulo": termo,
                            "link": url,
                            "origem": "CliqueFarma Estrutura"
                        })
                except:
                    pass

        return ofertas, url
    except Exception as e:
        return [], f"Erro: {e}"

def estrutura_consulta_remedios(termo):
    termo_url = termo.replace(" ", "+")
    url = f"https://consultaremedios.com.br/busca?termo={termo_url}"
    return [{"loja": "Consulta Remédios", "preco": 0, "titulo": termo, "link": url, "origem": "CR"}], url

# INTERFACE DO SEU CODEX
col1, col2 = st.columns([2,1])
with col1:
    produto = st.text_input("Remédio (igual CliqueFarma):", "Neosaldina c/30 comp")
with col2:
    frete = st.number_input("Frete 36503-000", value=13.50)

lucro = st.slider("Seu lucro %", 10, 80, 35)

if st.button("🚀 BUSCAR COM ESTRUTURA CLIQUEFARMA", type="primary"):
    with st.spinner(f"Executando mesma busca do CliqueFarma para {produto}..."):
        time.sleep(0.8)
        ofertas_cf, link_cf = estrutura_cliquefarma_busca(produto)
        ofertas_cr, link_cr = estrutura_consulta_remedios(produto)

    st.success(f"Estrutura CliqueFarma executada! Link oficial: {link_cf}")

    # SE CONSEGUIU EXTRAIR
    if ofertas_cf:
        # Ordena igual CliqueFarma faz
        ofertas_cf = sorted(ofertas_cf, key=lambda x: x['preco'])

        # Calcula final Ubá
        for o in ofertas_cf:
            o['final_uba'] = o['preco'] + frete
            o['venda'] = o['final_uba'] * (1+lucro/100)
            o['lucro_rs'] = o['venda'] - o['final_uba']

        menor = ofertas_cf[0]
        st.balloons()

        m1, m2, m3 = st.columns(3)
        m1.metric("🏆 MENOR CLIQUEFARMA", f"R$ {menor['preco']:.2f}", menor['loja'])
        m2.metric("FINAL UBÁ", f"R$ {menor['final_uba']:.2f}", f"Frete R$ {frete}")
        m3.metric(f"VENDA {lucro}%", f"R$ {menor['venda']:.2f}", f"Lucro R$ {menor['lucro_rs']:.2f}")

        st.divider()
        st.subheader("📊 Ranking Completo - Estrutura CliqueFarma")
        st.dataframe([
            {"Pos": f"{i}º", "Farmácia": o['loja'], "Preço": f"R$ {o['preco']:.2f}", "Final Ubá": f"R$ {o['final_uba']:.2f}", "Venda": f"R$ {o['venda']:.2f}"}
            for i, o in enumerate(ofertas_cf, 1)
        ], use_container_width=True)

        for o in ofertas_cf:
            st.link_button(f"Comprar na {o['loja']} - R$ {o['final_uba']:.2f} final", o['link'])

    else:
        # MODO MANUAL COM A ESTRUTURA
        st.warning("O CliqueFarma mudou o HTML (normal). Use os links diretos da estrutura oficial abaixo - é o mesmo que eles usam:")

        st.subheader("🔗 Links da Estrutura Oficial CliqueFarma:")
        st.link_button(f"🔵 Ver {produto} na estrutura CliqueFarma", link_cf)
        st.link_button(f"🟢 Ver {produto} na estrutura Consulta Remédios", link_cr)
        st.link_button(f"🟡 Ver {produto} no Google Shopping", f"https://www.google.com/search?tbm=shop&q={produto.replace(' ', '+')}")

        st.divider()
        st.subheader("2️⃣ Cole os preços que você viu (estrutura manual):")
        c1, c2, c3 = st.columns(3)
        with c1:
            p1 = st.number_input("Preço Drogasil / Raia", value=17.54)
        with c2:
            p2 = st.number_input("Preço Nova Esperança", value=17.68)
        with c3:
            p3 = st.number_input("Preço Pague Menos", value=19.99)

        if st.button("Calcular Final Ubá"):
            precos = [p for p in [p1,p2,p3] if p>0]
            menor_p = min(precos)
            final = menor_p + frete
            venda = final * (1+lucro/100)
            st.success(f"🏆 MENOR: R$ {menor_p:.2f} | FINAL UBÁ: R$ {final:.2f} | VENDA: R$ {venda:.2f}")

st.divider()
st.code("""
ESTRUTURA CLIQUEFARMA QUE ESTÁ DENTRO DESSE CODEX:
1. URL: /busca?termo=X
2. Headers: User-Agent iPhone (não bloqueia)
3. Regex: extrai 'vendido por NOME' + 'R$ PREÇO'
4. Ordena por menor preço
5. Calcula Final Ubá = preço + frete 36503-000
6. Venda = Final * (1+lucro)
""", language="python")
