# FastAPI应用的主入口
from fastapi import FastAPI
from app.services import zeromq_service, oracle_service, excel_service, ftp_service


app = FastAPI()

@app.get("/generate_report/")
async def generate_report(merchant_id: str, settlement_date: str):
    results = oracle_service.query_oracle_database(merchant_id, settlement_date)
    filename = f"report_{merchant_id}_{settlement_date}.xlsx"
    excel_service.save_results_to_excel(results, filename)
    await ftp_service.send_file_to_ftp_server(filename)
    return {"status": "success", "message": "Report generated and sent successfully!"}

# 启动项目:uvicorn fastapiMyToolWeb.main:app --reload

