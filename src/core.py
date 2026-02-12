import re
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
