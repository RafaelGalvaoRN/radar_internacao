import re
import time

import streamlit as st
from PyPDF2 import PdfReader
from padroes_regex import padroes, subpadroes, \
    stop_padroes, stop_subpadroes


def menu_analisador():
    st.title("Sistema de análise de processos de Internação Hospitalar")


def pdf_extract():
    arquivos = st.file_uploader("Junte os PDF's aqui", type="PDF", accept_multiple_files=True)
    return arquivos




def tratar_texto(texto: str) -> str:
    # Remove quebras de linha (substitui por um espaço)
    texto_sem_quebras = texto.replace("\n", " ").replace("\r", " ")

    # Substitui múltiplos espaços por apenas um espaço
    texto_tratado = re.sub(r'\s+', ' ', texto_sem_quebras)

    # Remove espaços no início e no fim
    texto_tratado = texto_tratado.strip()

    return texto_tratado


# def get_text(text, pattern, subpattern=None):
#     result = None
#
#     print(f"Analisando padrao {pattern}")
#
#     main_pattern = re.compile(pattern, re.IGNORECASE)
#
#     main_match = main_pattern.search(text)
#
#     if main_match:
#         print('Achei main', main_match)
#         result = main_match.group()
#
#         if subpattern:
#             print('Achei sub', main_match)
#             sub_pattern = re.compile(subpattern, re.IGNORECASE)
#
#             sub_match = sub_pattern.search(result)
#
#             if sub_match:
#                 result = sub_match.group()
#
#     return result

# def get_text(text, pattern, subpattern=None):
#     result = None
#
#     print(f"Analisando padrao {pattern}")
#
#     main_pattern = re.compile(pattern, re.IGNORECASE)
#
#     main_match = main_pattern.search(text)
#
#     if main_match:
#         print('Achei main', main_match.group())
#         # Use group(1) to get the content of the capturing group
#         if main_match.lastindex:
#             result = main_match.group(1)
#         else:
#             result = main_match.group()
#
#         if subpattern:
#             print('Analisando subpadrao', subpattern)
#             sub_pattern = re.compile(subpattern, re.IGNORECASE)
#
#             sub_match = sub_pattern.search(result)
#
#             if sub_match:
#                 result = sub_match.group()
#
#     return result

def get_text(text: str, pattern: str, subpattern: str = None) -> str:
    """
    Searches for a pattern in the text and optionally applies a subpattern.

    Args:
        text (str): The text to search in.
        pattern (str): The main regular expression pattern.
        subpattern (str): An optional subpattern for further matching.

    Returns:
        str: The matched text, or None if no match is found.
    """
    result = None
    print(f"Analyzing pattern: {pattern}")

    main_pattern = re.compile(pattern, re.IGNORECASE)
    main_match = main_pattern.search(text)

    if main_match:
        print('Main match found:', main_match.group())
        # Use group(1) if there's a capturing group; otherwise, use the full match
        result = main_match.group(1) if main_match.lastindex else main_match.group()

        # If a subpattern is provided, apply it to the result
        if subpattern:
            print('Analyzing subpattern:', subpattern)
            sub_pattern = re.compile(subpattern, re.IGNORECASE)
            sub_match = sub_pattern.search(result)

            if sub_match:
                result = sub_match.group()
            else:
                result = None  # Subpattern did not match

    else:
        print('No match found for pattern:', pattern)

    return result

# Função para limpar os valores do dicionário
def clean_value(val):
    if isinstance(val, dict):
        # Extrair os valores de 'found_text' e 'page'
        found_text = val.get('found_text', '')
        page = val.get('page', '')
        # Concatenar os dois valores, se ambos existirem
        if found_text and page:
            return f"{found_text} (página: {page})"
        elif found_text:
            return found_text
        elif page:
            return f"(página: {page})"
    return val  # Retorna o valor original se não for dicionário



