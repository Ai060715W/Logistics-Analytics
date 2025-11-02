"""data_loader.py

Placeholder functions for loading data.
"""

import pandas as pd


def load_csv(path):
    """加载通用CSV数据，返回DataFrame。"""
    return pd.read_csv(path)


def load_warehouse_data(path):
    """加载仓储环节数据。"""
    df = pd.read_csv(path)
    # 可在此处添加仓储专属预处理
    return df


def load_trunkline_data(path):
    """加载干线运输数据。"""
    df = pd.read_csv(path)
    # 可在此处添加干线专属预处理
    return df


def load_delivery_data(path):
    """加载配送环节数据。"""
    df = pd.read_csv(path)
    # 可在此处添加配送专属预处理
    return df
