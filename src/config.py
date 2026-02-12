import json
import os

# Caminho absoluto para a pasta 'data' (Boas práticas para rodar de qualquer lugar)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def carregar_glossario():
    caminho = os.path.join(DATA_DIR, "glossario.json")
    if not os.path.exists(caminho):
        print(f"⚠️ AVISO: '{caminho}' não encontrado.")
        return {}
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler JSON: {e}")
        return {}


# Carrega os dados na inicialização
GLOSSARIO = carregar_glossario()

# Lista de Gatilhos (Hardcoded para agilidade, conforme combinamos)
GATILHOS_ALERTA = [
    "vedado",
    "proibido",
    "nulo",
    "anulado",
    "revogado",
    "inconstitucional",
    "crime",
    "pena",
    "reclusão",
    "detenção",
    "cassação",
    "improbidade",
    "suspenso",
]


def obter_cor_alerta(termo):
    vermelhos = ["crime", "reclusão", "vedado", "proibido", "inconstitucional"]
    return "VERMELHO" if termo in vermelhos else "AMARELO"
