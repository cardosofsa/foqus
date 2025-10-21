import logging
import requests
import os
from django.conf import settings

logger = logging.getLogger(__name__)

def obter_resposta_ia(assunto, tipo_prompt, pergunta=None):
    """
    Integração com serviço de IA para fornecer respostas inteligentes.
    Por enquanto é um mock, mas pode ser integrado com OpenAI, Google AI, etc.
    """
    try:
        # Mapeamento de tipos de prompt para respostas padrão
        respostas_base = {
            'simplificar': f"Vou simplificar '{assunto}' para você: Imagine que {assunto} é como...",
            'questoes': f"Aqui estão 3 questões sobre '{assunto}':\n\n1. Questão prática 1\n2. Questão prática 2\n3. Questão prática 3",
            'explicar': f"Vou explicar '{assunto}' detalhadamente: Este conceito trata de...",
            'exercicios': f"Aqui estão alguns exercícios sobre '{assunto}':\n\n• Exercício 1\n• Exercício 2\n• Exercício 3"
        }

        # Resposta base + pergunta específica se fornecida
        resposta = respostas_base.get(tipo_prompt, f"Aqui está uma explicação sobre '{assunto}'.")
        
        if pergunta:
            resposta += f"\n\nSobre sua pergunta '{pergunta}': {gerar_resposta_para_pergunta(pergunta, assunto)}"

        return resposta

    except Exception as e:
        logger.error(f"Erro no serviço de IA: {e}")
        return f"Desculpe, houve um erro ao processar sua solicitação sobre '{assunto}'. Tente novamente."

def gerar_resposta_para_pergunta(pergunta, assunto):
    """
    Gera uma resposta específica para uma pergunta do usuário.
    (Implementação mock - integrar com IA real posteriormente)
    """
    respostas_genericas = [
        "Essa é uma ótima pergunta! Em relação a este tópico, é importante considerar...",
        "Essa dúvida é comum quando se estuda este assunto. A resposta envolve...",
        "Excelente questionamento! Vamos analisar isso passo a passo...",
        "Essa pergunta nos leva a refletir sobre aspectos fundamentais de..."
    ]
    
    import random
    return random.choice(respostas_genericas)

# Função para integração futura com APIs de IA reais
def chamar_api_ia_externa(mensagem, contexto):
    """
    Função para integração com APIs de IA como OpenAI, Google Gemini, etc.
    """
    # Exemplo com OpenAI (descomente quando tiver a API key)
    """
    try:
        import openai
        openai.api_key = settings.OPENAI_API_KEY
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um tutor especializado em ensino médio e preparação para ENEM."},
                {"role": "user", "content": mensagem}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Erro na API OpenAI: {e}")
        return "Desculpe, não consegui processar sua solicitação no momento."
    """
    pass