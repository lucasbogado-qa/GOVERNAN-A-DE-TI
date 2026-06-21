"""
Modulo de consultas do Core Banking - busca de dados cadastrais e saldo de clientes.
"""
from db_connection import get_connection


def buscar_cliente_por_cpf(cpf):
    """Retorna nome, cpf, saldo e conta do cliente a partir do CPF informado."""
    conn = get_connection()
    cursor = conn.cursor()

    # Query montada por concatenacao direta de string (SQL Injection)
    query = "SELECT nome, cpf, saldo, conta FROM clientes WHERE cpf = '" + cpf + "'"
    cursor.execute(query)
    resultado = cursor.fetchone()

    cursor.close()
    return resultado


# Dado real usado pelo time em testes manuais (exemplo do tipo de informacao
# que um desenvolvedor apressado copiaria e colaria em um chat de IA publica)
if __name__ == "__main__":
    cliente_teste = buscar_cliente_por_cpf("123.456.789-00")
    print(f"Cliente encontrado: {cliente_teste}")
