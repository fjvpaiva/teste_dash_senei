import streamlit as st
import plotly as px
import requests #1
import os

st.set_page_config(layout="wide")

# Configuração das credenciais dos usuários (em texto plano para apresentação)
usuarios = {
    "silva_joao": {
        "nome": "João Silva",
        "senha": "abc123"  # Senha em texto plano
    }
}

# Função para verificar o login
def verificar_login(usuario, senha):
    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        return True
    return False

def pagina_principal():
    st.title("Página Principal")
    st.write("Bem-vindo à página Principal! Aqui você pode acessar as outras páginas.")

    # Links para as páginas subalternas
    if st.button("Insumos e Drawback"):
        st.session_state["pagina_atual"] = "Insumos_Drawback"

    if st.button("Produção e Entregas"):
        st.session_state["pagina_atual"] = "Producao_Entregas"

    if st.button("Financeiro"):
        st.session_state["pagina_atual"] = "Financeiro"

# Função para carregar e exibir um arquivo do GitHub
def carregar_arquivo_github(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            exec(response.text)  # Executa o código do arquivo
        else:
            st.error(f"Erro ao carregar o arquivo: {response.status_code}")
    except Exception as e:
        st.error(f"Erro ao executar o arquivo: {e}")

# Função para exibir a página Insumos_Drawback
def pagina_insumos_drawback():
    st.title("Insumos e Drawback")
    url_github = "https://raw.githubusercontent.com/fjvpaiva/teste_dash_senei/main/Insumos_Drawback.py"
    carregar_arquivo_github(url_github)

    # Botão para retornar à página Principal
    if st.button("Voltar à Página Principal"):
        st.session_state["pagina_atual"] = "Principal"

# Função para exibir a página Producao_Entregas
def pagina_producao_entregas():
    st.title("Produção e Entregas")
    url_github = "https://raw.githubusercontent.com/fjvpaiva/teste_dash_senei/main/Producao_Entregas.py"
    carregar_arquivo_github(url_github)

    # Botão para retornar à página Principal
    if st.button("Voltar à Página Principal"):
        st.session_state["pagina_atual"] = "Principal"

# Função para exibir a página Financeiro
def pagina_financeiro():
    st.title("Financeiro")
    url_github = "https://raw.githubusercontent.com/fjvpaiva/teste_dash_senei/main/Financeiro.py"
    carregar_arquivo_github(url_github)

    # Botão para retornar à página Principal
    if st.button("Voltar à Página Principal"):
        st.session_state["pagina_atual"] = "Principal"

# Lógica principal do aplicativo
def main():
    # Inicializa o estado da sessão para a página atual
    if "pagina_atual" not in st.session_state:
        st.session_state["pagina_atual"] = "Principal"

    # Verifica se o usuário está logado
    if "logado" not in st.session_state:
        st.session_state["logado"] = False

    # Página de Login
    if not st.session_state["logado"]:
        st.title("Página de Login")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Login"):
            if verificar_login(usuario, senha):
                st.session_state["logado"] = True
                st.session_state["nome"] = usuarios[usuario]["nome"]
                st.session_state["usuario"] = usuario
            else:
                st.error("Usuário ou senha incorretos")

        # Bloqueia o acesso às outras páginas se não estiver logado
        if st.session_state["pagina_atual"] != "Principal":
            st.warning("Você precisa fazer login para acessar esta página.")
            st.session_state["pagina_atual"] = "Principal"
        return  # Impede a execução do restante do código se não estiver logado

    # Páginas após o login
    else:
        # Exibe o nome do usuário logado
        st.sidebar.write(f"Bem-vindo, {st.session_state['nome']}!")

        # Botão de logout
        if st.sidebar.button("Logout"):
            st.session_state["logado"] = False
            st.session_state["pagina_atual"] = "Principal"

        # Navegação entre as páginas
        if st.session_state["pagina_atual"] == "Principal":
            pagina_principal()
        elif st.session_state["pagina_atual"] == "Insumos_Drawback":
            pagina_insumos_drawback()
        elif st.session_state["pagina_atual"] == "Producao_Entregas":
            pagina_producao_entregas()
        elif st.session_state["pagina_atual"] == "Financeiro":
            pagina_financeiro()

if __name__ == "__main__":
    main()



