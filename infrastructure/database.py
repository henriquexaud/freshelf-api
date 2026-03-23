import os
import sqlite3
from contextlib import closing

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "produtos.db")

COLUNAS_PRODUTOS = ["id", "nome", "quantidade", "data_validade"]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _colunas_produtos(conn):
    return [row["name"] for row in conn.execute("PRAGMA table_info(produtos)").fetchall()]


def _criar_tabela_produtos(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data_validade TEXT NOT NULL
        )
        """
    )


def _migrar_schema_produtos(conn, colunas_origem):
    colunas_comuns = [coluna for coluna in COLUNAS_PRODUTOS if coluna in colunas_origem]

    conn.execute("ALTER TABLE produtos RENAME TO produtos_antiga")
    _criar_tabela_produtos(conn)
    if colunas_comuns:
        lista_colunas = ", ".join(colunas_comuns)
        conn.execute(
            f"""
            INSERT INTO produtos ({lista_colunas})
            SELECT {lista_colunas}
            FROM produtos_antiga
            """
        )
    conn.execute("DROP TABLE produtos_antiga")


def init_db():
    with closing(get_db()) as conn:
        _criar_tabela_produtos(conn)
        colunas = _colunas_produtos(conn)
        if sorted(colunas) != sorted(COLUNAS_PRODUTOS):
            _migrar_schema_produtos(conn, colunas)
        conn.commit()