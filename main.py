import streamlit as st
from util_analisador import *
import pandas as pd



sidebar()

menu_analisador()

tab1, tab2 = st.tabs(["Módulo Home Care", "Em construção"])

# Adiciona estilo ao botão
# Adiciona estilo ao botão
st.markdown("""
    <style>
    .stButton button {
        background-color: #f0f0f0; /* Cor de fundo cinza claro */
        color: black; /* Cor do texto */
        border-radius: 10px; /* Bordas levemente arredondadas */
        padding: 8px 16px;
        font-size: 14px;
        border: 1px solid #d0d0d0; /* Borda leve */
    }
    .stButton button:hover {
        background-color: #e0e0e0; /* Cor um pouco mais escura ao passar o mouse */
    }
    </style>
    """, unsafe_allow_html=True)


with tab1:

    # Função para reiniciar a aplicação
    if st.button('Reiniciar Aplicação'):
        st.rerun()  # Reinicia a execução da aplicação

    arquivos = pdf_extract()

    resultados_tratados = []

    if st.button("Analisar arquivos"):
        for arquivo in arquivos:
            resultado = []



            resultado.append(verifica_information(arquivo,
                                             padroes=padroes,
                                             subpadroes=subpadroes,
                                             stop_padroes=stop_padroes,
                                             stop_subpadroes=stop_subpadroes))


            resultado_tratado = list(map(capturar_nomes_advogados, resultado))

            resultados_tratados.extend(resultado_tratado)


        # Itera sobre cada tabela tratada para exibi-las
        for i, tabela in enumerate(resultados_tratados):
            # Converte o dicionário em um DataFrame para exibição
            df = pd.DataFrame.from_dict(tabela, orient='index')

            # Aplica a função clean_value a todo o DataFrame
            df = df.map(clean_value)  # Modificação aqui para garantir que seja aplicada a cada valor

            # Substitui valores NA por '--'
            df = df.fillna('--')

            # Exibe cada DataFrame separadamente com um título ou header
            st.write(f"Tabela {i + 1} - Ref ao Processo {arquivos[i].name}")  # Título da tabela
            st.dataframe(df, height=600, width=2500)  # Exibe a tabela no Streamlit


