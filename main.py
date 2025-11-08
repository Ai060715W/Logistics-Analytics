"""Main runner for LogiInsight skeleton - 自动清洗并分析数据 + 生成运营洞察报告"""

import os
import pandas as pd
from src.data_processing.data_cleaner import clean_cost_data
from src.data_processing.data_loader import load_csv
from src.analysis.cost_analysis import (
    analyze_price_trend, analyze_price_change, generate_price_suggestion,
    plot_price_bar, plot_price_pie, plot_price_donut, plot_price_hist,
    generate_operational_insights, generate_risk_assessment, generate_strategy_suggestions
)


def clean_and_save():
    """清洗原始数据并保存到 data/processed/"""
    print("开始清洗原始数据...")
    files = ['1.csv', '2.csv', '3.csv']
    src = 'data/raw/'
    dst = 'data/processed/'
    os.makedirs(dst, exist_ok=True)

    for i, f in enumerate(files, 1):
        fp = os.path.join(src, f)
        print(f"Checking: {fp}")
        if os.path.exists(fp):
            print(f"Found: {fp}")
            try:
                df = pd.read_csv(fp, encoding='gbk')
                print(f"Loaded {len(df)} rows from {fp}")

                df_clean = clean_cost_data(df)
                print(f"Cleaned type: {type(df_clean)}")

                out = os.path.join(dst, f'{i}_clean.csv')
                df_clean.to_csv(out, index=False, encoding='utf-8')
                print(f"Saved cleaned file to: {out}")

            except Exception as e:
                print(f"Error processing {fp}: {e}")
        else:
            print(f"File not found: {fp}")
    print("数据清洗完成。")


def main():
    print("干线运输价格分析示例（自动清洗并合并三个清洗后数据表）")

    try:
        # === 1. 自动清洗原始数据 ===
        clean_and_save()

        # === 2. 读取清洗后的文件并合并 ===
        files = [
            'data/processed/1_clean.csv',
            'data/processed/2_clean.csv',
            'data/processed/3_clean.csv'
        ]
        dfs = []
        for f in files:
            try:
                df_temp = pd.read_csv(f, encoding='utf-8')
                dfs.append(df_temp)
                print(f"Loaded: {f} ({len(df_temp)} rows)")
            except FileNotFoundError:
                print(f"Warning: {f} not found, skipped.")

        if not dfs:
            raise FileNotFoundError("No cleaned CSV files found in data/processed/")

        df = pd.concat(dfs, ignore_index=True)
        print(f"Total combined rows: {len(df)}")

        # === 3. 分析价格趋势 ===
        trend = analyze_price_trend(df)
        pct_change = analyze_price_change(df)
        suggestion = generate_price_suggestion(trend, pct_change)

        # === 4. 生成分析图表 ===
        bar_path = plot_price_bar(df)
        pie_path = plot_price_pie(df)
        donut_path = plot_price_donut(df)
        hist_path = plot_price_hist(df)

        # === 5. 生成分析报告 ANALYSIS_REPORT.md ===
        os.makedirs("docs", exist_ok=True)
        with open('docs/ANALYSIS_REPORT.md', 'w', encoding='utf-8') as f:
            f.write('# 自动化分析报告\n\n')
            f.write('## 价格分析结论（合并数据）\n')
            f.write(f'- 数据总行数：{len(df)}\n')
            f.write(f'- 均价：{trend["mean_price"]:.2f} 元\n')
            f.write(f'- 最大价：{trend["max_price"]:.2f} 元\n')
            f.write(f'- 最小价：{trend["min_price"]:.2f} 元\n')
            f.write(f'- 最新价：{trend["latest_price"]:.2f} 元\n')
            f.write(f'- 环比均值：{pct_change:.2f}%\n')
            f.write(f'- 优化建议：{suggestion}\n\n')
            f.write('## 图表说明\n')
            f.write(f'- 柱状图：{bar_path}\n')
            f.write(f'- 饼状图：{pie_path}\n')
            f.write(f'- 环形图：{donut_path}\n')
            f.write(f'- 价格分布直方图：{hist_path}\n')
            f.write('\n（可在 outputs 文件夹查看图片）\n')

        print("分析报告已生成：docs/ANALYSIS_REPORT.md")

        # === 6. 新增：生成运营洞察报告 INSIGHTS.md ===
        insights = generate_operational_insights(df)
        risks = generate_risk_assessment(df)
        strategies = generate_strategy_suggestions(df)

        with open('docs/INSIGHTS.md', 'w', encoding='utf-8') as f:
            f.write('# 运营洞察报告 (INSIGHTS)\n\n')
            f.write('## 一、运营洞察\n')
            for item in insights:
                f.write(f'- {item}\n')
            f.write('\n## 二、风险评估\n')
            for item in risks:
                f.write(f'- {item}\n')
            f.write('\n## 三、策略建议\n')
            for item in strategies:
                f.write(f'- {item}\n')

        print("运营洞察报告已生成：docs/INSIGHTS.md")

    except Exception as e:
        print("数据分析失败:", e)


if __name__ == '__main__':
    main()
