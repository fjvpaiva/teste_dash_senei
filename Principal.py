import streamlit as st
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

# Função para exibir a página Principal
def pagina_principal():
    st.title("Página Principal")
    st.write("Bem-vindo à página Principal! Aqui você pode acessar as outras páginas.")

    # Links para as páginas subalternas
    if st.button("Insumos e Drawback"):
        st.session_state["pagina_atual"] = "Insumos_Drawback"
        st.rerun()

    if st.button("Produção e Entregas"):
        st.session_state["pagina_atual"] = "Producao_Entregas"
        st.rerun()

    if st.button("Financeiro"):
        st.session_state["pagina_atual"] = "Financeiro"
        st.rerun()

# Função para exibir a página Insumos_Drawback
def pagina_insumos_drawback():
    # Caminho para o arquivo Insumos_Drawback.py
    caminho_insumos_drawback = r"C:\Users\fjvpa\PycharmProjects\PythonProject1\Insumos_Drawback.py"

    # Verifica se o arquivo existe
    if os.path.exists(caminho_insumos_drawback):
        # Lê e executa o conteúdo do arquivo
        with open(caminho_insumos_drawback, "r", encoding="utf-8") as file:
            exec(file.read())
    else:
        st.error("Arquivo Insumos_Drawback.py não encontrado!")

    # Botão para retornar à página Principal
    if st.button("Voltar à Página Principal"):
        st.session_state["pagina_atual"] = "Principal"
        st.rerun()

# Função para exibir a página Producao_Entregas
def pagina_producao_entregas():
    # Caminho para o arquivo Producao_Entregas.py
    caminho_producao_entregas = r"https://github.com/fjvpaiva/teste_dash_senei/blob/main/Producao_Entregas.py"
    

    # Verifica se o arquivo existe
    if os.path.exists(caminho_producao_entregas):
        # Lê e executa o conteúdo do arquivo
        with open(caminho_producao_entregas, "r", encoding="utf-8") as file:
            exec(file.read())
    else:
        st.error("Arquivo Producao_Entregas.py não encontrado!")

    # Botão para retornar à página Principal
    if st.button("Voltar à Página Principal"):
        st.session_state["pagina_atual"] = "Principal"
        st.rerun()

# Função para exibir a página Financeiro
def pagina_financeiro():
    # Caminho para o arquivo Financeiro.py
    caminho_financeiro = r"C:\Users\fjvpa\PycharmProjects\PythonProject1\Financeiro.py"

    # Verifica se o arquivo existe
    if os.path.exists(caminho_financeiro):
        # Lê e executa o conteúdo do arquivo
        with open(caminho_financeiro, "r", encoding="utf-8") as file:
            exec(file.read())
    else:
        st.error("Arquivo Financeiro.py não encontrado!")

    # Botão para retornar à página Principal
    if st.button("Voltar à Página Principal"):
        st.session_state["pagina_atual"] = "Principal"
        st.rerun()

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
                st.rerun()  # Recarrega a página após o login
            else:
                st.error("Usuário ou senha incorretos")

        # Bloqueia o acesso às outras páginas se não estiver logado
        if st.session_state["pagina_atual"] != "Principal":
            st.warning("Você precisa fazer login para acessar esta página.")
            st.session_state["pagina_atual"] = "Principal"
            st.rerun()
        return  # Impede a execução do restante do código se não estiver logado

    # Páginas após o login
    else:
        # Exibe o nome do usuário logado
        st.sidebar.write(f"Bem-vindo, {st.session_state['nome']}!")

        # Botão de logout
        if st.sidebar.button("Logout"):
            st.session_state["logado"] = False
            st.session_state["pagina_atual"] = "Principal"
            st.rerun()  # Recarrega a página após o logout

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



