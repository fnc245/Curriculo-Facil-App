# app/services/gemini_service.py (V2.009)
# SISTEMA CURRICULO FACIL VERSÃO 2.0
# AUTOR: FRANCISCO NEVES
# DATA: 27/06/2025
# Versão do arquivo gemini_service.py: V2.009
# Descrição: Isola a lógica da API Gemini. O log de inicialização do modelo
#            foi removido para limpar a saída do console.
# -----------------------------------------------------------------------------
import google.generativeai as genai
from flask import current_app, g


class GeminiService:
    def __init__(self, api_key=None):
        self.api_key = api_key or current_app.config.get('GEMINI_API_KEY')
        self.model_name = current_app.config.get('GEMINI_MODEL_NAME')

        if not self.api_key:
            self.is_configured = False
        else:
            genai.configure(api_key=self.api_key)
            self.is_configured = True

        self.system_instructions = g.get('dynamic_system_instructions', None)

        if not self.system_instructions:
            print("AVISO: Instruções de sistema não encontradas no contexto da requisição 'g'.")

    def start_session_with_history(self, history):
        if not self.is_configured: return None

        model_kwargs = {'model_name': self.model_name}
        if self.system_instructions:
            model_kwargs['system_instruction'] = self.system_instructions

        model = genai.GenerativeModel(**model_kwargs)
        return model.start_chat(history=history)

    def get_chat_response(self, chat_session, user_prompt):
        if not chat_session: return "Erro: A sessão de chat não pôde ser iniciada. Verifique a API Key."
        try:
            response = chat_session.send_message(user_prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Erro na chamada da API Gemini: {e}")
            return "Desculpe, ocorreu um erro ao comunicar com a IA. Tente novamente."

    def get_dicas(self, chat_session):
        if not chat_session: return ""
        prompt = (
            "Contexto para você, IA: O usuário acabou de ter um documento HTML gerado e salvo com sucesso. "
            "Agora, por favor, forneça um texto que inclua 2 ou 3 dicas curtas e práticas para uma entrevista de emprego."
        )
        try:
            response = chat_session.send_message(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Erro na chamada da API Gemini para dicas: {e}")
            return ""

    def validate_api_key(self):
        if not self.is_configured:
            return False
        try:
            genai.list_models()
            return True
        except Exception as e:
            print(f"Falha na validação da API Key: {e}")
            return False