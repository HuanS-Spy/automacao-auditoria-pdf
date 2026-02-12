import re
from src.core import analisar_frase_juridica
from src.utils import tratar_quebras_de_linha


class ParserLegislativo:
    def __init__(self):
        self.estrutura = []
        self.artigo_atual = None
        self.ultimo_filho_processado = None

    def processar_texto_bruto(self, texto_bruto):

        texto_limpo = tratar_quebras_de_linha(texto_bruto)

        linhas = texto_limpo.split("\n")

        # Regex compilados
        # rgx_artigo = re.compile(r"^\s*(Art\.\s*\d+.*?)(?:\s[-–—]\s|$)", re.IGNORECASE)
        rgx_artigo = re.compile(r"^\s*(Art\.\s*\d+[º°]?)", re.IGNORECASE)
        rgx_paragrafo = re.compile(r"^\s*(§\s*\d+|Parágrafo único)", re.IGNORECASE)
        rgx_inciso = re.compile(r"^\s*([IVXLCDM]+\s*[-–—])", re.IGNORECASE)
        rgx_alinea = re.compile(r"^\s*([a-z]\))", re.IGNORECASE)

        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue

            match_art = rgx_artigo.match(linha)

            # 1. Identifica Artigo
            if match_art:
                if self.artigo_atual:
                    self.estrutura.append(self.artigo_atual)

                self.artigo_atual = {
                    "tipo": "ARTIGO",
                    "cabecalho": match_art.group(1),
                    "texto": linha,
                    "filhos": [],
                    "analise": analisar_frase_juridica(linha),  # Chama o core aqui
                }

                self.ultimo_filho_processado = None
                continue

            # 2. Identifica Filhos
            if self.artigo_atual:

                match_par = rgx_paragrafo.match(linha)
                match_inc = rgx_inciso.match(linha)
                match_ali = rgx_alinea.match(linha)

                tipo_filho = None
                if match_par:
                    tipo_filho = "PARAGRAFO"
                elif match_inc:
                    tipo_filho = "INCISO"
                elif match_ali:
                    tipo_filho = "ALINEA"

                if tipo_filho:
                    sub_item = {
                        "tipo": tipo_filho,
                        "texto": linha,
                        "analise": analisar_frase_juridica(linha),
                    }
                    self.artigo_atual["filhos"].append(sub_item)
                    self.ultimo_filho_processado = sub_item

                else:
                    if self.ultimo_filho_processado:
                        self.ultimo_filho_processado["texto"] += " " + linha

                    else:
                        self.artigo_atual["texto"] += " " + linha

        if self.artigo_atual:
            self.estrutura.append(self.artigo_atual)

        return self.estrutura
