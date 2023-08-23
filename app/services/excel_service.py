# Excel文件生成服务
import pandas as pd

def save_results_to_excel(results, filename):
    df = pd.DataFrame(results)
    df.to_excel(filename, index=False)

