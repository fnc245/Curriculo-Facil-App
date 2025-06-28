# app/security.py
# SISTEMA CURRICULO FACIL VERSÃO 2.0
# AUTOR: FRANCISCO NEVES
# DATA: 21/06/2025
# Versão do arquivo security.py: V2.004
# Descrição: Módulo para lidar com a criptografia e descriptografia de dados sensíveis, como a API Key.
# -----------------------------------------------------------------------------
from cryptography.fernet import Fernet
from flask import current_app

def encrypt_data(data: str) -> bytes:
    """Criptografa uma string usando a chave da configuração."""
    key = current_app.config['ENCRYPTION_KEY']
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode('utf-8'))
    return encrypted_data

def decrypt_data(encrypted_data: bytes) -> str:
    """Descriptografa dados usando a chave da configuração."""
    try:
        key = current_app.config['ENCRYPTION_KEY']
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        print(f"Erro ao descriptografar dados: {e}")
        return None