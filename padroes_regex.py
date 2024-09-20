# Dictionary of main patterns to search for in the text, keyed by label
padroes = {
    "bloqueio_conta_salario": r"RECIBO DE PROTOCOLAMENTO DE BLOQUEIO DE VALORES.*Bloquear Conta-Salário",
    "conta_beneficiario_resgatada": r"conta.*beneficiário.*resgatada",
    "numero_processo": r"Processo:\s*\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}",
    "autor": r"AUTOR:\s*([A-ZÁÉÍÓÚÇãáàéíóúç\s]+)\.?",  # Captures the author's name
    "reu": r"REU:\s*([A-ZÁÉÍÓÚÇãáàéíóúç\s,]+)decisão?",
    "vara": r"poder judiciário do estado do rio grande do norte(.*?)processo",
    "nota fiscal": r"Nota Fiscal de Serviços Eletrônica - NFS-e",
    "nad\sesap": r"relatório.*Núcleo de Atenção Domiciliar da Secretaria de Estado da Saúde Pública",
    "conclusao nad\sesap": r"relatório.*Núcleo de Atenção Domiciliar da Secretaria de Estado da Saúde Pública.*natal/rn",
}

# Dictionary of subpatterns to further refine the search, keyed by label
subpadroes = {
    "bloqueio_conta_salario": r"R\$\s*\d{1,3}(?:\.\d{3})*,\d{2}",  # Captures monetary values
    "conta_beneficiario_resgatada": None,  # No subpattern needed
    "numero_processo": r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}",  # Extracts the process number
    "autor": None,  # No subpattern needed
    "reu": None,  # No subpattern needed
    "vara": None,
    "nota fiscal": None,
    "nad\sesap": None,
    "conclusao nad\sesap":r"\D{300,2000}natal/rn"

}

# Dictionary indicating whether to stop processing after finding each label
stop_padroes = {
    "bloqueio_conta_salario": False,
    "conta_beneficiario_resgatada": False,
    "numero_processo": True,  # Stop after finding the process number
    "autor": True,
    "reu": True,  # Stop after finding the defendant's name
    "vara": True,
    "nota fiscal": False,
    "nad\sesap": False,
    "conclusao nad\sesap": False

}

# Dictionary for stopping after finding subpatterns (if any), keyed by label
stop_subpadroes = {
    "bloqueio_conta_salario": False,
    "conta_beneficiario_resgatada": False,
    "numero_processo": True,
    "autor": False,
    "reu": True,
    "vara": True,
    "nota fiscal": True,
    "nad\sesap": True,
    "conclusao nad\sesap": False
}
