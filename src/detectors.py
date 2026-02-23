import re


def validar_cpf_matematica(cpf):
    """
    🛡️ Validador de CPF: Evita Falsos Positivos de DLP garantindo
    que o número encontrado passa no cálculo da Receita Federal.
    """
    # Remove tudo que não for número
    cpf_limpo = re.sub(r"\D", "", cpf)

    if len(cpf_limpo) != 11:
        return False

    # Bloqueia sequências repetidas (Testes) para evitar falsos positivos
    if cpf_limpo in [str(i) * 11 for i in range(10)]:
        return False

    # Lógica Matemática dos Dígitos Verificadores
    def calcular_digito(cpf_parcial, peso_inicial):
        soma = sum(
            int(digito) * peso
            for digito, peso in zip(cpf_parcial, range(peso_inicial, 1, -1))
        )
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    digito1 = calcular_digito(cpf_limpo[:9], 10)
    digito2 = calcular_digito(cpf_limpo[:10], 11)

    return cpf_limpo.endswith(f"{digito1}{digito2}")


def varrer_texto_por_cpfs(texto):
    """
    🔎 Caçador de Padrões (DLP Engine)
    Retorna uma lista de CPFs reais encontrados no texto.
    """
    cpfs_encontrados = []

    # Regex que caça o formato do CPF (com ou sem pontuação)
    padrao_cpf = r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"

    possiveis_cpfs = re.findall(padrao_cpf, texto)

    # Filtro de Falsos Positivos: A matemática bate?
    for candidato in possiveis_cpfs:
        if validar_cpf_matematica(candidato):
            cpfs_encontrados.append(candidato)

    return cpfs_encontrados


def validar_cartao_luhn(cartao):
    """
    🛡️ Algoritmo de Luhn: Valida cartões de crédito para evitar falsos positivos.
    Norma: PCI-DSS.
    """
    # Remove tudo que não for número (espaços, traços, etc)
    cartao_limpo = re.sub(r"\D", "", cartao)

    # Cartões variam de 13 a 19 dígitos
    if len(cartao_limpo) < 13 or len(cartao_limpo) > 19:
        return False

    # Lógica Matemática do Algoritmo de Luhn (Módulo 10)
    soma = 0
    alternar = False

    # Lendo o cartão de trás para frente
    for i in range(len(cartao_limpo) - 1, -1, -1):
        digito = int(cartao_limpo[i])

        if alternar:
            digito *= 2
            if digito > 9:
                digito -= 9

        soma += digito
        alternar = not alternar

    # Retorna True se a soma for divisível por 10
    return soma % 10 == 0


def varrer_texto_por_cartoes(texto):
    """
    🔎 DLP Engine: Caçador de Cartões de Crédito (PCI-DSS)
    """
    cartoes_encontrados = []

    # Regex para achar 4 blocos de 4 números separados por espaço ou traço
    padrao_cartao = r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"

    possiveis_cartoes = re.findall(padrao_cartao, texto)

    for candidato in possiveis_cartoes:
        # Passa o candidato pelo crivo matemático de Luhn
        if validar_cartao_luhn(candidato):
            cartoes_encontrados.append(candidato)

    return cartoes_encontrados


def sanitizar_log_str(texto):
    """
    Substitui os dados sensíveis encontrados na string original
    pelas suas versões mascaradas, protegendo a exibição do log.
    """
    texto_seguro = texto

    # 1. Mascara Cartões de Crédito (PCI-DSS)
    cartoes = varrer_texto_por_cartoes(texto_seguro)
    for cartao in cartoes:
        final_cartao = cartao[-4:]
        texto_seguro = texto_seguro.replace(cartao, f"****.****.****.{final_cartao}")

    # 2. Mascara CPFs (LGPD)
    cpfs = varrer_texto_por_cpfs(texto_seguro)
    for cpf in cpfs:
        texto_seguro = texto_seguro.replace(cpf, "***.***.***-**")

    # 3. Mascara Credenciais (CLOUD/DEVOPS)
    credenciais = varrer_texto_por_credenciais(texto_seguro)
    for cred in credenciais:
        # Mostra o prefixo AKIA e oculta o resto da chave AWS
        if cred.startswith("AKIA"):
            texto_seguro = texto_seguro.replace(cred, f"{cred[:4]}****************")
        # Mascara senhas genéricas totalmente
        else:
            texto_seguro = texto_seguro.replace(cred, "********")

    return texto_seguro


def varrer_texto_por_credenciais(texto):
    """
    ☁️ DLP Engine: Caçador de Credenciais e Segredos (AWS, Senhas, Tokens)
    """
    credenciais_encontradas = []

    # Access Key da AWS (IAM)
    padrao_aws = r"\bAKIA[A-Z0-9]{16}\b"

    # Senhas em formatos como "password=1234" ou "senha: root"
    padrao_senha = r"\b(?:password|senha|pwd|secret)\s*[:=]\s*([a-zA-Z0-9@#*&]+)\b"

    aws_keys = re.findall(padrao_aws, texto)
    credenciais_encontradas.extend(aws_keys)

    # Flag IGNORECASE para pegar "Senha", "SENHA", etc.
    senhas = re.findall(padrao_senha, texto, flags=re.IGNORECASE)
    credenciais_encontradas.extend(senhas)

    return credenciais_encontradas


def varrer_texto_por_iocs(texto):
    """
    🕸️ SOC Engine: Caçador de Indicadores de Comprometimento (IPs e Hashes)
    """
    iocs_encontrados = []

    # IPv4 (4 blocos de 1 a 3 dígitos). O {3} repete o padrão do ponto 3 vezes.
    padrao_ipv4 = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

    # Hashes MD5 ou SHA256 (Hexadecimal)
    padrao_hash = r"\b[0-9A-F]{32,64}\b"

    ips = re.findall(padrao_ipv4, texto)
    iocs_encontrados.extend(ips)

    hashes = re.findall(padrao_hash, texto, flags=re.IGNORECASE)
    iocs_encontrados.extend(hashes)

    return iocs_encontrados
