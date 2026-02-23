import gradio as gr
import re


# --- 1. LÓGICA DE SEGURANÇA (O "Motor") ---
def motor_de_analise(arquivo_binario):
    if arquivo_binario is None:
        return "⚠️ Nenhum arquivo foi enviado."

    try:
        # Transformando o upload em texto
        texto = arquivo_binario.decode("utf-8", errors="ignore")

        # BUSCA 1: CPFs (DLP)
        cpfs = re.findall(r"\d{3}\.\d{3}\.\d{3}-\d{2}", texto)
        # BUSCA 2: Chaves AWS (Cloud Security)
        chaves_aws = re.findall(r"AKIA[0-9A-Z]{16}", texto)

        # Formatando o Relatório Final
        resultado = "🛡️ RELATÓRIO DE VARREDURA V1.0\n"
        resultado += "=" * 30 + "\n\n"

        resultado += f"📊 CPFs Encontrados: {len(cpfs)}\n"
        if cpfs:
            # Mascarando para segurança (Ex: 123.***.***-45)
            mascarados = [c[:4] + "***.***" + c[-3:] for c in cpfs]
            resultado += f"   Detalhamento: {', '.join(mascarados)}\n\n"

        resultado += f"🔑 Chaves AWS Encontradas: {len(chaves_aws)}\n"
        if chaves_aws:
            resultado += f"   Aviso: Chaves de acesso expostas detectadas!\n"

        if not cpfs and not chaves_aws:
            resultado += "✅ Nenhum dado sensível detectado em texto claro."

        return resultado

    except Exception as e:
        return f"❌ Erro ao processar arquivo: {str(e)}"


# --- 2. INTERFACE GRÁFICA (Gradio) ---
interface = gr.Interface(
    fn=motor_de_analise,
    inputs=gr.File(label="Arraste seu arquivo de LOG ou TXT aqui", type="binary"),
    outputs=gr.Textbox(label="Resultado da Auditoria", lines=15),
    title="🛡️ SOC Scanner & DLP Engine",
    description="Analise logs e documentos em busca de CPFs e Credenciais expostas.",
    theme="soft",
)

# --- 3. LANÇAMENTO ---
if __name__ == "__main__":
    interface.launch()
