# app/routes.py
# SISTEMA CURRICULO FACIL VERSÃO 2.0
# AUTOR: FRANCISCO NEVES
# DATA: 27/06/2025
# Versão do arquivo routes.py: V2.012
# Descrição: Sem mudanças funcionais. O uso do objeto 'session' permanece o mesmo,
#            mas agora é gerenciado pela extensão Flask-Session no backend.
# -----------------------------------------------------------------------------
import os
import re
import configparser
from datetime import datetime
from flask import (
    render_template, request, jsonify, session, send_from_directory, url_for,
    current_app, g
)
from werkzeug.exceptions import NotFound
from .services.gemini_service import GeminiService
from .security import encrypt_data
from .utils import get_best_local_ip


@current_app.before_request
def prepare_dynamic_context():
    """
    Executa antes de cada requisição. Prepara as instruções de sistema dinâmicas
    apenas uma vez por sessão de usuário e as armazena no objeto 'g'.
    """
    if 'instructions_prepared' not in session:
        base_instructions = current_app.config.get('BASE_SYSTEM_INSTRUCTIONS', "")

        local_ip = get_best_local_ip()
        if local_ip:
            port = request.environ.get('SERVER_PORT', '5001')
            local_ip_url = f"http://{local_ip}:{port}/app_chat"

            ip_context = (
                f"\n\nContexto Adicional do Sistema: A URL de acesso para outros dispositivos nesta rede local é {local_ip_url}. "
                "Se o usuário perguntar qual é o endereço de acesso local, o endereço de IP ou como acessar de outro computador, forneça esta URL."
            )
            session['full_system_instructions'] = base_instructions + ip_context
            print(f"Instruções dinâmicas (com IP) preparadas para a sessão.")
        else:
            session['full_system_instructions'] = base_instructions
            print(f"Instruções base preparadas para a sessão.")

        session['instructions_prepared'] = True

    g.dynamic_system_instructions = session.get('full_system_instructions')


@current_app.route('/app_chat', methods=['GET'])
def chat_page():
    if 'chat_history' not in session:
        session['chat_history'] = []

    needs_api_key = current_app.config.get('NEEDS_API_KEY', True)
    return render_template('chat.html', needs_api_key=needs_api_key)


@current_app.route('/reset_chat_history', methods=['POST'])
def reset_chat():
    # Limpa toda a sessão para garantir que as instruções sejam recriadas
    session.clear()
    print("Sessão do usuário limpa.")
    return jsonify({"status": "sucesso", "mensagem": "Seu histórico de chat foi reiniciado."})


@current_app.route(f"/{current_app.config['CURRICULOS_URL_ENDPOINT']}/<path:filename>")
def servir_curriculo_gerado(filename):
    if '..' in filename or filename.startswith('/'):
        raise NotFound("Nome de arquivo inválido.")
    storage_path = current_app.config['CURRICULOS_STORAGE_DIR_NAME']
    try:
        return send_from_directory(storage_path, filename, as_attachment=False)
    except FileNotFoundError:
        raise NotFound("Arquivo de currículo não encontrado.")
    return "Erro ao servir o arquivo.", 500


@current_app.route('/chat', methods=['POST'])
def handle_chat():
    if 'chat_history' not in session:
        session['chat_history'] = []
    try:
        data = request.get_json()
        user_prompt = data.get('prompt', '').strip()
        if not user_prompt:
            return jsonify({"status": "erro", "mensagem": "Payload inválido."}), 400

        if current_app.config.get('NEEDS_API_KEY'):
            temp_gemini_service = GeminiService(api_key=user_prompt)
            if temp_gemini_service.validate_api_key():
                encrypted_key = encrypt_data(user_prompt)
                user_config_path = current_app.config['USER_CONFIG_FILE']
                config = configparser.ConfigParser()
                config['Credentials'] = {'EncryptedApiKey': encrypted_key.decode('latin1')}
                with open(user_config_path, 'w') as configfile:
                    config.write(configfile)

                current_app.config['GEMINI_API_KEY'] = user_prompt
                current_app.config['NEEDS_API_KEY'] = False

                response_message = "Chave de API válida e salva com sucesso! Agora podemos começar. Como posso te ajudar?"
                session.clear()
                session['chat_history'] = [{'role': 'model', 'parts': [response_message]}]
                return jsonify({"status": "sucesso", "resposta_assistente": response_message})
            else:
                response_message = "API Key inválida. Por favor, verifique sua chave e tente novamente."
                return jsonify({"status": "sucesso", "resposta_assistente": response_message})

        current_session_history = session.get('chat_history', [])
        gemini = GeminiService()
        chat_session = gemini.start_session_with_history(current_session_history)
        assistant_response = gemini.get_chat_response(chat_session, user_prompt)
        final_message_to_user = assistant_response
        current_session_history.append({'role': 'user', 'parts': [user_prompt]})
        html_marker = current_app.config['HTML_OUTPUT_MARKER']
        salvo_com_sucesso = False

        if html_marker in assistant_response:
            try:
                marker_position = assistant_response.index(html_marker)
                html_content = assistant_response[marker_position + len(html_marker):].strip()
                storage_path = current_app.config['CURRICULOS_STORAGE_DIR_NAME']
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                session_id_for_file = "user"
                filename = f"curriculo_{session_id_for_file}_{timestamp}.html"
                filepath = os.path.join(storage_path, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(html_content)
                salvo_com_sucesso = True
                link = url_for('servir_curriculo_gerado', filename=filename, _external=False)
                confirm_msg = f"Seu arquivo HTML foi gerado e salvo! Você pode visualizá-lo [aqui]({link})."
                dicas = gemini.get_dicas(chat_session)
                if dicas:
                    final_message_to_user = f"{confirm_msg}\n\n{dicas}\n\nBOA SORTE E ATÉ A PRÓXIMA!"
                else:
                    final_message_to_user = f"{confirm_msg}\n\nATÉ A PRÓXIMA!"
                session.clear()
            except Exception as e:
                final_message_to_user = "Houve um erro ao processar e salvar seu documento."
                current_session_history.append({'role': 'model', 'parts': [final_message_to_user]})
                session['chat_history'] = current_session_history

        if not salvo_com_sucesso:
            current_session_history.append({'role': 'model', 'parts': [final_message_to_user]})
            session['chat_history'] = current_session_history

        return jsonify({"status": "sucesso", "resposta_assistente": final_message_to_user})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "erro", "mensagem": f"Erro interno no servidor: {type(e).__name__}"}), 500