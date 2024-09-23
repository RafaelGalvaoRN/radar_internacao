# Dictionary of main patterns to search for in the text, keyed by label
padroes = {
    "💰Houve Bloqueio da Conta Salário?": r"RECIBO DE PROTOCOLAMENTO DE BLOQUEIO DE VALORES.*Bloquear Conta-Salário|DETALHAMENTO\sDA\sORDEM\sJUDICIAL\sDE\sDESDOBRAMENTO\sDE\sBLOQUEIO\sDE\sVALORES",
    "conta_beneficiario_resgatada": r"conta.*beneficiário.*resgatada",
    "⚖️Número do Processo": r"Processo:\s*\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}",
    "👨‍💼Autor": r"AUTOR:\s*([A-ZÁÉÍÓÚÇãáàéíóúç\s]+)\.?",  # Captures the author's name
    "👨‍💼Réu": r"REU:\s*([A-ZÁÉÍÓÚÇãáàéíóúç\s,]+)decisão?",
    "🏛️Vara": r"poder judiciário do estado do rio grande do norte(.*?)processo",
    "🧾Nota Fiscal": r"Nota Fiscal de Serviços Eletrônica - NFS-e",
    "📄NAD/SESAP": r"relatório.*Núcleo de Atenção Domiciliar da Secretaria de Estado da Saúde Pública",
    "📋Conclusão do NAD/SESAP": r"relatório.*Núcleo de Atenção Domiciliar da Secretaria de Estado da Saúde Pública.*natal/rn",
    "💳Alvará Eletrônico": r"Conta\/Pcl Resgatada.*Beneficiario.*Titular Conta.*Cta Corrente.*Crédito em C\/C BB Finalidade",
    "⚕️NT NAT/JUS": r"nota técnica.+dados do paciente.+urgente.+paciente.+natjus",
    "👨‍💼Advogados": r"tjrn.*Processo\sJudicial.*Partes\sProcurador.*\(autor\).*\(reu\)",
    "⚖️Decisão Interlocutória": r"poder\sjudici.rio\sdo\sestado\sdo\srio\sgrande\sdo\snorte.+processo.+decis.o(?!.*MANDADO\sDE\sINTIMAÇÃO\s-\sPRAZO)"
}

# Dictionary of subpatterns to further refine the search, keyed by label
subpadroes = {
    "💰Houve Bloqueio da Conta Salário?": r"R\$\s*\d{1,3}(?:\.\d{3})*,\d{2}",  # Captures monetary values
    "conta_beneficiario_resgatada": None,  # No subpattern needed
    "⚖️Número do Processo": r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}",  # Extracts the process number
    "👨‍💼Autor": None,  # No subpattern needed
    "👨‍💼Réu": None,  # No subpattern needed
    "🏛️Vara": None,
    "🧾Nota Fiscal": None,
    "📄NAD/SESAP": None,
    "📋Conclusão do NAD/SESAP": r"\D{300,2000}natal/rn",
    "💳Alvará Eletrônico": None,
    "⚕️NT NAT/JUS": None,
    "👨‍💼Advogados": None,
    "⚖️Decisão Interlocutória": None,

}

# Dictionary indicating whether to stop processing after finding each label
stop_padroes = {
    "💰Houve Bloqueio da Conta Salário?": False,
    "conta_beneficiario_resgatada": False,
    "⚖️Número do Processo": True,  # Stop after finding the process number
    "👨‍💼Autor": True,
    "👨‍💼Réu": True,  # Stop after finding the defendant's name
    "🏛️Vara": True,
    "🧾Nota Fiscal": False,
    "📄NAD/SESAP": False,
    "📋Conclusão do NAD/SESAP": False,
    "💳Alvará Eletrônico": False,
    "⚕️NT NAT/JUS": False,
    "👨‍💼Advogados": False,
    "⚖️Decisão Interlocutória": False,
}

# Dictionary for stopping after finding subpatterns (if any), keyed by label
stop_subpadroes = {
    "💰Houve Bloqueio da Conta Salário?": False,
    "conta_beneficiario_resgatada": False,
    "⚖️Número do Processo": True,
    "👨‍💼Autor": False,
    "👨‍💼Réu": True,
    "🏛️Vara": True,
    "🧾Nota Fiscal": True,
    "📄NAD/SESAP": True,
    "📋Conclusão do NAD/SESAP": False,
    "💳Alvará Eletrônico": True,
    "⚕️NT NAT/JUS": False,
    "👨‍💼Advogados": False,
    "⚖️Decisão Interlocutória": False,

}
