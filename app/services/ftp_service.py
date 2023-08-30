# app/services/ftp_service.py
from ftplib import FTP
from app.core import config
from fastapi import HTTPException


import logging

logger = logging.getLogger(__name__)


def send_file_to_ftp_server(filename, path, save_path):
    try:
        # Connect to FTP server
        print(f"send_file_to_ftp_server path {path}",path)
        ftp = FTP()
        ftp.connect(config.FTP_SERVER, int(config.FTP_PORT))
        ftp.login(config.FTP_USERNAME, config.FTP_PASSWORD)

        # Change to the desired directory
        try:
            ftp.cwd(path)
        except:
            ftp.mkd(path)  # Create directory if it doesn't exist
            ftp.cwd(path)

        # Open the file and upload
        with open(f"{save_path}/{filename}", 'rb') as f:  # 使用完整路径打开文件
            ftp.storbinary(f"STOR {filename}", f)

        # Close the connection
        ftp.quit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


