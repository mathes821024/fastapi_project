# Oracle数据库服务
import cx_Oracle


def query_oracle_database(merchant_id, settlement_date):
    connection = cx_Oracle.connect("username", "password", "localhost/orcl")
    cursor = connection.cursor()

    query = """SELECT * FROM your_table
               WHERE merchant_id = :merchant_id
               AND settlement_date = :settlement_date"""
    cursor.execute(query, merchant_id=merchant_id, settlement_date=settlement_date)

    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return results

