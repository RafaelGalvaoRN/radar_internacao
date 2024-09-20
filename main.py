import streamlit as st
from util_analisador import *
import pandas as pd


tab1, tab2 = st.tabs(["Analisador de Processo", "Em construção"])


with tab1:

    menu_analisador()
    arquivos = pdf_extract()


    for arquivo in arquivos:
        resultado = verifica_information(arquivo,
                                         padroes=padroes,
                                         subpadroes=subpadroes,
                                         stop_padroes=stop_padroes,
                                         stop_subpadroes=stop_subpadroes)




    print("terminei")
    if arquivos:
        # Converte o dicionário em um DataFrame para exibição em tabela
        df = pd.DataFrame.from_dict(resultado, orient='index')

        # Aplicar a função clean_value a todo o DataFrame
        df = df.map(clean_value)

        # Substituir valores NA por '--'
        df = df.fillna('--')

        st.table(df)  # Exibe o dicionário como uma tabela





