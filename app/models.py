# app/models.py
# SISTEMA CURRICULO FACIL VERSÃO 2.0
# AUTOR: FRANCISCO NEVES
# DATA: 21/06/2025
# Versão do arquivo models.py: V2.001
# -----------------------------------------------------------------------------
import sqlite3
import click
from flask import current_app, g


def get_db():
    """
    Cria uma conexão com o banco de dados, se ainda não existir para a requisição atual.
    A conexão é armazenada em 'g', um objeto especial do Flask para cada requisição.
    """
    if 'db' not in g:
        db_path = os.path.join(current_app.root_path, '..', current_app.config['DATABASE_FILE'])
        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # Permite acessar colunas por nome

    return g.db


def close_db(e=None):
    """
    Fecha a conexão com o banco de dados no final da requisição.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """
    Executa o schema SQL para criar a(s) tabela(s) do banco de dados.
    """
    db = get_db()

    # O schema pode ser movido para um arquivo .sql se ficar complexo
    schema = """
    CREATE TABLE IF NOT EXISTS curriculos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nome_completo_normalizado TEXT NOT NULL,
      telefone TEXT NOT NULL,
      html_conteudo TEXT NOT NULL,
      data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(nome_completo_normalizado, telefone)
    );

    CREATE INDEX IF NOT EXISTS idx_nome_completo ON curriculos (nome_completo_normalizado);
    CREATE INDEX IF NOT EXISTS idx_telefone ON curriculos (telefone);
    """
    db.executescript(schema)
    print("Banco de dados inicializado.")


@click.command('init-db')
def init_db_command():
    """Comando de console para limpar dados existentes e criar novas tabelas."""
    init_db()
    click.echo('Banco de dados inicializado.')


def db_init_app(app):
    """
    Registra as funções de gerenciamento do banco de dados com a aplicação Flask.
    """
    app.teardown_appcontext(close_db)  # Chama close_db ao final de cada requisição
    app.cli.add_command(init_db_command)  # Adiciona o comando 'flask init-db'
