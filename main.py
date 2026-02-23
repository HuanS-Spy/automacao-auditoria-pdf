# Importações dos Nossos Módulos
import os
from src.readers import LeitorPDF
from src.log_parser import LogParser
from src.reports import GeradorRelatorio, GeradorHTML
from src.utils import validar_caminho_seguro


def main():
    print("🚀 Iniciando Sistema de Análise Legislativa...")

    # CONFIGURAÇÃO
    # Nome da pasta segura onde os PDFs devem estar
    PASTA_BASE = os.path.join(os.path.dirname(__file__), "inputs")

    nome_arquivo = ""  # Certifique-se que o arquivo existe
    pag_inicial = 1
    pag_final = 1

    try:
        print("🛡️ Validando segurança do caminho do arquivo...")

        # Retornar o caminho completo se for seguro, ou dar erro se for ataque
        caminho_seguro = validar_caminho_seguro(nome_arquivo, PASTA_BASE)

        # 1. Leitura
        leitor = LeitorPDF(caminho_seguro)
        texto = leitor.extrair_texto(pag_inicial, pag_final)

        if not texto.strip():
            print("⚠️ Nenhum texto extraído.")
            return

        print("✅ Texto extraído.")

        # 2. Processamento
        parser = LogParser()
        dados_estruturados = parser.processar_texto(texto)
        print(f"📊 {len(dados_estruturados)} eventos/linhas processados.")

        # 3. Geração de Relatório (HTML)
        print("🎨 Gerando relatório HTML estilizado...")
        gerador = GeradorHTML(dados_estruturados)  # <--- Usando a nova classe
        gerador.gerar_html("relatorio_final.html")

        print("🎉 SUCESSO! Abra o arquivo 'relatorio_final.html' no seu navegador.")

        # 3. Geração de Relatório (MD)
        # gerador = GeradorRelatorio(dados_estruturados)
        # gerador.gerar_markdown("relatorio_final.md")
        # print("🎉 Relatório 'relatorio_final.md' gerado com sucesso!")

        # Capture o erro específico de PERMISSÃO
        # Isso acontece se alguém tentar sair da pasta (Path Traversal)

    except PermissionError as e:
        print(f"\n🚨 [INCIDENTE DE SEGURANÇA] TENTATIVA DE ATAQUE DETECTADA!")
        print(f"Detalhe: {e}")
        print("Ação: Execução abortada para proteger o servidor.")

        # [DESAFIO 5]: Capture o erro de ARQUIVO NÃO ENCONTRADO (separado do erro de ataque)
    except FileNotFoundError as e:
        print(f"\n❌ Erro: O arquivo '{nome_arquivo}' não existe na pasta 'inputs'.")
        print(
            "Dica: Verifique se o nome está correto e se o arquivo está na pasta certa."
        )

    except Exception as e:
        print(f"❌ ERRO CRÍTICO NÃO ESPERADO: {e}")


if __name__ == "__main__":
    main()
