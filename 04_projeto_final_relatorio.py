"""
04 - Projeto Final: Gerador de Relatório Consolidado
Objetivo: juntar tudo que foi visto. O script lê todos os
arquivos .txt de uma pasta (poderiam ser anotações, chamados, respostas
de formulário, etc.), envia o conteúdo combinado para a IA e pede um
relatório consolidado em Markdown, pronto para compartilhar com a equipe.

Use este script como ponto de partida: o prompt e a fonte dos dados 
(trocar .txt por PDFs, planilhas, e-mails, etc.) podem ser ajustados 
para o próprio contexto de trabalho.
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
modelo = os.getenv("MODELO")
poder_processamento = os.getenv("POWER")

PASTA_DADOS = "notas_do_dia"
ARQUIVO_SAIDA = "relatorio_final.md"


def criar_dados_exemplo_se_nao_existir():
    if not os.path.exists(PASTA_DADOS):
        os.makedirs(PASTA_DADOS)
        exemplos = {
            "nota_1.txt": "Reunião com cliente A: interessado em fechar contrato, pediu proposta até sexta.",
            "nota_2.txt": "Bug reportado no módulo de pagamentos, 3 usuários afetados, prioridade alta.",
            "nota_3.txt": "Equipe de marketing pediu orçamento extra para campanha de fim de ano.",
        }
        for nome, conteudo in exemplos.items():
            with open(os.path.join(PASTA_DADOS, nome), "w", encoding="utf-8") as f:
                f.write(conteudo)
        print(f"Pasta '{PASTA_DADOS}' criada com notas de exemplo.\n")


def ler_todos_os_arquivos(pasta: str) -> str:
    conteudo_combinado = ""
    for nome_arquivo in sorted(os.listdir(pasta)):
        caminho = os.path.join(pasta, nome_arquivo)
        if os.path.isfile(caminho) and nome_arquivo.endswith(".txt"):
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo_combinado += f"### {nome_arquivo}\n{f.read()}\n\n"
    return conteudo_combinado


def gerar_relatorio(conteudo: str) -> str:
    data_hoje = datetime.now().strftime(f"%d/%m/%Y")

    prompt = f"""Você é um assistente que ajuda a consolidar anotações do dia
em um relatório executivo curto e organizado.

Abaixo estão várias notas soltas. Gere um relatório em Markdown com:
1. Um resumo geral (2-3 frases)
2. Uma seção "Pontos de Atenção" (itens urgentes ou que precisam de ação)
3. Uma seção "Próximos Passos" (lista de ações recomendadas)

Data do relatório: {data_hoje}

NOTAS:
{conteudo}
"""

    resposta = client.interactions.create(
        model=modelo,
        input=prompt,
        generation_config={"thinking_level": poder_processamento}
    )
    return resposta.output_text


if __name__ == "__main__":
    criar_dados_exemplo_se_nao_existir()

    print("Lendo notas...")
    conteudo = ler_todos_os_arquivos(PASTA_DADOS)

    if not conteudo:
        print("Nenhuma nota encontrada.")
    else:
        print("Gerando relatório com IA...\n")
        relatorio = gerar_relatorio(conteudo)

        with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
            f.write(relatorio)

        print("=" * 50)
        print(relatorio)
        print("=" * 50)
        print(f"\nRelatório também salvo em '{ARQUIVO_SAIDA}'")
