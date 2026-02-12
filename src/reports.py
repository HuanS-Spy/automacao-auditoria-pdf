import datetime
import os


class GeradorRelatorio:
    def __init__(self, dados_estruturados):
        self.dados = dados_estruturados
        self.buffer = []

    def _adicionar_linha(self, texto=""):
        self.buffer.append(texto)

    def _renderizar_enrichment(self, analises):
        if not analises:
            return
        self._adicionar_linha("> --- 📘 **NOTA DE CONHECIMENTO** ---")
        for item in analises:
            icone = "⚠️" if item["tipo"] == "ALERTA" else "💡"
            self._adicionar_linha(f"> **{icone} {item['termo']}**")
            if item.get("definicao"):
                self._adicionar_linha(f"> *Definição:* {item['definicao']}")
            if item.get("objetivo"):
                self._adicionar_linha(f"> *Objetivo:* {item['objetivo']}")
            if item.get("categoria"):
                self._adicionar_linha(f"> *Categoria:* {item['categoria']}")
            if item.get("sinonimos"):
                self._adicionar_linha(f"> *Sinônimos:* {item['sinonimos']}")

            if item.get("mensagem"):
                self._adicionar_linha(f"> *AVISO:* {item['mensagem']}")
        self._adicionar_linha(">")
        self._adicionar_linha("> ----------------------------------\n")

    def processar_item(self, item, indentacao=0):
        prefixo = ""
        if item["tipo"] == "ARTIGO":
            self._adicionar_linha(f"## {item['cabecalho']}")
            self._adicionar_linha(f"**Texto:** {item['texto']}\n")
        elif item["tipo"] == "PARAGRAFO":
            prefixo = "   " * indentacao
            self._adicionar_linha(f"{prefixo}**{item['texto']}**")
        elif item["tipo"] == "INCISO":
            prefixo = "   " * indentacao
            self._adicionar_linha(f"{prefixo}- {item['texto']}")
        elif item["tipo"] == "ALINEA":
            prefixo = "       " * indentacao
            self._adicionar_linha(f"{prefixo}{item['texto']}")

        if item.get("analise"):
            self._renderizar_enrichment(item["analise"])

        if "filhos" in item:
            for filho in item["filhos"]:
                self.processar_item(filho, indentacao + 1)
        if item["tipo"] == "ARTIGO":
            self._adicionar_linha("---")

    def gerar_markdown(self, nome_arquivo="relatorio_final.md"):
        data_hoje = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self._adicionar_linha(f"# Relatório de Análise Legislativa")
        self._adicionar_linha(f"*Gerado automaticamente em: {data_hoje}*\n")
        self._adicionar_linha("---")
        for artigo in self.dados:
            self.processar_item(artigo)

        conteudo = "\n".join(self.buffer)
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return conteudo


class GeradorHTML:
    def __init__(self, dados_estruturados):
        self.dados = dados_estruturados
        self.html_content = ""

        self.css = """
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #2c3e50; text-align: center; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
            h2 { color: #2980b9; margin-top: 30px; border-left: 5px solid #2980b9; padding-left: 10px; }
            .meta { text-align: center; color: #7f8c8d; font-size: 0.9em; margin-bottom: 40px; }
            
            .artigo-texto { font-size: 1.1em; margin-bottom: 15px; }
            .paragrafo { font-weight: bold; margin-left: 20px; color: #444; }
            .inciso { margin-left: 40px; }
            .alinea { margin-left: 60px; font-style: italic; }
            
            /* Caixas de Enriquecimento */
            .box-enrichment { background-color: #f9f9f9; border-radius: 5px; padding: 15px; margin: 15px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
            
            .card-conceito { border-left: 4px solid #27ae60; background-color: #eafaf1; padding: 10px; margin-bottom: 5px; }
            .card-alerta { border-left: 4px solid #c0392b; background-color: #fadbd8; padding: 10px; margin-bottom: 5px; }
            
            .titulo-termo { font-weight: bold; display: block; margin-bottom: 4px; }
            .tag { display: inline-block; padding: 2px 6px; font-size: 0.8em; border-radius: 4px; color: white; margin-left: 5px;}
            .tag-alerta { background-color: #c0392b; }
            .tag-conceito { background-color: #27ae60; }
        </style>
        """

    def _renderizar_enrichment(self, analises):

        if not analises:
            return ""

        html = '<div class="box-enrichment">'
        html += "<p><strong>📘 NOTAS DE CONHECIMENTO</strong></p>"

        for item in analises:
            if item["tipo"] == "ALERTA":
                html += f""" 
                    <div class="card-alerta">
                    <span class="titulo-termo">⚠️ {item['termo']} <span class="tag tag-alerta">ALERTA</span></span>
                    {item['mensagem']}
                </div>
                """
            else:
                definicao = item.get("definicao", "Sem definição")
                html += f"""
                <div class="card-conceito">
                    <span class="titulo-termo">💡 {item['termo']} <span class="tag tag-conceito">CONCEITO</span></span>
                    <em>{definicao}</em>
                </div>
                """
        html += "</div>"
        return html

    def processar_item(self, item):
        html = ""

        # Renderiza o Texto Legislativo
        if item["tipo"] == "ARTIGO":
            html += f"<h2>{item['cabecalho']}</h2>"

            # --- LÓGICA DE LIMPEZA VISUAL ---
            texto_exibicao = item["texto"]
            cabecalho = item["cabecalho"]

            # Se o texto começar com "Art. 5º", removemos esse pedaço
            # e também removemos hifens ou espaços extras que sobrarem
            if texto_exibicao.lower().startswith(cabecalho.lower()):
                texto_exibicao = texto_exibicao[len(cabecalho) :].strip(" -–—")

            # Se o texto ficou vazio (ex: o artigo estava só na linha de cima e o texto embaixo),
            # não exibe nada, caso contrário exibe o texto limpo.
            if texto_exibicao:
                html += f"<div class='artigo-texto'>{texto_exibicao}</div>"

        elif item["tipo"] == "PARAGRAFO":
            html += f"<div class='paragrafo'>{item['texto']}</div>"

        elif item["tipo"] == "INCISO":
            html += f"<div class='inciso'>• {item['texto']}</div>"

        elif item["tipo"] == "ALINEA":
            html += f"<div class='alinea'>{item['texto']}</div>"

        # Renderiza Análises (Glossário)
        if item.get("analise"):
            html += self._renderizar_enrichment(item["analise"])

        # Recursividade para Filhos
        if "filhos" in item:
            for filho in item["filhos"]:
                html += self.processar_item(filho)

        if item["tipo"] == "ARTIGO":
            html += "<hr>"  # Linha horizontal visual

        return html

    def gerar_html(self, nome_arquivo="relatorio_final.html"):
        data_hoje = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Relatório Legislativo</title>
            {self.css}
        </head>
        <body>
            <h1>Relatório de Análise Legislativa</h1>
            <div class="meta">Gerado automaticamente em: {data_hoje}</div>
            
            <div class="conteudo">
        """

        for artigo in self.dados:
            full_html += self.processar_item(artigo)

        full_html += """
            </div>
        </body>
        </html>
        """

        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(full_html)

        return full_html
