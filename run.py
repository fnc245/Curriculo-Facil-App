# run.py
# SISTEMA CURRICULO FACIL VERSÃO 2.0
# AUTOR: FRANCISCO NEVES
# DATA: 27/06/2025
# Versão do arquivo run.py: V2.004
# Descrição: Ponto de entrada que agora cria uma aplicação de bandeja de sistema (system tray).
#            Inicia o servidor Flask em uma thread separada e fornece um ícone na bandeja para
#            interação do usuário. Corrigido o caminho para o ícone da aplicação.
# -----------------------------------------------------------------------------
import os
import sys
import webbrowser
from threading import Thread
from PIL import Image
from pystray import MenuItem as item, Icon as icon
from app import create_app


def resource_path(relative_path):
    """
    Retorna o caminho absoluto para o recurso, funcionando para desenvolvimento
    e para o executável criado pelo PyInstaller.
    """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Em modo de desenvolvimento, usa o caminho absoluto do script
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# --- Funções para o menu da bandeja ---
def open_chat(icon_instance, menu_item):
    """Abre o navegador na página do chat."""
    print("Abrindo o chat no navegador...")
    webbrowser.open("http://127.0.0.1:5001/app_chat")


def exit_app(icon_instance, menu_item):
    """Para o ícone e encerra o programa de forma abrupta."""
    print("Saindo da aplicação...")
    icon_instance.stop()
    # os._exit(0) é uma forma "forte" de fechar, que encerra o processo
    # imediatamente. Necessário porque o servidor Flask está em outra thread.
    os._exit(0)


# --- Lógica Principal ---
if __name__ == '__main__':
    # Cria a instância da aplicação Flask
    app = create_app()


    # Função para rodar o Flask em uma thread separada
    def run_flask():
        # debug=False e use_reloader=False são cruciais para rodar em uma thread
        # e para o PyInstaller funcionar corretamente.
        try:
            app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)
        except Exception as e:
            print(f"Erro ao iniciar o servidor Flask: {e}")


    print("Iniciando o servidor Flask em uma thread separada...")
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Prepara o ícone e o menu da bandeja
    try:
        # Usa a função resource_path para encontrar o ícone
        icon_path = resource_path("app_icon.ico")
        image = Image.open(icon_path)

        menu = (
            item('Abrir Currículo Fácil', open_chat, default=True),
            item('Sair', exit_app)
        )

        # Cria e roda a aplicação de bandeja
        print("Iniciando o ícone na bandeja do sistema...")
        icon_app = icon('CurriculoFacil', image, "Currículo Fácil", menu)
        icon_app.run()

    except FileNotFoundError:
        print("ERRO FATAL: O arquivo 'app_icon.ico' não foi encontrado.")
        # Em um cenário real, poderíamos mostrar uma caixa de diálogo de erro.
    except Exception as e:
        print(f"ERRO FATAL ao iniciar a aplicação de bandeja: {e}")