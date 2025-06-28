# config.py
# SISTEMA CURRICULO FACIL VERSÃO 2.0
# AUTOR: FRANCISCO NEVES
# DATA: 27/06/2025
# Versão do arquivo config.py: V2.009
# Descrição: Centraliza todas as configurações da aplicação. Adicionadas configurações
#            para a extensão Flask-Session, movendo o armazenamento de sessão para o servidor.
# -----------------------------------------------------------------------------
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (útil para desenvolvimento)
load_dotenv()


class Config:
    """Classe de configuração da aplicação."""
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'uma-chave-secreta-padrao-para-desenvolvimento-v2'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

    ENCRYPTION_KEY = b'wE15i3z8hX-tT5_gA0nQ6bVlRzYjCnU-pFsK9jJ1eGk='
    DEFAULT_GEMINI_MODEL_NAME = 'gemini-2.0-flash'

    # Define um nome de pasta para os dados da aplicação
    APP_DATA_FOLDER_NAME = "CurriculoFacil"
    # Constrói o caminho para a pasta %APPDATA% (multiplataforma)
    APP_DATA_PATH = os.path.join(os.getenv('APPDATA', os.path.expanduser('~')), APP_DATA_FOLDER_NAME)

    # Os arquivos de configuração e dados agora usarão o APP_DATA_PATH como base
    USER_CONFIG_FILE = os.path.join(APP_DATA_PATH, 'user_config.ini')
    DATABASE_FILE = os.path.join(APP_DATA_PATH, 'curriculos.db')
    CURRICULOS_STORAGE_DIR_NAME = os.path.join(APP_DATA_PATH, "curriculos_gerados")

    # --- NOVAS CONFIGURAÇÕES PARA FLASK-SESSION ---
    # Define o tipo de armazenamento da sessão como 'filesystem'
    SESSION_TYPE = 'filesystem'
    # Define a pasta onde os arquivos de sessão serão armazenados
    SESSION_FILE_DIR = os.path.join(APP_DATA_PATH, 'flask_session')
    # Garante que os cookies de sessão sejam assinados
    SESSION_USE_SIGNER = True
    # (Opcional) Define a duração da sessão em segundos (ex: 30 minutos)
    PERMANENT_SESSION_LIFETIME = 1800

    # Configurações que não mudaram
    HTML_OUTPUT_MARKER = "[CURRICULO_FACIL_HTML_OUTPUT]"
    CURRICULOS_URL_ENDPOINT = "curriculos"