# Importações dos Nossos Módulos
from src.readers import LeitorPDF
from src.parsers import ParserLegislativo
from src.reports import GeradorRelatorio, GeradorHTML


def main():
    print("🚀 Iniciando Sistema de Análise Legislativa...")

    # CONFIGURAÇÃO
    nome_arquivo = "CF ATUALIZADA.pdf"  # Certifique-se que o arquivo existe
    pag_inicial = 14
    pag_final = 15

    try:
        # 1. Leitura
        leitor = LeitorPDF(nome_arquivo)
        texto = leitor.extrair_texto(pag_inicial, pag_final)

        if not texto.strip():
            print("⚠️ Nenhum texto extraído.")
            return

        print("✅ Texto extraído.")

        # 2. Processamento
        parser = ParserLegislativo()
        dados_estruturados = parser.processar_texto_bruto(texto)
        print(f"📊 {len(dados_estruturados)} artigos processados.")

        # 3. Geração de Relatório (HTML)
        print("🎨 Gerando relatório HTML estilizado...")
        gerador = GeradorHTML(dados_estruturados)  # <--- Usando a nova classe
        gerador.gerar_html("relatorio_final.html")

        print("🎉 SUCESSO! Abra o arquivo 'relatorio_final.html' no seu navegador.")

        # 3. Geração de Relatório (MD)
        # gerador = GeradorRelatorio(dados_estruturados)
        # gerador.gerar_markdown("relatorio_final.md")
        # print("🎉 Relatório 'relatorio_final.md' gerado com sucesso!")

    except Exception as e:
        print(f"❌ ERRO CRÍTICO: {e}")


if __name__ == "__main__":
    main()
