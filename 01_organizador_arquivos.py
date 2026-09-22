"""
01 - Organizador de Arquivos com IA
Objetivo: ler os nomes dos arquivos de uma pasta e pedir para a IA
sugerir uma categoria para cada um, depois mover para subpastas.

Este script NÃO abre o conteúdo dos arquivos, apenas usa o nome
do arquivo como pista inicial para introduzir o conceito de
"prompt com contexto" de forma simples e rápida.
"""

import os
import shutil
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
modelo = os.getenv("MODELO")
poder_processamento = os.getenv("POWER")

# Pasta que será organizada. Altere para testar com seus próprios arquivos.
PASTA_ALVO = "arquivos_teste"

# Categorias sugeridas (a IA pode escolher outra se fizer mais sentido)
CATEGORIAS = ["Documentos", "Imagens", "Planilhas", "Código", "Outros"]


def criar_pasta_teste_se_nao_existir():
    """Cria alguns arquivos de exemplo para testar o script, caso a pasta não exista."""
    if not os.path.exists(PASTA_ALVO):
        os.makedirs(PASTA_ALVO)
        exemplos = [
            "relatorio_financeiro.txt",
            "fotos_casamento.txt",
            "planilha_vendas.txt",
            "script_backup.txt",
            "notas_reuniao.txt",
        ]
        for nome in exemplos:
            with open(os.path.join(PASTA_ALVO, nome), "w") as f:
                f.write("arquivo de exemplo para a oficina")
        print(f"Pasta '{PASTA_ALVO}' criada com arquivos de exemplo.\n")


def classificar_arquivo(nome_arquivo: str) -> str:
    """Pergunta à IA em qual categoria o arquivo se encaixa melhor."""
    prompt = f"""Você é um assistente de organização de arquivos.
Dado o nome de um arquivo, responda APENAS com uma palavra, escolhendo
uma destas categorias: {", ".join(CATEGORIAS)}.

Nome do arquivo: {nome_arquivo}

Categoria:"""

    resposta = client.interactions.create(
        model=modelo,
        input=prompt,
        generation_config={"thinking_level": poder_processamento}
    )
    categoria = resposta.output_text

    # Garante que a IA não "inventou" uma categoria fora da lista
    if categoria not in CATEGORIAS:
        categoria = "Outros"
    return categoria


def organizar():
    criar_pasta_teste_se_nao_existir()
    arquivos = [
        f for f in os.listdir(PASTA_ALVO)
        if os.path.isfile(os.path.join(PASTA_ALVO, f))
    ]

    if not arquivos:
        print("Nenhum arquivo encontrado para organizar.")
        return

    for nome_arquivo in arquivos:
        categoria = classificar_arquivo(nome_arquivo)
        pasta_destino = os.path.join(PASTA_ALVO, categoria)
        os.makedirs(pasta_destino, exist_ok=True)

        origem = os.path.join(PASTA_ALVO, nome_arquivo)
        destino = os.path.join(pasta_destino, nome_arquivo)
        shutil.move(origem, destino)

        print(f"'{nome_arquivo}' -> {categoria}/")

    print("\nOrganização concluída!")


if __name__ == "__main__":
    organizar()
