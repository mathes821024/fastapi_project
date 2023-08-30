# FastAPI应用的主入口
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  # <-- 新添加的导入
from app.services.oracle_service import fetch_and_process_data


import os
import datetime
import logging


# 只是显示日志到终端,并没有进行日志落盘
#logging.basicConfig(level=logging.INFO)


# 获取当前日期
current_date = datetime.datetime.now().strftime('%Y%m%d')

# 获取 HOME 环境变量
home_path = os.getenv("HOME")

# 构建日志文件名
log_filename = f"{home_path}/log/fastapi_project_app{current_date}.log"

logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(funcName)s] [%(thread)d]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = FastAPI()

# 创建一个新的Pydantic模型来描述接收的JSON数据
class Message(BaseModel):
    msg_type: str
    data: str


@app.post("/api/process/")
async def process_message(message: Message):
    try:
        msg_type = message.msg_type
        data = message.data
        logging.info(f"Received {msg_type} message with data: {data}")

        if msg_type == "transaction":
            date = data  # 假设 data 是一个日期字符串
            await fetch_and_process_data(date)
            logging.info(f"Processed transaction with data: {data}")
            return {"status": "success", "message": "Transaction processed successfully"}

        elif msg_type == "reconciliation":
            logging.info(f"Processed reconciliation with data: {data}")
            return {"status": "success", "message": "Reconciliation processed successfully"}

        else:
            raise HTTPException(status_code=400, detail="Unknown message type")

    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        return {"status": "error", "message": str(e)}



# 启动项目:uvicorn fastapi_project.main:app --reload
# uvicorn fastapi_project.main:app --reload --port 8000
# uvicorn app.main:app --reload --port 8000


