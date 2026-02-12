# 📄 Automação de Análise de Contratos e PDFs (Python Security Tools)

> **Status do Projeto:** 🚧 Status: Versão Inicial (Aguardando Refatoração de Segurança))
> **Foco de Estudo:** Automação de Processos (RPA), Tratamento de Dados e Codificação Segura (AppSec).

---

## 🎯 1. O Desafio (Contexto de Negócio)

**O Problema:** Em processos de auditoria e conformidade, a leitura manual de grandes volumes de documentos (PDFs e arquivos de texto) é uma tarefa repetitiva, lenta e propensa a falhas humanas (fadiga). A busca por termos específicos (como cláusulas de risco ou dados sensíveis) consome horas preciosas que deveriam ser usadas na análise estratégica.

**A Solução:** Desenvolvi este script em Python para atuar como um "Assistente de Pré-Auditoria". Ele automatiza a ingestão de documentos, extrai entidades nomeadas, destaca palavras-chave pré-configuradas e gera um relatório final com os pontos de atenção, reduzindo o tempo de triagem em aproximadamente 80%.

---

## 🛠️ 2. Competências Técnicas (Hard Skills)

### 💻 Stack Tecnológico
* ![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python) **Core:** Lógica de script estruturada e modular.
* **Manipulação de Arquivos:** Bibliotecas `pypdf` (extração de texto) e gestão de I/O com `os`/`shutil`.
* **Processamento de Texto:** Uso avançado de `re` (Regular Expressions) para *pattern matching* de alta precisão.
* **Saída de Dados:** Geração automatizada de relatórios em PDF usando `reportlab` ou bibliotecas similares.

### 🛡️ Engenharia de Segurança (AppSec Highlights)
*Diferencial: O código foi construído com mentalidade "Security by Design".*

* **Sanitização de Entradas (Input Validation):** Implementei filtros rigorosos nos nomes de arquivos de entrada para prevenir vulnerabilidades de **Path Traversal** (impedindo que o script acesse diretórios indevidos do sistema operacional).
* **Tratamento de Exceções (Fail-Safe):** Utilizei blocos `try/except` específicos para garantir que erros de leitura (arquivos corrompidos) não interrompam o lote inteiro e, principalmente, não exponham *stack traces* sensíveis no terminal.
* **Gerenciamento de Recursos:** O script utiliza gerenciadores de contexto (`with open...`) para garantir que os descritores de arquivos sejam fechados imediatamente após o uso, evitando vazamento de memória ou bloqueio de arquivos no sistema.

---

## 🧠 3. Diário de Bordo: Análise e Troubleshooting (Soft Skills)

O desenvolvimento deste projeto exigiu mais do que apenas escrever código; exigiu diagnóstico e resolução de problemas reais de ambiente. Abaixo, documento as principais barreiras e minhas soluções:

| Desafio Encontrado (O Erro) | Minha Análise (Causa Raiz) | Solução Implementada |
| :--- | :--- | :--- |
| **Incompatibilidade de Encoding:** O script falhava silenciosamente ou gerava caracteres estranhos () ao ler arquivos gerados em sistemas Windows antigos. | Identifiquei através de testes que o Python 3 força UTF-8 por padrão, mas os arquivos legados estavam em `cp1252` ou `latin-1`. | Implementei uma função de leitura resiliente que tenta abrir em UTF-8 e, se falhar, faz o *fallback* automático para `latin-1`, garantindo a integridade dos dados. |
| **Falsos Positivos na Busca:** A Regex inicial para capturar "CPF" estava trazendo números de telefone e protocolos aleatórios. | A expressão `\d{11}` era muito genérica ("qualquer sequência de 11 números"). Faltava contexto. | Refatorei a Regex para validar a pontuação exata (`\d{3}\.\d{3}\.\d{3}-\d{2}`) e adicionei lógica de validação de dígito verificador para garantir que fosse um documento real. |
| **Arquivos PDF Bloqueados:** O script parava a execução total ao encontrar um PDF protegido por senha. | O método de extração lançava uma exceção não tratada que "crashava" o loop principal. | Adicionei uma verificação prévia `is_encrypted` e configurei o script para logar um aviso ("Arquivo X ignorado: Senha necessária") e pular para o próximo, mantendo a automação rodando. |

---

## ⚙️ 4. Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/automacao-auditoria-pdf.git](https://github.com/seu-usuario/automacao-auditoria-pdf.git)
    ```
2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure os diretórios:**
    * Coloque os arquivos PDF/TXT na pasta `/inputs`.
4.  **Execute o script:**
    ```bash
    python main.py
    ```
    *O relatório final será gerado na pasta `/outputs`.*

---

## 🚀 5. Próximos Passos (Roadmap)

Para a versão 2.0, o foco será em escalabilidade e segurança avançada:
* [ ] **Containerização:** Criar um `Dockerfile` para rodar a automação em ambiente isolado e seguro.
* [ ] **Log de Auditoria:** Implementar logs estruturados (JSON) para rastrear qual usuário executou a análise e quando.
* [ ] **OCR:** Integrar biblioteca `Tesseract` para ler PDFs digitalizados (imagens).

---
*Desenvolvido durante estudos de Especialização em Defesa Cibernética e AppSec.*