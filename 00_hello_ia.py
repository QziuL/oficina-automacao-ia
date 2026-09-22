"""
00 - Hello IA
Objetivo: confirmar que o ambiente está configurado corretamente,
fazendo uma primeira chamada simples à API de IA.
"""

import os
from dotenv import load_dotenv
from google import genai

# Carrega as variáveis do arquivo .env (ex: GEMINI_API_KEY)
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
modelo = os.getenv("MODELO")
poder_processamento = os.getenv("POWER")

prompt = "Em uma frase, explique o que é automação de tarefas."

resposta = client.interactions.create(
    model=modelo,
    input=prompt,
    generation_config={"thinking_level": poder_processamento}
)

texto_resposta = resposta.output_text
print("=" * 50)
print("Resposta da IA:")
print(texto_resposta)
print("=" * 50)
