import streamlit as st
from supabase import create_client

SUPABASE_URL = "https://euwtrohuszgejvqgdqcc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV1d3Ryb2h1c3pnZWp2cWdkcWNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQzMTIyMDUsImV4cCI6MjA4OTg4ODIwNX0.h90TddvOhVQOCkN900LeVuo1TkWbTSTDqr-WyeJt31E"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(layout="wide")
st.title("🌍 Event OS Global")

# LOGIN
if "user" not in st.session_state:

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        user = supabase.table("usuarios")\
            .select("*")\
            .eq("email", email)\
            .execute().data

        if user and user[0]["senha"] == senha:
            st.session_state.user = user[0]
            st.rerun()
        else:
            st.error("Login inválido")

    st.stop()

user = st.session_state.user

# EVENTOS AUTORIZADOS
acessos = supabase.table("usuarios_eventos")\
    .select("id_evento")\
    .eq("id_usuario", user["id"])\
    .execute().data

event_ids = [a["id_evento"] for a in acessos]

eventos = supabase.table("eventos")\
    .select("*")\
    .in_("id", event_ids)\
    .execute().data

evento_nome = st.sidebar.selectbox(
"Evento ativo",
[e["nome"] for e in eventos]
)

evento = next(e for e in eventos if e["nome"] == evento_nome)
evento_id = evento["id"]

menu = st.sidebar.radio(
"Menu",
["Dashboard","Receitas","Despesas","Contratos","Documentos"]
)

# DASHBOARD
if menu == "Dashboard":

    receitas = supabase.table("receitas")\
        .select("*")\
        .eq("id_evento", evento_id)\
        .execute().data

    despesas = supabase.table("despesas")\
        .select("*")\
        .eq("id_evento", evento_id)\
        .execute().data

    total_receita = sum(r["valor"] for r in receitas) if receitas else 0
    total_despesa = sum(d["valor"] for d in despesas) if despesas else 0

    col1,col2,col3 = st.columns(3)

    col1.metric("Receita", total_receita)
    col2.metric("Despesa", total_despesa)
    col3.metric("Resultado", total_receita-total_despesa)

# RECEITAS
if menu == "Receitas":

    valor = st.number_input("Valor")
    desc = st.text_input("Descrição")
    cat = st.text_input("Categoria")

    if st.button("Salvar Receita"):

        supabase.table("receitas").insert({
            "id_evento":evento_id,
            "descricao":desc,
            "categoria":cat,
            "valor":valor
        }).execute()

        st.success("Receita registrada")

# DESPESAS
if menu == "Despesas":

    valor = st.number_input("Valor")
    desc = st.text_input("Descrição")
    cat = st.text_input("Categoria")

    if st.button("Salvar Despesa"):

        supabase.table("despesas").insert({
            "id_evento":evento_id,
            "descricao":desc,
            "categoria":cat,
            "valor":valor
        }).execute()

        st.success("Despesa registrada")

# CONTRATOS
if menu == "Contratos":

    fornecedor = st.text_input("Fornecedor")
    valor = st.number_input("Valor contrato")

    if st.button("Salvar"):

        supabase.table("contratos").insert({
            "id_evento":evento_id,
            "fornecedor":fornecedor,
            "valor":valor
        }).execute()

        st.success("Contrato salvo")

# DOCUMENTOS
if menu == "Documentos":

    st.write("Integração com storage pode ser ativada")