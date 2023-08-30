#app/config.py
# 项目配置文件
import os

# FTP Credentials
FTP_SERVER = os.getenv("FTP_SERVER", "192.168.10.245")
FTP_USERNAME = os.getenv("FTP_USERNAME", "npaydev")
FTP_PASSWORD = os.getenv("FTP_PASSWORD", "npaydev")
FTP_PATH = os.getenv("FTP_PATH", "/FKN")
FTP_PORT = os.getenv("FTP_PORT", "21")

#save path
SAVE_PATH = os.getenv("HOME", "/home/pyapp")+"/save_reconciliation_file"

# Oracle Credentials
ORACLE_USERNAME = os.getenv("ORACLE_USERNAME", "fkslt")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "fkslt")
ORACLE_HOST = os.getenv("ORACLE_HOST", "192.168.6.86")
ORACLE_DB = os.getenv("ORACLE_DB", "orcl")
ORACLE_PORT = "1521"  # 确保这一行存在

