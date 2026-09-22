# Oficina: Automação de Tarefas com Python + IA

## Setup rápido

1. Abra esta pasta no VSCode.
2. Abra o terminal integrado (Ctrl+ ` ou Cmd+ `).
3. (Opcional, mas recomendado) Crie um ambiente virtual:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Copie `.env.example` para `.env` e cole sua chave de API do Gemini
   ([AI Studio](https://aistudio.google.com/api-keys) -> API Keys -> Criar chave de API).
6. Teste se está tudo funcionando:
   ```bash
   python 00_hello_ia.py
   ```
   Se aparecer uma resposta da IA no terminal, está pronto!

## Scripts desta oficina

| Arquivo | O que faz |
|---|---|
| `00_hello_ia.py` | Testa a conexão com a API de IA |
| `01_organizador_arquivos.py` | Organiza arquivos de uma pasta em subpastas por categoria, usando IA para decidir a categoria |
| `02_resumir_pdf.py` | Lê um PDF e gera um resumo automático com IA |
| `03_classificador_textos.py` | Classifica uma lista de textos (ex: mensagens, tickets) por categoria e urgência |
| `04_projeto_final_relatorio.py` | Projeto guiado: lê vários arquivos de uma pasta e gera um relatório consolidado em texto |

## Dúvidas comuns

- **"ModuleNotFoundError"** → o ambiente virtual não está ativado ou o `pip install` não rodou. Repita o passo 3 e 4.
- **"AuthenticationError"** → confira se colou a chave corretamente no `.env`, sem espaços ou aspas.
- **Nada acontece / trava** → verifique sua conexão com a internet.
