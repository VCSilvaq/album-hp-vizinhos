
import streamlit as st
import os
import pickle

ARQUIVO_VIZINHOS = "vizinhos.pkl"

# Funções para carregar e salvar vizinhos
def carregar_vizinhos():
    if os.path.exists(ARQUIVO_VIZINHOS):
        with open(ARQUIVO_VIZINHOS, "rb") as f:
            return pickle.load(f)
    return []

def salvar_vizinhos(lista_vizinhos):
    with open(ARQUIVO_VIZINHOS, "wb") as f:
        pickle.dump(lista_vizinhos, f)

# Carregar os vizinhos cadastrados
vizinhos = carregar_vizinhos()

st.title("📘 Álbum Harry Potter – Super Nosso")

st.markdown("## 🧍 Cadastro de Vizinhos para Troca de Figurinhas")

with st.form("form_vizinho"):
    nome = st.text_input("Seu nome ou apelido")
    predio = st.text_input("Nome do seu prédio")
    apartamento = st.text_input("Número do seu apartamento")

    figurinhas_total = list(range(1, 189))

    figurinhas_que_tenho = st.multiselect(
        "Figurinhas que você já tem",
        options=figurinhas_total
    )

    repetidas_input = st.text_input("Figurinhas repetidas (opcional, separadas por vírgula)")
    figurinhas_repetidas = [int(f.strip()) for f in repetidas_input.split(",") if f.strip().isdigit()]

    submitted = st.form_submit_button("Salvar cadastro")

    if submitted:
        novo_vizinho = {
            "nome": nome,
            "predio": predio,
            "ap": apartamento,
            "tem": figurinhas_que_tenho,
            "repetidas": figurinhas_repetidas
        }
        vizinhos.append(novo_vizinho)
        salvar_vizinhos(vizinhos)
        st.success("Cadastro salvo com sucesso!")

st.markdown("---")
st.markdown("## 🤝 Vizinho(a)s Cadastrado(a)s e Sugestões de Trocas")

if len(vizinhos) == 0:
    st.info("Nenhum vizinho cadastrado ainda.")
else:
    for v in vizinhos:
        st.markdown(f"### 🧍 {v['nome']} – Prédio {v['predio']} – Ap {v['ap']}")
        st.write(f"Figurinhas que tem: {sorted(v['tem'])}")
        st.write(f"Repetidas: {sorted(v['repetidas']) if v['repetidas'] else 'Nenhuma'}")
        st.markdown("---")

    st.markdown("### 🔍 Comparar com um vizinho específico")
    nomes_disponiveis = [f"{v['nome']} - {v['predio']} Ap {v['ap']}" for v in vizinhos]
    selecionado = st.selectbox("Selecione você (para ver quem pode trocar com você):", nomes_disponiveis)

    if selecionado:
        usuario = next(v for v in vizinhos if f"{v['nome']} - {v['predio']} Ap {v['ap']}" == selecionado)

        outros = [v for v in vizinhos if v != usuario]

        for outro in outros:
            tem_que_eu_preciso = sorted(set(outro['tem']) - set(usuario['tem']))
            eu_tenho_que_ele_precisa = sorted(set(usuario['tem']) - set(outro['tem']))
            posso_oferecer = sorted(set(usuario['repetidas']).intersection(outro['tem']))

            if tem_que_eu_preciso or posso_oferecer:
                st.markdown(f"#### 🔄 Troca possível com {outro['nome']} (Prédio {outro['predio']} – Ap {outro['ap']})")
                if tem_que_eu_preciso:
                    st.write(f"Ele(a) tem {tem_que_eu_preciso} que você ainda não tem.")
                if eu_tenho_que_ele_precisa:
                    st.write(f"Você tem {eu_tenho_que_ele_precisa} que ele(a) não tem.")
                if posso_oferecer:
                    st.write(f"Você pode oferecer de suas repetidas: {posso_oferecer}")
                st.markdown("---")
