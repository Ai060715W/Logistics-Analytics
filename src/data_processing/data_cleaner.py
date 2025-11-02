"""data_cleaner.py

Placeholder for data cleaning utilities.
"""

import pandas as pd


def clean_dataframe(df):
    """通用数据清洗：去重、缺失值填充。"""
    df = df.drop_duplicates()
    df = df.fillna(method='ffill').fillna(method='bfill')
    return df


def clean_order_data(df):
    """订单数据清洗：日期格式转换、数值字段处理。"""
    if '日期' in df.columns:
        df['日期'] = pd.to_datetime(df['日期'], errors='coerce')
    # 假设有订单量字段
    if '订单量' in df.columns:
        df['订单量'] = pd.to_numeric(df['订单量'], errors='coerce')
    return df


def clean_region_data(df):
    """区域分布数据清洗：标准化区域名。"""
    if '区域' in df.columns:
        df['区域'] = df['区域'].str.strip().str.upper()
    return df


def clean_cost_data(df):
    """成本数据清洗：价格字段提取和数值化。"""
    import re
    if '价格' in df.columns:
        # 提取数字部分
        df['价格数值'] = df['价格'].apply(lambda x: float(re.findall(r'[\d.]+', str(x))[0]) if re.findall(r'[\d.]+', str(x)) else None)
    if '涨跌幅' in df.columns:
        df['涨跌幅'] = df['涨跌幅'].str.replace('%','').astype(float)
    return df
