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
    def __init__(self, dados):
        # Agora self.dados recebe a lista de eventos (logs) gerada pelo LogParser
        self.dados = dados

    def gerar_html(self, caminho_saida):
        # CSS Básico focado em visualização de SOC (Dark/Light mode simples)
        html = """
        <html>
        <head>
            <meta charset='utf-8'>
            <title>Relatório de Auditoria SOC/DLP</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; padding: 20px; color: #333; }
                h2 { color: #2c3e50; border-bottom: 2px solid #bdc3c7; padding-bottom: 10px; }
                .card { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                .alert { border-left: 6px solid #e74c3c; }
                .success { border-left: 6px solid #2ecc71; background-color: #eafaf1; color: #27ae60; font-weight: bold; text-align: center; padding: 30px;}
                .warning-title { color: #e74c3c; margin-top: 0; }
                .log-line { background-color: #f8f9fa; padding: 10px; border-radius: 4px; font-family: monospace; border: 1px solid #ddd; word-wrap: break-word;}
                ul { margin-top: 10px; }
                li { margin-bottom: 8px; }
            </style>
        </head>
        <body>
            <h2>🛡️ Relatório de Auditoria e Logs (DLP)</h2>
        """

        alertas_gerados = 0

        # Iterando sobre cada linha/evento processado pelo nosso motor
        for evento in self.dados:

            # Busca a lista de ameaças daquela linha específica
            alertas = evento.get("alertas", [])

            # Só renderiza o card no HTML se houver alguma ameaça (SOC silencioso para logs normais)
            if alertas:
                alertas_gerados += 1
                linha = evento.get("linha_origem", "Desconhecida")
                texto_vazado = evento.get("texto", "Texto indisponível")

                html += f"<div class='card alert'>"
                html += f"<h3 class='warning-title'>⚠️ Ameaça Detectada na Linha {linha}</h3>"
                html += f"<p><strong>Trecho Original do Log/Documento:</strong></p>"
                html += f"<div class='log-line'>{texto_vazado}</div>"
                html += "<ul>"

                # Lista todas as violações encontradas naquela mesma linha
                for alerta in alertas:
                    tipo = alerta.get("tipo", "ALERTA")
                    mensagem = alerta.get("mensagem", "Verifique este item.")
                    acao = alerta.get("acao", "")

                    html += f"<li><strong>[{tipo}]</strong> {mensagem}"
                    if acao:
                        html += f"<br><em>Recomendação: {acao}</em>"
                    html += "</li>"

                html += "</ul></div>"

        # Se o motor rodou tudo e não achou nada, exibe o selo de segurança
        if alertas_gerados == 0:
            html += """
            <div class='card success'>
                <h2>✅ Ambiente Seguro</h2>
                <p>Nenhum dado sensível (PII), anomalia ou violação de política foi detectado nos registros analisados.</p>
            </div>
            """

        html += "</body></html>"

        # Salva o arquivo final
        with open(caminho_saida, "w", encoding="utf-8") as f:
            f.write(html)
