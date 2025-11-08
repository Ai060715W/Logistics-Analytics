# LogiInsight - 智能物流数据分析平台

## 📊 项目概述
🚚 一个端到端的物流数据分析与可视化项目，
从原始业务数据出发，自动完成清洗、特征构建、成本与效率分析，
并生成可交互仪表板与运营优化建议报告。

---

## 📦 项目背景
在现代物流运营中，如何通过数据驱动来优化运输成本、提升配送效率，是企业竞争力的关键。
Logistics-Analytics 致力于构建一个自动化的数据分析流程，从原始业务数据出发，快速获得可执行的运营洞察。

---

## 🚀 主要功能  
- 📊 **成本分析**：按仓储、干线、末端配送等维度拆解成本结构  
- 📍 **区域表现分析**：比较不同区域的运输效率与盈利情况  
- 🧹 **数据清洗与特征工程**：自动处理缺失值、异常值与指标标准化  
- 📈 **可视化仪表板**：基于 Plotly 生成交互式运营看板（`outputs/dashboard.html`）  
- 📑 **报告与洞察输出**：自动生成报告文档（`docs/ANALYSIS_REPORT.md`、`docs/INSIGHTS.md`）  
- 🔁 **模块化分析流程**：从数据导入 → 清洗 → 分析 → 输出的完整自动化管线  

---

## 🛠 技术栈
| 类别 | 工具 / 框架 |
|------|--------------|
| 语言 | Python 3.8+，CSS3，HTML5，JavaScript (ES6) |
| 数据处理 | Pandas, NumPy |
| 可视化 | Matplotlib, Plotly |
| 存储 | CSV |
| 其他 | OS, Logging, argparse |

---

## 📁 项目结构
```
Logistics-Analytics/
├── src/
│   ├── data_processing/
│   │   ├── data_loader.py         # 数据加载模块，负责从CSV文件读取原始数据
│   │   ├── data_cleaner.py        # 数据清洗模块，处理数据缺失、异常值等
│   │   └── feature_engineer.py    # 特征工程模块，提取和创建分析所需特征
│   ├── analysis/
│   │   ├── cost_analysis.py       # 成本分析模块，实现价格趋势分析和图表生成
│   │   ├── dashboard_generator.py # 交互式看板生成模块，创建可视化数据面板
│   │   └── regional_analysis.py   # 区域分析模块，提供基础区域统计功能
├── data/
│   ├── raw/
│   │   ├── 1.csv
│   │   ├── 2.csv
│   │   └── 3.csv
│   │  
│   ├── processed/
│   │   ├── 1_clean.csv
│   │   ├── 2_clean.csv
│   │   └── 3_clean.csv
├── docs/
│   ├── ANALYSIS_REPORT.md         # 生成的分析报告文档
│   └── INSIGHTS.md                # 运营洞察和优化建议文档
├── outputs/
│   ├── price_bar.png              # 价格柱状图可视化结果
│   ├── price_donut.png            # 价格环形图可视化结果
│   ├── price_hist.png             # 价格直方图可视化结果
│   └── price_pie.png              # 价格饼图可视化结果
├── static
│   ├── dashboard.js               # 主逻辑脚本：负责读取数据、处理数据与绘制 Plotly 图表
│   ├── plotly-2.30.0.min.js       # Plotly.js 可视化库（离线版），主要用于绘制交互式图表（可缩放、悬浮提示、导出图像）
│   └── style.css                  # 负责仪表板布局（如网格、卡片阴影、边框、背景）
├── requirements.txt               # 项目依赖包配置文件
├── main.py                        # 项目主入口，协调各模块执行数据分析流程
├── clean_and_save.py              # 数据清洗与保存脚本
├── dashboard.html                 # 交互式数据可视化看板
└── README.md                      # 项目说明文档
```

---

## ⚙️ 快速开始

### 1️⃣ 克隆项目
```bash
git clone https://github.com/Ai060715W/Logistics-Analytics
cd Logistics-Analytics
```

### 2️⃣ 安装依赖
```bash
pip install -r requirements.txt
```

### 3️⃣ 运行主程序
```bash
python main.py
```

### 4️⃣ 安装 Live Server 插件

- 打开 VS Code
- 左侧点击 扩展（Extensions） 图标
- 搜索 Live Server
- 安装 Ritwick Dey 的版本

### 5️⃣ 查看结果
- 分析报告：`docs/ANALYSIS_REPORT.md`
- 洞察建议：`docs/INSIGHTS.md`
- 图表输出：`outputs/charts/`
- 可视化仪表板：`dashboard.html`
  打开 `dashboard.html`文件  
  右键选择**“Open with Live Server”** 或点击右下角**“Go Live”**按钮

---

## 📊 数据说明
- 输入数据：放置于 `data/raw/` 目录下（CSV格式）
- 输出数据：程序运行后自动生成 `data/processed/`

---

## 📝 字段示例  

| 字段名 | 英文名 | 数据类型 | 示例值 | 说明 |
|--------|----------|-----------|--------|------|
| 运输方式 | `transport_mode` | string | `Air` | 订单使用的运输方式（如：Air, Sea, Truck） |
| 路线 | `route` | string | `Shanghai → Beijing` | 货物运输的起止路线 |
| 价格 | `price` | float | `560.75` | 当前周期的运输单价（元） |
| 环比 | `month_over_month` | float | `+3.8%` | 与上月相比的价格变化百分比 |
| 日期 | `date` | date | `2025-10-15` | 数据记录日期 |
| 价格数值 | `price_value` | float | `560.75` | 价格的数值化字段（用于计算与可视化） |

---

## 🗂️ 项目依赖
```txt
# 数据处理与计算
pandas>=1.5.0
numpy>=1.21.0
scipy>=1.7.0

# 可视化分析
plotly>=5.10.0
matplotlib>=3.5.0

# 时间日期处理
python-dateutil>=2.8.0
```
---

## 🤝 贡献
欢迎通过以下方式参与贡献：
- 提交 Issue 报告问题
- 提交 Pull Request 改进功能
- 优化算法、文档或可视化效果

---

## 📑 License
本项目采用 MIT License — 详情见 [LICENSE](LICENSE) 文件。

---

## 👨‍💻 作者
Author: Ai060715W
📫 GitHub: [@Ai060715W](https://github.com/Ai060715W)
---