def verifica_information(arquivo: str,
                         padroes: dict,
                         subpadroes: dict = None,
                         stop_padroes: dict = None,
                         stop_subpadroes: dict = None) -> dict:
    """
    Verifies information in a PDF file by searching for specified patterns.

    Args:
        arquivo (str): Path to the PDF file to be analyzed.
        padroes (dict): Dictionary of main patterns to search for.
        subpadroes (dict): Dictionary of subpatterns to refine matches.
        stop_padroes (dict): Flags to stop searching a pattern after finding it once.
        stop_subpadroes (dict): Flags to stop searching a subpattern after finding it once.

    Returns:
        dict: A dictionary containing the results found in the PDF.
    """

    results = {}
    reader = PdfReader(arquivo)
    total_pages = len(reader.pages)

    # Initialize pattern status tracking
    patterns_status = {}
    for label in padroes.keys():
        patterns_status[label] = {
            'found': False,  # Whether the pattern has been found
            'stop': stop_padroes.get(label, False) if stop_padroes else False,
            # Whether to stop after finding the pattern
            'sub_stop': stop_subpadroes.get(label, False) if stop_subpadroes else False  # Same for subpattern
        }

    # Iterate over each page of the PDF
    for page_number in range(total_pages):
        print(f"Processing page {page_number + 1} of {total_pages}")
        page = reader.pages[page_number]
        text = page.extract_text()

        if text:

            # if page_number == 368:
            #     print(text)
            #     time.sleep(5000)


            # Preprocess the extracted text
            texto_tratado = tratar_texto(text)
            print(f"Analyzing page {page_number + 1}")
            print(f"Processed text: {texto_tratado[:500]}...\n")  # Show a snippet of the text



            # Iterate over each label and its associated pattern
            for label, padrao in padroes.items():
                # Check if we should continue searching for this pattern
                if patterns_status[label]['found'] and patterns_status[label]['stop']:
                    continue  # Skip this pattern since it's already found and stop is True

                subpattern = subpadroes.get(label) if subpadroes else None

                print(f"Searching for pattern '{label}': {padrao}")
                resultado = get_text(texto_tratado, padrao, subpattern)

                if resultado:
                    print(f"Found result for '{label}' on page {page_number + 1}: {resultado}")
                    # Initialize the list for this label if not already done
                    if label not in results:
                        results[label] = []

                    # Append the result to the list
                    results[label].append({
                        'page': page_number + 1,
                        'found_text': resultado
                    })

                    # Update the found status
                    patterns_status[label]['found'] = True

                    # Check if we should stop searching for this pattern
                    if patterns_status[label]['stop']:
                        print(f"Stopping search for pattern '{label}' as per stop condition.")
                        # Continue to next pattern without searching further for this one
                        continue

                    # Check if we should stop searching for the subpattern
                    if subpattern and patterns_status[label]['sub_stop']:
                        print(f"Stopping search for subpattern of '{label}' as per stop condition.")
                        # You can set a flag or handle as needed
                        # For now, we just note that subpattern has been found

    return results

# def verifica_information(arquivo,
#                          funcoes: list,
#                          padroes: dict,
#                          subpadroes: dict = None,
#                          stop_padroes: dict = None,
#                          stop_subpadroes: dict = None) -> dict:
#
#     results = {}
#     reader = PdfReader(arquivo)
#     total_pages = len(reader.pages)
#     stop_processing = False  # Flag para controlar a parada
#
#
#     # Step 1: Itera sobre cada página do PDF
#     for i in range(total_pages):
#         print(f"Página {i+1} de {total_pages}")
#         page = reader.pages[i]
#         text = page.extract_text()
#         #
#         # if i == 54:
#         #     print("textto", text)
#         #     texto_tratado = tratar_texto(text)
#         #
#         #     autor_pattern = r"AUTOR:\s*([A-ZÁÉÍÓÚÇãáàéíóúç\s]+)\.?"
#         #
#         #     autor_match = re.search(autor_pattern, texto_tratado)
#         #
#         #     if autor_match:
#         #         print(f"Autor: {autor_match.group()}")
#         #
#         #     time.sleep(500000)
#
#         if text:
#             texto_tratado = tratar_texto(text)
#
#
#             for funcao in funcoes:
#                 # Itera sobre os rótulos e seus respectivos padrões
#                 for rotulo, padrao in padroes.items():
#                     # Obtém o subpadrão correspondente, se existir
#                     subpattern = subpadroes.get(rotulo)
#
#                     resultado = get_text(texto_tratado, padrao, subpattern)
#
#
#                     if resultado:
#                         print(f"Achei resultado para o rótulo '{rotulo}': {resultado}")
#                         # Se encontrar uma correspondência, adiciona aos resultados
#                         results[f'pagina_{i + 1}'] = {
#                             'rotulo': rotulo,
#                             'texto_encontrado': resultado
#                         }
#
#                         # Verifica se deve parar com base em `stop_padroes`
#                         if stop_padroes and stop_padroes.get(rotulo):
#                             stop_processing = True
#                             break
#
#                         # Verifica se deve parar com base em `stop_subpadroes`
#                         if stop_subpadroes and stop_subpadroes.get(rotulo):
#                             stop_processing = True
#                             break
#
#                     if stop_processing:  # Interrompe o loop interno se a flag for True
#                         break
#
#     return results
#
# def convert_to_df (dict: dict):
#
