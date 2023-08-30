import cx_Oracle
import logging
from app.core import config
import pandas as pd
from .ftp_service import send_file_to_ftp_server
import os
import traceback

#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Placeholder for your actual implementation.
async def generate_excel_and_upload(transactions, file_name, date, parent_id):
    try:
        # 将数据转换为 Pandas DataFrame
        df = pd.DataFrame(transactions, columns=[
            '交易日期', '交易时间', '商户号', '商户名',
            '参考号', '终端号', '交易类型', '交易金额',
            '卡类型', '费率', '手续费', '分润金额'
        ])

        # 生成 Excel 文件
        # 检查保存路径是否存在，如果不存在则创建
        if not os.path.exists(config.SAVE_PATH):
            os.makedirs(config.SAVE_PATH)

        excel_path = f'{config.SAVE_PATH}/{file_name}'  # 请替换为您要保存文件的实际路径
        df.to_excel(excel_path, index=False, engine='openpyxl')

        # 使用 FTP 上传文件
        ftp_path = config.FTP_PATH + f'/{date}/' + f'{parent_id}/' + r'SALE/'# FTP服务器上的路径，需要您自己指定

        #ftp_path = config.FTP_PATH + f'/{date}/'
        send_file_to_ftp_server(file_name, ftp_path, config.SAVE_PATH)# 使用同步FTP

        logging.info(f"Excel file ftp_path {ftp_path} has been generated and uploaded.")
        logging.info(f"Excel file file_name {file_name} has been generated and uploaded.")

    except Exception as e:
        logging.error(f"An error occurred while generating and uploading Excel: {repr(e)}")
        traceback.print_exc()  # 打印堆栈信息

async def fetch_and_process_data(date):
    try:
        # Using context manager for handling Oracle Database connection
        with cx_Oracle.connect(
                config.ORACLE_USERNAME,
                config.ORACLE_PASSWORD,
                f"{config.ORACLE_HOST}:{config.ORACLE_PORT}/{config.ORACLE_DB}"
        ) as connection:

            # Using context manager for handling cursor
            with connection.cursor() as cursor:
                parent_id_query = """
                SELECT parent_id, param_value, param_name FROM sys_parameter@DBLINK_TO_FKCORE
                WHERE param_type = 'MERCHANT_CHANNEL' AND SUBSTR(parent_id, 1, 2) = '10'
                """
                logging.info(f"Executing SQL query: {parent_id_query}")
                cursor.execute(parent_id_query)

                while True:
                    row = cursor.fetchone()
                    if row is None:
                        break
                    parent_id, param_value, param_name = row
                    logging.info(f"Parent ID: {parent_id}, Param Value: {param_value}, Param Name: {param_name}")

                    file_name = f"SALE_{parent_id}_{date}.xls"

                    transaction_query = """
                    SELECT 
                        t.transactiondate as 交易日期,
                        REPLACE(LPAD(t.transactiontime, 6), ' ', '0') as 交易时间,
                        m.MRCHNO as 商户号, 
                        m.mrcht_name as 商户名, 
                        t.rrn as 参考号, 
                        t.terminalnumber as 终端号,
                        DECODE(t.txncode, 0, '消费', '20', '退货', t.txncode) as 交易类型,
                        t.transactionmoney as 交易金额,
                        t.cardtypename as 卡类型,
                        t.fee_order/100 as 费率,
                        t.PERFEE as 手续费,
                        t.amt_share as 分润金额
                    FROM 
                        T_TRANSACTION_RECORDS_ORG t,
                        MERCHANT_X@DBLINK_TO_FKCORE M
                    WHERE 
                        T.MERCHANTNUMBER = M.MRCHNO 
                        AND m.merchant_channel = :p_value
                        AND t.transactiondate = :p_date
                    """
                    logging.info(f"Executing SQL query: {transaction_query} with p_value: {param_value}, p_date: {date}")
                    cursor.execute(transaction_query, p_value=param_value, p_date=date)
                    transactions = cursor.fetchall()

                    if not transactions:
                        logging.info(f"No transactions found for Parent ID: {parent_id}, skipping...")
                        continue

                    await generate_excel_and_upload(transactions, file_name, date, parent_id)  # Assuming this function is defined elsewhere

    except cx_Oracle.DatabaseError as e:
        error_message = f"Oracle Database error occurred: {e}"
        logging.error(error_message)
        raise Exception(error_message)
    except Exception as e:
        error_message = f"An error occurred: {e}"
        logging.error(error_message)
        traceback.print_exc()
        raise Exception(error_message)
