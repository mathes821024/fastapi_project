# Excel文件生成服务
#excel_service.py
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def save_results_to_excel(results, filename):
    df = pd.DataFrame(results)
    df.to_excel(filename, index=False)
    print(df)
    #logger.info(df)
    logger.info(f"DataFrame shape: {df.shape}, columns: {df.columns.tolist()}")


