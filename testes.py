import re
from util_analisador import tratar_texto

texto = """
Processing page 1 of 1549
19/09/2024
Número: 0802303-87.2022.8.20.5162
Classe: PROCEDIMENTO COMUM CÍVEL
 Órgão julgador: 2ª Vara da Comarca de Extremoz
 Última distribuição : 19/08/2022
 Valor da causa: R$ 117.000,00
 Assuntos: Tratamento Domiciliar (Home Care)
 Segredo de justiça? NÃO
 Justiça gratuita? SIM
 Pedido de liminar ou antecipação de tutela? SIM

TJRN
PJe - Processo Judicial Eletrônico
Partes Procurador/Terceiro vinculado
MARIA DO SOCORRO HONORATO DA CONCEICAO
(AUTOR)ANDRE RODRIGUES GRESS registrado(a) civilmente como
ANDRE RODRIGUES GRESS (ADVOGADO)
RICARDO CESAR GOMES DA SILVA (ADVOGADO)
JOAO PAULO HONORATO DO NASCIMENTO (AUTOR) ANDRE RODRIGUES GRESS registrado(a) civilmente como
ANDRE RODRIGUES GRESS (ADVOGADO)
RICARDO CESAR GOMES DA SILVA (ADVOGADO)
MUNICÍPIO DE EXTREMOZ (REU)
Estado do Rio Grande do Norte (REU)
SECRETÁRIO DE SAÚDE DO ESTADO DO RIO GRANDE DO
NORTE (REU)
Município de Extremoz (REU)
SECRETARIA DE ESTADO DE SAÚDE PÚBLICA - SESAP
(REU)
MPRN - 1ª Promotoria Extremoz (CUSTOS LEGIS)
S M CAMPOS BARBOSA (TERCEIRO INTERESSADO) JOSE FIGUEIREDO DE LIMA JUNIOR (ADVOGADO)
Documentos
Id. Data Documento Tipo
87260702 19/08/2022
18:05Petição Inicial Petição Inicial
87260703 19/08/2022
18:05Ma DO SOCORRO INICIAL Petição
87260704 19/08/2022
18:05CamScanner 08-10-2022 08.27 Documento de Identificação
87260705 19/08/2022
18:05CamScanner 08-16-2022 09.51 Documento de Identificação
87260706 19/08/2022
18:05DOC-20220811-WA0056. Procuração
87260708 19/08/2022
18:05LAUDO Documento de Comprovação
87260710 19/08/2022
18:05CONFIANÇA HOME CARE ORÇAMENTO
DOLORESOutros documentos
87260712 19/08/2022
18:05ORÇAMENTO CUIDADOS MARIA DO SOCORRO Outros documentos
87260713 19/08/2022
18:05ORÇAMENTO PEM REMOVIDAS MARIA DO
SOCORROOutros documentos
87288735 23/08/2022
16:55Decisão Decisão
87564597 25/08/2022
16:44Certidão Certidão

"""

texto = tratar_texto(texto)

# Regex para capturar Autor e Réu
pattern = r"Partes Procurador/Terceiro vinculado\s*\(AUTOR\)"



# Procurar autor e réu no texto
padrao_match = re.search(pattern, texto, re.DOTALL)


# Exibir os resultados
if padrao_match:
    print(f"pesquisa: {padrao_match.group()}")
else:
    print("pesquisa não encontrado")

