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
from src.utils import normalizar_texto
from src.config import GLOSSARIO, GATILHOS_ALERTA, obter_cor_alerta


def analisar_frase_juridica(frase_original):
    frase_limpa = normalizar_texto(frase_original)
    anotacoes = []

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
