import os
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

    # --- NOVO BLOCO DE SEGURANÇA (APPSEC) ---


def validar_caminho_seguro(nome_arquivo, diretorio_base):
    """
    🛡️ PREVENÇÃO DE PATH TRAVERSAL (CWE-22)
    """
    # 1. Transforma a pasta base em caminho absoluto (Ex: /home/user/projeto/inputs)
    base_abs = os.path.abspath(diretorio_base)

    # 2. Junta a pasta com o nome do arquivo (AQUI ESTÁ A MÁGICA)
    # Ex: /home/user/projeto/inputs + CF_ATUALIZADA.pdf
    caminho_final = os.path.abspath(os.path.join(base_abs, nome_arquivo))

    # 3. VERIFICAÇÃO DE SEGURANÇA (O Guardião)
    # Verifica se o caminho final começa exatamente com a pasta base
    # Se o usuário tentou "../", o commonpath vai dar diferente.
    try:
        caminho_comum = os.path.commonpath([base_abs, caminho_final])
    except ValueError:
        caminho_comum = ""

    if caminho_comum != base_abs:
        raise PermissionError(
            f"⛔ ALERTA DE SEGURANÇA: Tentativa de Path Traversal! {nome_arquivo}"
        )

    # 4. Verifica se o arquivo existe de verdade
    if not os.path.exists(caminho_final):
        # Dica de Debug: Se cair aqui, é porque o arquivo não está na pasta
        raise FileNotFoundError(
            f"Arquivo não encontrado no caminho seguro: {caminho_final}"
        )

    # 5. O RETORNO CRÍTICO (Aqui estava o erro provável)
    # Temos que retornar o CAMINHO FINAL (arquivo), nunca a base_abs (pasta)
    return caminho_final
