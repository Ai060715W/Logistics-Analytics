# LogiInsight - 物流运营智能分析平台

## 📊 项目概述
基于真实物流业务场景的数据分析系统，提供端到端的物流运营洞察和优化建议。

## 🚀 功能特性
- **成本分析**: 仓储、干线、配送各环节成本拆解
- **绩效评估**: 准时率、时效性、服务质量分析  
- **区域洞察**: 订单分布、区域效率热力图
- **自动化报告**: 一键生成业务洞察报告

## 🛠 技术栈
- Python 3.8+
- Pandas, NumPy (数据处理)
- Plotly, Matplotlib (可视化)
- SQLite (数据存储)

## 📁 项目结构
```
logistics-analytics/
├── src/
│   ├── data_processing/
│   │   ├── data_loader.py
│   │   ├── data_cleaner.py
│   │   └── feature_engineer.py
│   ├── analysis/
│   │   ├── cost_analysis.py
│   │   ├── delivery_performance.py
│   │   └── regional_analysis.py
│   ├── visualization/
│   │   ├── charts_generator.py
│   │   └── dashboard.py
│   └── utils/
│       ├── config.py
│       └── helpers.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
├── docs/
│   ├── ANALYSIS_REPORT.md
│   ├── METHODOLOGY.md
│   └── INSIGHTS.md
├── tests/
├── requirements.txt
├── main.py
└── README.md
```

## 🏃 快速开始
```bash
# 安装依赖
pip install -r requirements.txt

# 运行分析
python main.py

📈 输出成果
自动化分析报告 (docs/ANALYSIS_REPORT.md)

交互式数据看板 (outputs/dashboard.html)

运营优化建议 (docs/INSIGHTS.md)
```

## 📁 项目依赖
```txt
pandas>=1.5.0
numpy>=1.21.0
plotly>=5.10.0
matplotlib>=3.5.0
sqlalchemy>=1.4.0
scipy>=1.7.0
python-dateutil>=2.8.0
