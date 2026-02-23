from src.detectors import sanitizar_log_str
from src.core import analisar_frase_juridica
from src.utils import tratar_quebras_de_linha


class LogParser:
    def __init__(self):
        self.eventos = []

    def processar_texto(self, texto_bruto):
        """
        Lê qualquer bloco de texto (PDF ou Log) e processa linha por linha.
        """
        texto_limpo = tratar_quebras_de_linha(texto_bruto)

        # Divide o texto gigantesco em uma lista de linhas individuais
        linhas = texto_limpo.split("\n")

        # Itera guardando o número da linha para rastreabilidade
        for numero_linha, linha in enumerate(linhas, start=1):

            linha = linha.strip()

            # Pula linhas vazias para economizar processamento
            if not linha:
                continue

            # Envia a linha isolada para o motor DLP
            alertas_encontrados = analisar_frase_juridica(linha)

            # 🛡️ SANITIZAÇÃO DO LOG: Limpa o texto antes de salvar no relatório
            linha_segura = sanitizar_log_str(linha)

            # Estrutura o evento padronizado
            evento = {
                "tipo": "REGISTRO_LOG",
                "linha_origem": numero_linha,
                "texto": linha_segura,
                "alertas": alertas_encontrados,
            }

            self.eventos.append(evento)

        return self.eventos
