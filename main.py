import streamlit as st
from util_analisador import *
import pandas as pd



sidebar()

menu_analisador()


tab1, tab2 = st.tabs(["Módulo Home Care", "Em construção"])


with tab1:

    arquivos = pdf_extract()


    for arquivo in arquivos:
        resultado = verifica_information(arquivo,
                                         padroes=padroes,
                                         subpadroes=subpadroes,
                                         stop_padroes=stop_padroes,
                                         stop_subpadroes=stop_subpadroes)



        resultado = capturar_nomes_advogados(resultado)


    if arquivos:
        # Converte o dicionário em um DataFrame para exibição em tabela
        df = pd.DataFrame.from_dict(resultado, orient='index')

        # Aplicar a função clean_value a todo o DataFrame
        df = df.map(clean_value)

        # Substituir valores NA por '--'
        df = df.fillna('--')

        with st.container():
            st.dataframe(df, height=600, width=800)  # O 'height' define a altura máxima antes de ativar a rolagem





