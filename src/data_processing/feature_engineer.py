"""feature_engineer.py

Placeholder for feature engineering helpers.
"""


def create_features(df):
    """Create features from raw dataframe.

    Args:
        df: input data

    Raises:
        NotImplementedError
    """
    raise NotImplementedError("Implement feature engineering")


def extract_order_features(df):
    """订单量相关特征工程。"""
    raise NotImplementedError("实现订单量特征工程")


def extract_region_features(df):
    """区域分布相关特征工程。"""
    raise NotImplementedError("实现区域分布特征工程")


def extract_cost_features(df):
    """物流成本相关特征工程。"""
    raise NotImplementedError("实现物流成本特征工程")
