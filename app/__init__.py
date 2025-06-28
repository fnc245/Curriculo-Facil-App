# app/__init__.py
# SISTEMA CURRICULO FACIL VERSÃO 2.0
# AUTOR: FRANCISCO NEVES
# DATA: 27/06/2025
# Versão do arquivo __init__.py: V2.009
# Descrição: Fábrica da App. Agora inicializa a extensão Flask-Session para
#            gerenciar sessões no lado do servidor, resolvendo o problema de cookies grandes.
# -----------------------------------------------------------------------------
import os
import configparser
from flask import Flask
from flask_session import Session  # Importa a extensão
from config import Config
from .services.prompt_config import SYSTEM_INSTRUCTIONS


def _load_and_set_user_configs(app):
    """Carrega configs do user_config.ini e as aplica sobre os padrões."""
    from .security import decrypt_data

    user_config_path = app.config['USER_CONFIG_FILE']
    user_cfg = configparser.ConfigParser()

    app.config['NEEDS_API_KEY'] = True
    app.config['GEMINI_MODEL_NAME'] = app.config.get('DEFAULT_GEMINI_MODEL_NAME')

    if os.path.exists(user_config_path):
        user_cfg.read(user_config_path)
        if 'Credentials' in user_cfg and 'EncryptedApiKey' in user_cfg['Credentials']:
            encrypted_key_str = user_cfg['Credentials']['EncryptedApiKey']
            if encrypted_key_str:
                encrypted_key_bytes = encrypted_key_str.encode('latin1')
                decrypted_key = decrypt_data(encrypted_key_bytes)
                if decrypted_key:
                    app.config['GEMINI_API_KEY'] = decrypted_key
                    app.config['NEEDS_API_KEY'] = False
                    print("API Key do usuário carregada com sucesso.")

        if 'Settings' in user_cfg and 'ModelName' in user_cfg['Settings']:
            model_name = user_cfg['Settings']['ModelName'].strip()
            if model_name:
                app.config['GEMINI_MODEL_NAME'] = model_name
                print(f"Modelo Gemini sobrescrito pelo user_config.ini: {model_name}")

    if app.config['NEEDS_API_KEY']:
        print("API Key do usuário não encontrada. Aplicação em modo de configuração.")


def create_app(config_class=Config):
    """Fábrica da aplicação Flask. Cria e configura a instância do Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- INICIALIZAÇÃO DO FLASK-SESSION ---
    # Inicializa a extensão, que lerá a configuração do app.config
    Session(app)

    # Armazena as instruções base na config UMA VEZ.
    app.config['BASE_SYSTEM_INSTRUCTIONS'] = SYSTEM_INSTRUCTIONS

    # Garante que as pastas de dados existem
    if not os.path.exists(app.config['APP_DATA_PATH']):
        os.makedirs(app.config['APP_DATA_PATH'])
    if not os.path.exists(app.config['CURRICULOS_STORAGE_DIR_NAME']):
        os.makedirs(app.config['CURRICULOS_STORAGE_DIR_NAME'])
    # Garante que a pasta para as sessões do Flask-Session existe
    if not os.path.exists(app.config['SESSION_FILE_DIR']):
        os.makedirs(app.config['SESSION_FILE_DIR'])

    with app.app_context():
        _load_and_set_user_configs(app)

        from . import routes
        from .models import db_init_app
        db_init_app(app)

    return app