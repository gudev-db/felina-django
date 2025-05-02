import os
import requests
import openai
from typing import List, Dict
from django.conf import settings

# Configuração da API da OpenAI
openai.api_key = settings.OPENAI_API_KEY

class AstraDBClient:
    def __init__(self):
        self.base_url = f"{settings.ASTRA_DB_API_BASE}/api/json/v1/{settings.ASTRA_DB_NAMESPACE}"
        self.headers = {
            "Content-Type": "application/json",
            "x-cassandra-token": settings.ASTRA_DB_TOKEN,
            "Accept": "application/json"
        }
    
    def vector_search(self, collection: str, vector: List[float], limit: int = 3) -> List[Dict]:
        """Realiza busca por similaridade vetorial"""
        url = f"{self.base_url}/{collection}"
        payload = {
            "find": {
                "sort": {"$vector": vector},
                "options": {"limit": limit}
            }
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()["data"]["documents"]
        except Exception as e:
            print(f"Erro na busca vetorial: {str(e)}")
            if 'response' in locals():
                print(f"Resposta da API: {response.text}")
            return []

def get_embedding(text: str) -> List[float]:
    """Obtém embedding do texto usando OpenAI"""
    try:
        response = openai.Embedding.create(
            input=text,
            model=settings.EMBEDDING_MODEL
        )
        return response["data"][0]["embedding"]
    except Exception as e:
        print(f"Erro ao obter embedding: {str(e)}")
        return []

def generate_response(query: str, context: str) -> str:
    """Gera resposta usando o modelo de chat da OpenAI"""
    if not context:
        return "Não encontrei informações relevantes para responder sua pergunta."
    
    prompt = f"""Responda baseado no contexto abaixo:
    
    Contexto:
    {context}
    
    Pergunta: {query}
    Resposta:"""
    
    try:
        response = openai.ChatCompletion.create(
            model=settings.CHAT_MODEL,
            messages=[
                {"role": "system", "content": '''
                
                Você é o co piloto do laboratório conhecido como LASID. O grupo de estudos em sistemas dinâmicos. Você está aqui para
                ajudar o usuário a fazer manuseio das ferramentas que ele pedir. Assim como fornecer fundamentação teórica sobre vibrações. Aprofunde
                ao máximo as suas explicações, você está aqui para garantir que o usuário consiga fazer uso das ferramentas cujos manuais estão em sua
                base de informações.

                
                
                
                
                '''},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"
