"""import re
from src.utils import normalizar_texto
from src.config import GLOSSARIO, GATILHOS_ALERTA, obter_cor_alerta


def analisar_frase_juridica(frase_original):
    frase_limpa = normalizar_texto(frase_original)
    anotacoes = []

    # 1. Busca no Glossário
    for termo_chave, dados in GLOSSARIO.items():
        termo_normalizado = normalizar_texto(termo_chave)
        padrao = r"\b" + re.escape(termo_normalizado) + r"\b"

        if re.search(padrao, frase_limpa):
            anotacoes.append(
                {
                    "tipo": "CONCEITO",
                    "termo": termo_chave.upper(),
                    "definicao": dados["definicao"],
                    "objetivo": dados.get("objetivo", "N/A"),
                    "categoria": dados.get("categoria", "geral"),
                    "sinonimos": dados.get("sinonimos", "N/A"),
                }
            )

    # 2. Busca nos Gatilhos
    for gatilho in GATILHOS_ALERTA:
        gatilho_normalizado = normalizar_texto(gatilho)
        padrao = r"\b" + re.escape(gatilho_normalizado) + r"\b"

        if re.search(padrao, frase_limpa):
            cor = obter_cor_alerta(gatilho_normalizado)
            anotacoes.append(
                {
                    "tipo": "ALERTA",
                    "termo": gatilho.upper(),
                    "mensagem": f"⚠️ Atenção! Termo restritivo ou penal ({cor}). Verifique o contexto.",
                    "prioridade": "ALTA" if cor == "VERMELHO" else "MEDIA",
                }
            )

    return anotacoes
"""

import re
from src.detectors import (
    varrer_texto_por_cpfs,
    varrer_texto_por_cartoes,
    varrer_texto_por_credenciais,
    varrer_texto_por_iocs,
)
from src.utils import normalizar_texto
from src.config import GLOSSARIO, GATILHOS_ALERTA, obter_cor_alerta


def analisar_frase_juridica(frase_original):
    frase_limpa = normalizar_texto(frase_original)
    anotacoes = []

    cpfs_vazados = varrer_texto_por_cpfs(frase_original)

    for cpf in cpfs_vazados:
        anotacoes.append(
            {
                "tipo": "RISCO_DETECTADO",
                "termo": f"CPF EXPOSTO: {cpf}",
                "nivel_risco": "CRÍTICO",
                "categoria": "LGPD / Privacidade",
                "acao": "Anonimizar (mascarar) o dado imediatamente para evitar sanções.",
                "mensagem": "⚠️ Violação LGPD (Art. 7º): Exposição de Dado Pessoal identificável sem mascaramento.",
            }
        )

    # === CAÇADOR DE CARTÕES DE CRÉDITO (PCI-DSS) ===
    cartoes_vazados = varrer_texto_por_cartoes(frase_original)

    for cartao in cartoes_vazados:
        # Mascaramento de dados (DLP): Esconde tudo, mostra só os últimos 4 dígitos
        cartao_limpo = re.sub(r"\D", "", cartao)
        cartao_mascarado = f"**** **** **** {cartao_limpo[-4:]}"

        anotacoes.append(
            {
                "tipo": "RISCO_DETECTADO",
                "termo": f"CARTÃO DE CRÉDITO EXPOSTO: {cartao_mascarado}",
                "nivel_risco": "CRÍTICO",
                "categoria": "PCI-DSS / Financeiro",
                "acao": "Revogar token imediatamente e mascarar dado (Data Masking).",
                "mensagem": "⚠️ Violação PCI-DSS: Exposição de PAN (Primary Account Number) em texto claro.",
            }
        )

    # === CAÇADOR DE CREDENCIAIS VAZADAS (CLOUD/DEVOPS) ===
    credenciais = varrer_texto_por_credenciais(frase_original)
    for cred in credenciais:
        anotacoes.append(
            {
                "tipo": "RISCO_DETECTADO",
                "termo": f"CREDÊNCIAL/SENHA EXPOSTA: {cred}",
                "nivel_risco": "CRÍTICO",
                "categoria": "Hardcoded Secrets / IAM",
                "acao": "Rotacionar a chave/senha imediatamente. Risco de invasão lateral.",
                "mensagem": "⚠️ Vazamento Crítico: Credenciais de acesso encontradas em texto claro.",
            }
        )

    # === CAÇADOR DE INDICADORES DE COMPROMETIMENTO (IOCs) ===
    iocs = varrer_texto_por_iocs(frase_original)
    for ioc in iocs:
        anotacoes.append(
            {
                "tipo": "ANOMALIA_DETECTADA",
                "termo": f"INDICADOR SUSPEITO (IP/HASH): {ioc}",
                "nivel_risco": "ALTO",
                "categoria": "SOC / Threat Intel",
                "acao": "Verificar IP em bases de Threat Intelligence e bloquear no Firewall se malicioso.",
                "mensagem": "🚨 Rastro suspeito: IP ou Hash de arquivo encontrado no registro.",
            }
        )

    # 1. Busca na Nova Matriz de Risco (Antigo Glossário)
    for termo_chave, dados in GLOSSARIO.items():
        # Busca por múltiplos padrões (sinônimos de risco)
        padroes = dados.get("padrao_busca", [termo_chave])

        encontrou = False
        for padrao in padroes:
            padrao_norm = normalizar_texto(padrao)
            # Regex simples (word boundary) para achar a palavra inteira
            if re.search(r"\b" + re.escape(padrao_norm) + r"\b", frase_limpa):
                encontrou = True
                break

        if encontrou:
            # Cria o card de RISCO (AppSec/Auditoria)
            anotacoes.append(
                {
                    "tipo": "RISCO_DETECTADO",
                    "termo": termo_chave.upper(),
                    "nivel_risco": dados.get("risco", "DESCONHECIDO"),
                    "categoria": dados.get("categoria", "Geral"),
                    "acao": dados.get("acao_sugerida", "Analisar contexto."),
                    "mensagem": f"⚠️ Risco {dados.get('risco')}: {dados.get('acao_sugerida')}",
                }
            )

    # 2. Busca nos Gatilhos (Mantém compatibilidade com alertas simples)
    for gatilho in GATILHOS_ALERTA:
        gatilho_normalizado = normalizar_texto(gatilho)
        if re.search(r"\b" + re.escape(gatilho_normalizado) + r"\b", frase_limpa):
            cor = obter_cor_alerta(gatilho_normalizado)
            # Só adiciona se não for duplicado com o glossário
            anotacoes.append(
                {
                    "tipo": "ALERTA_KEYWORD",
                    "termo": gatilho.upper(),
                    "mensagem": f"🔎 Termo Sensível ({cor}): Verifique o contexto.",
                    "prioridade": "ALTA" if cor == "VERMELHO" else "MEDIA",
                }
            )

    return anotacoes
