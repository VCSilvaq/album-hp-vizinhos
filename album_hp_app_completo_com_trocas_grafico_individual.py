
import streamlit as st
import os
import pickle
import matplotlib.pyplot as plt

ARQUIVO_VIZINHOS = "vizinhos.pkl"

# Carregar e salvar
def carregar_vizinhos():
    if os.path.exists(ARQUIVO_VIZINHOS):
        with open(ARQUIVO_VIZINHOS, "rb") as f:
            return pickle.load(f)
    return []

def salvar_vizinhos(lista_vizinhos):
    with open(ARQUIVO_VIZINHOS, "wb") as f:
        pickle.dump(lista_vizinhos, f)

vizinhos = carregar_vizinhos()
figurinhas_total = list(range(1, 189))

st.title("📘 Álbum Harry Potter – Super Nosso")

# Cadastro
st.markdown("## 🧍 Cadastro ou Atualização de Vizinhos")
with st.form("form_vizinho"):
    nome = st.text_input("Seu nome ou apelido")
    predio = st.text_input("Nome do seu prédio")
    apartamento = st.text_input("Número do seu apartamento")
    contato = st.text_input("Deseja doar figurinhas? Deixe um contato (opcional)")

    figurinhas_que_tenho = st.multiselect("Figurinhas que você já tem", options=figurinhas_total)
    repetidas_input = st.text_input("Figurinhas repetidas (opcional, separadas por vírgula)")
    figurinhas_repetidas = [int(f.strip()) for f in repetidas_input.split(",") if f.strip().isdigit()]
    submitted = st.form_submit_button("Salvar ou Atualizar")

    if submitted:
        atualizado = False
        for v in vizinhos:
            if v["nome"] == nome and v["predio"] == predio and v["ap"] == apartamento:
                v["tem"] = figurinhas_que_tenho
                v["repetidas"] = figurinhas_repetidas
                v["contato"] = contato
                atualizado = True
                break
        if not atualizado:
            vizinhos.append({
                "nome": nome,
                "predio": predio,
                "ap": apartamento,
                "tem": figurinhas_que_tenho,
                "repetidas": figurinhas_repetidas,
                "contato": contato
            })
        salvar_vizinhos(vizinhos)
        st.success("Cadastro atualizado com sucesso!" if atualizado else "Novo cadastro salvo com sucesso!")

# Registrar troca
st.markdown("---")
st.markdown("## 🔁 Registrar troca entre vizinhos")

if len(vizinhos) >= 2:
    nomes = [f"{v['nome']} - {v['predio']} Ap {v['ap']}" for v in vizinhos]
    col1, col2 = st.columns(2)
    with col1:
        usuario_sel = st.selectbox("Você", nomes, key="eu")
    with col2:
        parceiro_sel = st.selectbox("Com quem você trocou", nomes, key="vizinho")

    if usuario_sel != parceiro_sel:
        usuario = next(v for v in vizinhos if f"{v['nome']} - {v['predio']} Ap {v['ap']}" == usuario_sel)
        parceiro = next(v for v in vizinhos if f"{v['nome']} - {v['predio']} Ap {v['ap']}" == parceiro_sel)

        figurinha_recebida = st.number_input("Número da figurinha que você RECEBEU", min_value=1, max_value=188, step=1)
        figurinha_entregue = st.number_input("Número da figurinha que você ENTREGOU", min_value=1, max_value=188, step=1)

        if st.button("Confirmar troca"):
            if figurinha_recebida not in usuario["tem"]:
                usuario["tem"].append(figurinha_recebida)
            if figurinha_entregue in usuario["repetidas"]:
                usuario["repetidas"].remove(figurinha_entregue)
            if figurinha_entregue not in parceiro["tem"]:
                parceiro["tem"].append(figurinha_entregue)
            if figurinha_recebida in parceiro["repetidas"]:
                parceiro["repetidas"].remove(figurinha_recebida)
            salvar_vizinhos(vizinhos)
            st.success("Troca registrada e dados atualizados com sucesso!")

# Seção: Progresso individual
st.markdown("---")
st.markdown("## 📊 Veja seu progresso no álbum")
if len(vizinhos) >= 1:
    nomes_vizinhos = [f"{v['nome']} - {v['predio']} Ap {v['ap']}" for v in vizinhos]
    selecionado = st.selectbox("Selecione seu nome:", nomes_vizinhos, key="progresso")

    viz = next(v for v in vizinhos if f"{v['nome']} - {v['predio']} Ap {v['ap']}" == selecionado)
    total = 188
    preenchidas = len(set(viz["tem"]))
    faltantes = total - preenchidas
    porcentagem = int((preenchidas / total) * 100)

    st.write(f"Você já tem {preenchidas} figurinhas e faltam {faltantes} ({porcentagem}%).")

    fig, ax = plt.subplots()
    ax.pie([preenchidas, faltantes], labels=['Preenchidas', 'Faltantes'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    if preenchidas == total:
        st.success("🎉 Parabéns! Álbum completo! Agora você pode ajudar os vizinhos a completarem o deles também! 💛")

# Lista de vizinhos e sugestões de troca
st.markdown("---")
st.markdown("## 👥 Vizinho(a)s cadastrados")
for v in vizinhos:
    st.markdown(f"### 🧍 {v['nome']} – Prédio {v['predio']} – Ap {v['ap']}")
    st.write(f"Figurinhas que tem: {sorted(v['tem'])}")
    st.write(f"Repetidas: {sorted(v['repetidas']) if v['repetidas'] else 'Nenhuma'}")
    if v.get("contato"):
        st.write(f"📞 Contato para doações: {v['contato']}")
    st.markdown("---")

# SUGESTÕES DE TROCA
st.markdown("## 🔍 Sugestões de trocas entre vizinhos")
if len(vizinhos) >= 2:
    nomes_disponiveis = [f"{v['nome']} - {v['predio']} Ap {v['ap']}" for v in vizinhos]
    selecionado = st.selectbox("Selecione seu nome:", nomes_disponiveis, key="sugestao")

    if selecionado:
        usuario = next(v for v in vizinhos if f"{v['nome']} - {v['predio']} Ap {v['ap']}" == selecionado)
        outros = [v for v in vizinhos if v != usuario]

        for outro in outros:
            tem_que_eu_preciso = sorted(set(outro['tem']) - set(usuario['tem']))
            eu_tenho_que_ele_precisa = sorted(set(usuario['tem']) - set(outro['tem']))
            posso_oferecer = sorted(set(usuario['repetidas']).intersection(outro['tem']))

            if tem_que_eu_preciso or posso_oferecer:
                st.markdown(f"### 🔄 {outro['nome']} (Prédio {outro['predio']} – Ap {outro['ap']})")
                if tem_que_eu_preciso:
                    st.write(f"👉 Ele(a) tem: {tem_que_eu_preciso} que você ainda não tem.")
                if eu_tenho_que_ele_precisa:
                    st.write(f"🤝 Você tem: {eu_tenho_que_ele_precisa} que ele(a) não tem.")
                if posso_oferecer:
                    st.write(f"🎁 Você pode oferecer de suas repetidas: {posso_oferecer}")
                st.markdown("---")
