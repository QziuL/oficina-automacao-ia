"""
02 - Resumidor de PDF com IA
Objetivo: extrair o texto de um PDF e pedir para a IA gerar um
resumo em tópicos. Introduz o conceito de "ler um arquivo real
e enviar o conteúdo como parte do prompt".
"""

import os
from dotenv import load_dotenv
from google import genai
from PyPDF2 import PdfReader

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
modelo = os.getenv("MODELO")
poder_processamento = os.getenv("POWER")

# Altere para o caminho do seu PDF de teste
CAMINHO_PDF = "documento_exemplo.pdf"


def extrair_texto_pdf(caminho: str) -> str:
    leitor = PdfReader(caminho)
    texto_completo = ""
    for pagina in leitor.pages:
        texto_completo += pagina.extract_text() + "\n"
    return texto_completo


def resumir_texto(texto: str) -> str:
    # Limita o tamanho para caber tranquilamente no contexto do modelo
    texto_limitado = texto[:15000]

    prompt = f"""Resuma o texto abaixo em até 5 tópicos (bullet points),
destacando os pontos mais importantes. Responda em português.

TEXTO:
{texto_limitado}

RESUMO EM TÓPICOS:"""

    resposta = client.interactions.create(
        model=modelo,
        input=prompt,
        generation_config={"thinking_level": poder_processamento}
    )
    return resposta.output_text


if __name__ == "__main__":
    if not os.path.exists(CAMINHO_PDF):
        print(f"Arquivo '{CAMINHO_PDF}' não encontrado.")
        print("Coloque um PDF de teste nesta pasta e ajuste a variável CAMINHO_PDF.")
    else:
        print("Lendo PDF...")
        texto = extrair_texto_pdf(CAMINHO_PDF)

        print("Gerando resumo com IA...\n")
        resumo = resumir_texto(texto)

        print("=" * 50)
        print("RESUMO:")
        print(resumo)
        print("=" * 50)
