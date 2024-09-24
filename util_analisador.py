import re
import time

import streamlit as st
from PyPDF2 import PdfReader
from padroes_regex import padroes, subpadroes, \
    stop_padroes, stop_subpadroes, padroes_compilados


def menu_analisador():
    st.title("Sistema de Análise de Processos de Judicialização da Saúde - SAPJUS-MPRN")


def sidebar():
    st.sidebar.image("logo-mprn.png", width=150)
    st.sidebar.title("Menu Analisador de Processo")
    st.sidebar.markdown("""
    Capturas já implementadas:
    """)

    st.sidebar.markdown("""
    - ⚖️ **Número de Processo**
    - 🏛️ **Vara Judicial**
    - 👨‍💼 **Nome do Autor**
    - 👨‍💼 **Nome(s) do(s) Advogado(s)**
    - 👨‍💼 **Nome do Réu**
    - 💰 **Ordens de bloqueio com valores**
    - 🧾 **Notas Fiscais**
    - 📄 **Relatório do NAD/SESAP**
    - 📋 **Conclusão do Relatório do NAD/SESAP**
    - 💳 **Alvará Eletrônico de Pagamento**
    - ⚕️ **Solicitação Nota Técnica do NatJUS**
    - 📝 **NT NAT/JUS com conclusão**
    - ⚖️ **Decisão Interlocutória**
    - 📜 **Sentença**

    """)


def pdf_extract(total=5):

    arquivos = st.file_uploader(f"Junte os PDF's aqui - no máximo de {total}", type="PDF", accept_multiple_files=True)

    if len(arquivos) > total:
        st.error(f"Envie no máximo {total} arquivos")
        return None

    return arquivos


def get_execution_time(func):
    def wraper(*args, **kwargs):  # Accept any arguments
        start = time.time()
        result = func(*args, **kwargs)  # Pass arguments to the function
        end = time.time()
        st.write(f"Tempo de análise foi de {(end - start):.2f} segundos")
        return result  # Return the result of the wrapped function

    return wraper


def tratar_texto(texto: str) -> str:
    # Remove quebras de linha (substitui por um espaço)
    texto_sem_quebras = texto.replace("\n", " ").replace("\r", " ")

    # Substitui múltiplos espaços por apenas um espaço
    texto_tratado = re.sub(r'\s+', ' ', texto_sem_quebras)

    # Remove espaços no início e no fim
    texto_tratado = texto_tratado.strip()

    return texto_tratado


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

    # main_pattern = re.compile(pattern, re.IGNORECASE)
    main_pattern = pattern

    main_match = main_pattern.search(text)

    if main_match:
        print('Main match found:', main_match.group())
        # Use group(1) if there's a capturing group; otherwise, use the full match
        result = main_match.group(1) if main_match.lastindex else main_match.group()

        # If a subpattern is provided, apply it to the result
        if subpattern:
            print('Analyzing subpattern:', subpattern)
            print("Analisando texto por meio do subapptern; texto: ", result)
            sub_pattern = re.compile(subpattern, re.IGNORECASE)
            sub_match = sub_pattern.search(result)

            if sub_match:
                print(f'Subpattern {sub_match} match:',sub_match.group())
                result = sub_match.group()
            else:
                print(f'Subpattern dont match:')
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


@get_execution_time
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

    results = {k: [] for k in padroes.keys()}

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

            # if page_number == 287:
            #     print("imprimindo texto", text)
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


                #testando nova versao
                # resultado = get_text(texto_tratado, padrao, subpattern)

                padrao_compilado_pattern = padroes_compilados[label]
                resultado = get_text(texto_tratado, padrao_compilado_pattern, subpattern)

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


def capturar_nomes_advogados(result):
    try:
        # Verifica se result é uma lista
        if isinstance(result, list):
            # Se for uma lista, iterar sobre seus elementos
            for item in result:
                # Verifique se "👨‍💼Advogados" existe e se é uma lista não vazia
                if "👨‍💼Advogados" in item and isinstance(item["👨‍💼Advogados"], list) and len(item["👨‍💼Advogados"]) > 0:
                    texto = item["👨‍💼Advogados"][0].get("found_text", "")
                    if texto:
                        # Regex para capturar os nomes antes de "(ADVOGADO)"
                        padrao = r'\b[A-Z\s]+\b(?=\s+\(ADVOGADO\))'

                        # Encontrar os nomes de advogados
                        nomes_advogados = re.findall(padrao, texto)

                        # Removendo espaços desnecessários
                        nomes_advogados = [nome.strip() for nome in nomes_advogados]

                        # Atualizando o texto original com os nomes encontrados
                        item["👨‍💼Advogados"][0]["found_text"] = nomes_advogados if nomes_advogados else "--"
                else:
                    # Se a lista de advogados estiver vazia ou não existir, inicializar com "--"
                    item["👨‍💼Advogados"] = [{"found_text": "--"}]
        # Verifica se result é um dicionário
        elif isinstance(result, dict):
            if "👨‍💼Advogados" in result and isinstance(result["👨‍💼Advogados"], list) and len(result["👨‍💼Advogados"]) > 0:
                texto = result["👨‍💼Advogados"][0].get("found_text", "")
                if texto:
                    padrao = r'\b[A-Z\s]+\b(?=\s+\(ADVOGADO\))'
                    nomes_advogados = re.findall(padrao, texto)
                    nomes_advogados = [nome.strip() for nome in nomes_advogados]
                    result["👨‍💼Advogados"][0]["found_text"] = nomes_advogados if nomes_advogados else "--"
            else:
                result["👨‍💼Advogados"] = [{"found_text": "--"}]
        return result

    except Exception as e:
        print("Advogados não localizados: ", e)
        if isinstance(result, list):
            for item in result:
                if "👨‍💼Advogados" in item and len(item["👨‍💼Advogados"]) > 0:
                    item["👨‍💼Advogados"][0]["found_text"] = "--"
                else:
                    item["👨‍💼Advogados"] = [{"found_text": "--"}]
        elif isinstance(result, dict):
            if "👨‍💼Advogados" in result and len(result["👨‍💼Advogados"]) > 0:
                result["👨‍💼Advogados"][0]["found_text"] = "--"
            else:
                result["👨‍💼Advogados"] = [{"found_text": "--"}]
        return result
