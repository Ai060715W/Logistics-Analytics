"""Main runner for LogiInsight skeleton."""


def main():
    print("干线运输价格分析示例")
    import pandas as pd
    from src.data_processing.data_loader import load_csv
    from src.analysis.cost_analysis import (
        analyze_price_trend, analyze_price_change, generate_price_suggestion,
        plot_price_bar, plot_price_pie, plot_price_donut, plot_price_hist
    )
    from src.analysis.dashboard_generator import generate_dashboard
    # 以 1_clean.csv 为例
    try:
        df = pd.read_csv('data/processed/1_clean.csv', encoding='utf-8')
        trend = analyze_price_trend(df)
        pct_change = analyze_price_change(df)
        suggestion = generate_price_suggestion(trend, pct_change)
        # 生成图表
        bar_path = plot_price_bar(df)
        pie_path = plot_price_pie(df)
        donut_path = plot_price_donut(df)
        hist_path = plot_price_hist(df)
        # 自动生成报告
        with open('docs/ANALYSIS_REPORT.md', 'w', encoding='utf-8') as f:
            f.write('# 自动化分析报告\n\n')
            f.write('## 价格分析结论\n')
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
            
            # 生成交互式数据看板
            dashboard_path = generate_dashboard(df)
            f.write('\n## 交互式数据看板\n')
            f.write(f'- 交互式看板：{dashboard_path}\n')
            f.write('\n（可直接在浏览器中打开查看）\n')
            
        print("分析报告已生成：docs/ANALYSIS_REPORT.md")
        print(f"交互式数据看板已生成：{dashboard_path}")
    except Exception as e:
        print("数据分析失败:", e)


if __name__ == '__main__':
    main()
