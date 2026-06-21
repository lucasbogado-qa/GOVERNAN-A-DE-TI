# AI-Generated: Claude (Anthropic) — Vanguard FinTech S.A.
# REG-03: Código gerado por IA. Revisão humana obrigatória antes do merge (REG-04).
# ============================================================
# Módulo: db_client.py
# Responsabilidade: Conexão pooled e consulta parametrizada de clientes.
# ============================================================

import os
import logging
from contextlib import contextmanager
from psycopg2 import pool, OperationalError, DatabaseError

logger = logging.getLogger(__name__)

# ------------------------------------------------------------
# CORREÇÃO 1 — Credenciais via variáveis de ambiente
# Nunca hardcode credenciais em código-fonte.
# Configure as variáveis no secrets manager / CI pipeline.
# ------------------------------------------------------------
_DB_CONFIG = {
    "host":     os.environ["DB_HOST"],
    "user":     os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "dbname":   os.environ["DB_NAME"],
    "port":     int(os.environ.get("DB_PORT", 5432)),
}

# ------------------------------------------------------------
# CORREÇÃO 2 — Connection Pool (evita esgotamento de conexões)
# minconn / maxconn devem ser ajustados conforme capacity plan.
# ------------------------------------------------------------
_MIN_CONN = int(os.environ.get("DB_POOL_MIN", 2))
_MAX_CONN = int(os.environ.get("DB_POOL_MAX", 10))

try:
    _pool: pool.ThreadedConnectionPool = pool.ThreadedConnectionPool(
        _MIN_CONN, _MAX_CONN, **_DB_CONFIG
    )
    logger.info("Connection pool inicializado (min=%s, max=%s).", _MIN_CONN, _MAX_CONN)
except OperationalError as exc:
    logger.critical("Falha ao criar o connection pool: %s", exc)
    raise


@contextmanager
def get_connection():
    """
    Context manager que retira uma conexão do pool e a devolve ao final,
    mesmo em caso de exceção — prevenindo vazamento de conexões.

    Uso:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(...)
    """
    conn = _pool.getconn()
    try:
        yield conn
        conn.commit()
    except DatabaseError:
        conn.rollback()
        raise
    finally:
        _pool.putconn(conn)


# ------------------------------------------------------------
# CORREÇÃO 3 — Prepared Statement (elimina SQL Injection)
# O driver substitui %s por valores escapados com segurança.
# ------------------------------------------------------------

# Colunas retornadas explicitamente (sem SELECT *).
_CLIENTE_FIELDS = ("nome", "cpf", "saldo", "conta")
_SQL_BUSCA_CPF = (
    "SELECT nome, cpf, saldo, conta "
    "FROM clientes "
    "WHERE cpf = %s"           # ← parâmetro posicional: NUNCA concatenar string
)


def buscar_cliente_por_cpf(cpf: str) -> dict | None:
    """
    Retorna um dict com os dados do cliente ou None se não encontrado.

    Args:
        cpf: CPF do cliente (somente dígitos, sem máscara).

    Returns:
        dict com chaves (nome, cpf, saldo, conta) ou None.

    Raises:
        ValueError: se cpf for inválido.
        DatabaseError: se ocorrer erro na consulta.
    """
    if not cpf or not cpf.isdigit() or len(cpf) != 11:
        raise ValueError(f"CPF inválido: '{cpf}'. Esperado: 11 dígitos numéricos.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(_SQL_BUSCA_CPF, (cpf,))   # tupla obrigatória como 2º arg
            row = cur.fetchone()

    if row is None:
        logger.info("Cliente não encontrado para o CPF fornecido.")
        return None

    return dict(zip(_CLIENTE_FIELDS, row))
