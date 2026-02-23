# 🛡️ SOC Scanner & DLP Engine (Python Security Tools)

> **Status do Projeto:** 🚀 Status: Versão 1.0 Concluída (Arquitetura Modular e Interface Web)
> **Foco de Estudo:** AppSec, Prevenção de Perda de Dados (DLP), Threat Intelligence e Clean Code.

---

## 🎯 1. O Desafio (Contexto de Negócio)

**O Problema:** Em operações de *Blue Team* e auditoria de conformidade, a caça manual por vazamento de dados sensíveis (LGPD/PCI-DSS), *Hardcoded Secrets* (credenciais no código) e Indicadores de Comprometimento (IoCs) em logs e documentos é ineficiente. A exposição de chaves de nuvem ou dados de clientes não perdoa atrasos na triagem.

**A Solução:** Evoluí um script de leitura básica para uma **Engine de DLP e SOC** operando 100% local (offline) com interface gráfica. A ferramenta ingere arquivos `.txt` e `.pdf`, varre o conteúdo através de expressões regulares complexas e algoritmos de validação matemática, mascarando os dados sensíveis na tela e gerando um relatório HTML categorizado por nível de risco.

---

## 🛠️ 2. Competências Técnicas (Hard Skills)

### 💻 Stack Tecnológico e Arquitetura
* ![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python) **Core:** Arquitetura modular (*Separation of Concerns*) separando Leitores, Detectores, Parsers e Relatórios.
* **Interface Web:** Uso do framework `streamlit` para criar um *dashboard* interativo sem a necessidade de codificar HTML/CSS nativo.
* **Processamento e Regex:** Uso avançado do módulo `re` para caçar chaves **AWS** (`AKIA...`), Hashes Hexadecimais e IPs.
* **Validação Matemática:** Implementação do **Algoritmo de Luhn** para evitar falsos positivos na detecção de Cartões de Crédito (PCI-DSS).

### 🛡️ Engenharia de Segurança (AppSec Highlights)
*Diferencial: O código foi construído com mentalidade "Security by Design".*

* **Data Masking (Sanitização Visual):** Implementação de uma camada de filtro (`replace` e *slicing*) que substitui partes de CPFs, senhas e chaves AWS por asteriscos antes da renderização na tela, evitando que o próprio relatório gere um incidente de vazamento.
* **Memory & Storage Management:** Uso do módulo nativo `tempfile` para alocar os uploads da interface web temporariamente no sistema operacional, garantindo a exclusão automática dos arquivos após a varredura.
* **Prevenção de Falsos Positivos:** Validação lógica de dígitos verificadores (CPF) em conjunto com a validação de formato (*Regex*).

---

## 🧠 3. Diário de Bordo: Análise e Troubleshooting (Soft Skills)

O desenvolvimento exigiu diagnóstico e resolução de problemas reais de infraestrutura de desenvolvimento:

| Desafio Encontrado (O Erro) | Minha Análise (Causa Raiz) | Solução Implementada |
| :--- | :--- | :--- |
| **Erro "File does not exist" no Streamlit:** O terminal não encontrava o arquivo `app.py` na execução. | O terminal (CLI) estava operando em um caminho relativo diferente do diretório raiz do projeto. | Forcei a execução utilizando o **caminho absoluto** do arquivo ou a flag de módulo do Python (`python -m streamlit run`). |
| **Erro "components.v1 não é um módulo":** Falha na renderização do HTML dentro da interface web. | Submódulos profundos de algumas bibliotecas não são carregados automaticamente apenas com `import streamlit as st`. | Refatorei o código para fazer a importação **explícita** do submódulo no cabeçalho (`import streamlit.components.v1 as components`). |
| **Falha de Autenticação no Git Push:** O GitHub rejeitava o envio do código relatando "Password authentication is not supported". | A plataforma aboliu o uso de senhas convencionais no terminal em prol de tokens de segurança. | Gerei um **Personal Access Token (PAT)** com escopo de repositório e embuti a credencial diretamente na URL do `remote origin` via comando `set-url`. |

---

## ⚙️ 4. Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/automacao-auditoria-pdf.git](https://github.com/seu-usuario/automacao-auditoria-pdf.git)
    ```
2.  **Instale as dependências:**
    ```bash
    pip install streamlit pypdf
    ```
3.  **Inicie o Servidor Web Local:**
    Navegue até a raiz do projeto e execute:
    ```bash
    streamlit run app.py
    ```
4.  **Uso:** A interface abrirá automaticamente no navegador (`localhost:8501`). Faça o upload do arquivo e analise os alertas.

---

## 🚀 5. Próximos Passos (Roadmap V1.1)

* [ ] **Dashboard de Estatísticas:** Implementar gráficos visuais no Streamlit mostrando o volume de ameaças detectadas por categoria.
* [ ] **Sistema de Quarentena:** Lógica de *backend* para mover automaticamente arquivos infectados ou com dados críticos para um diretório isolado do sistema.
* [ ] **Containerização:** Criar um `Dockerfile` para rodar a automação em ambiente isolado.