"""
03 - Classificador de Textos com IA (saída estruturada em JSON)
Objetivo: simular uma caixa de mensagens/tickets de suporte e usar
a IA para classificar cada um por categoria e urgência, retornando
dados estruturados (JSON) prontos para usar em uma planilha ou painel.
"""

import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
modelo = os.getenv("MODELO")
poder_processamento = os.getenv("POWER")

# Mensagens de exemplo (poderiam vir de um e-mail, formulário, planilha, etc.)
MENSAGENS_EXEMPLO = [
    "O sistema caiu e não conseguimos emitir notas fiscais, isso está travando as vendas!",
    "Gostaria de saber se vocês têm plano anual com desconto.",
    "Meu login parou de funcionar desde ontem à noite.",
    "Só queria elogiar o atendimento, foi ótimo!",
]


def classificar_mensagem(mensagem: str) -> dict:
    prompt = f"""Classifique a mensagem abaixo e responda APENAS em JSON válido,
sem nenhum texto antes ou depois, seguindo exatamente este formato:

{{"categoria": "Suporte Técnico | Comercial | Elogio | Outro",
  "urgencia": "Alta | Média | Baixa",
  "resumo": "resumo de até 10 palavras"}}

MENSAGEM: "{mensagem}"
"""

    resposta = client.interactions.create(
        model=modelo,
        input=prompt,
        generation_config={"thinking_level": poder_processamento}
    )

    texto = resposta.output_text
    # Remove possíveis marcações de bloco de código, caso a IA adicione
    texto = texto.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        return {"categoria": "Erro", "urgencia": "N/A", "resumo": "Falha ao interpretar resposta"}


if __name__ == "__main__":
    resultados = []

    for mensagem in MENSAGENS_EXEMPLO:
        print(f"Classificando: {mensagem[:50]}...")
        classificacao = classificar_mensagem(mensagem)
        classificacao["mensagem_original"] = mensagem
        resultados.append(classificacao)

    print("\n" + "=" * 60)
    print("RESULTADO FINAL:")
    print("=" * 60)
    for r in resultados:
        print(f"[{r['urgencia']:^6}] {r['categoria']:<18} -> {r['resumo']}")

    # Bônus: salvar em JSON para usar em outro sistema/planilha
    with open("classificacoes.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print("\nResultados salvos em 'classificacoes.json'")
