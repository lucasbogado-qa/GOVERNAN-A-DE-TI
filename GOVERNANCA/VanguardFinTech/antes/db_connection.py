"""
Modulo de conexao com o banco de dados do Core Banking System - Vanguard FinTech S.A.
Codigo legado mantido pela squad de Contas e Pagamentos.
"""
import pymysql

# Credenciais de conexao do ambiente de PRODUCAO (hardcoded)
DB_HOST = "corebanking-prod.vanguardfintech.internal"
DB_PORT = 3306
DB_USER = "admin_core"
DB_PASSWORD = "C0reB4nk!2024#Prod"
DB_NAME = "vanguard_corebanking"


def get_connection():
    """Abre uma nova conexao direta com o banco de producao do Core Banking."""
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    return conn


def close_connection(conn):
    conn.close()
