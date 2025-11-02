import pandas as pd
import os
from src.data_processing.data_cleaner import clean_cost_data

files = ['1.csv', '2.csv', '3.csv']
src = 'data/external/'
dst = 'data/processed/'
os.makedirs(dst, exist_ok=True)

for i, f in enumerate(files, 1):
    fp = os.path.join(src, f)
    if os.path.exists(fp):
        df = pd.read_csv(fp, encoding='gbk')
        df_clean = clean_cost_data(df)
        out = os.path.join(dst, f'{i}_clean.csv')
        df_clean.to_csv(out, index=False, encoding='utf-8')
        print(f'Cleaned: {out}')
print('Done')
