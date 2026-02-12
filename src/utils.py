import re


def normalizar_texto(texto):
    """
    Remove caracteres especiais e padroniza para minúsculo.
    Usado para comparações precisas.
    """

    if not texto:
        return ""
    texto = texto.lower()

    # Mantém apenas letras, números e espaços
    texto = re.sub(r"[^\w\s]", "", texto)
    return texto


def tratar_quebras_de_linha(texto_bruto):
    """
    Corrige hifenização e quebras de linha indesejadas do PDF.
    Ex: 'Cons-\ntituição' vira 'Constituição'.
    """

    if not texto_bruto:
        return ""
    texto_tratado = re.sub(r"(\w+)-\n\s*(\w+)", r"\1\2", texto_bruto)

    return texto_tratado
