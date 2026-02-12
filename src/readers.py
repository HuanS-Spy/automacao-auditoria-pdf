import pdfplumber


class LeitorPDF:
    def __init__(self, caminho_arquivo):
        self.caminho = caminho_arquivo

    def _validar_seguranca(self):
        try:
            with open(self.caminho, "rb") as f:
                header = f.read(4)
                if header != b"%PDF":
                    raise ValueError("⛔ ERRO DE SEGURANÇA: Magic Bytes inválidos.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado: {self.caminho}")

    def extrair_texto(self, pagina_inicio=None, pagina_fim=None):
        self._validar_seguranca()
        texto_acumulado = ""
        print(f"📂 Abrindo arquivo: {self.caminho}...")

        with pdfplumber.open(self.caminho) as pdf:
            total_paginas = len(pdf.pages)
            inicio = (pagina_inicio - 1) if pagina_inicio else 0
            fim = pagina_fim if pagina_fim else total_paginas

            if inicio < 0 or fim > total_paginas:
                raise ValueError("Intervalo de páginas inválido.")
            print(f"📖 Lendo das páginas {inicio + 1} até {fim}...")

            for i in range(inicio, fim):
                pagina = pdf.pages[i]

                largura = pagina.width
                altura = pagina.height
                bbox = (0, 50, largura, altura - 50)

                pagina_cortada = pagina.crop(bbox)

                txt = pagina_cortada.extract_text()
                if txt:
                    texto_acumulado += txt + "\n"

        return texto_acumulado
