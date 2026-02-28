import streamlit.components.v1 as components
import streamlit as st
import os
import tempfile
from src.readers import LeitorPDF
from src.log_parser import LogParser
from src.reports import GeradorHTML

# Configuração da página para ocupar a tela toda
st.set_page_config(page_title="SOC Scanner", layout="wide")

st.title("🛡️ Scanner de Auditoria e Logs")
st.write(
    "Faça o upload do seu arquivo de log (.txt) ou documento (.pdf) para buscar dados sensíveis vazados."
)

# Componente visual de Upload (O Streamlit faz a mágica do CSS sozinho)
arquivo_upado = st.file_uploader("Selecione o arquivo", type=["txt", "pdf"])

# Botão de ação
if st.button("🔎 Iniciar Varredura"):

    if arquivo_upado is not None:
        with st.spinner("Analisando dados..."):
            texto_bruto = ""

            # O arquivo upado fica na memória. Precisamos salvar temporariamente
            # para o nosso LeitorPDF conseguir abrir o caminho físico.
            extensao = arquivo_upado.name.split(".")[-1]
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=f".{extensao}"
            ) as tmp:
                tmp.write(arquivo_upado.getvalue())
                tmp_path = tmp.name

            # Roteamento: É PDF ou é TXT?
            if extensao == "pdf":
                leitor = LeitorPDF(tmp_path)
                texto_bruto = leitor.extrair_texto(
                    1, 1
                )  # Lendo a pág 1 para teste rápido
            else:
                with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                    texto_bruto = f.read()

            # 1. Processamento pelo nosso Motor
            parser = LogParser()
            dados = parser.processar_texto(texto_bruto)

            # 2. Geração de Relatório
            gerador = GeradorHTML(dados)
            caminho_relatorio = "relatorio_final.html"
            gerador.gerar_html(caminho_relatorio)

            st.success("✅ Varredura Concluída com Sucesso!")

            # 3. Exibir o Relatório HTML diretamente dentro da interface gráfica!
            st.markdown("### 📊 Resultado da Auditoria")
            with open(caminho_relatorio, "r", encoding="utf-8") as f:
                html_content = f.read()

            # Renderiza o HTML seguro dentro do Streamlit
            components.html(html_content, height=600, scrolling=True)

            # Limpa o arquivo temporário para não lotar o servidor
            os.remove(tmp_path)
    else:
        st.warning("⚠️ Por favor, anexe um arquivo antes de iniciar.")
