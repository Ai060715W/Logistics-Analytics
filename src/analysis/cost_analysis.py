import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
font_manager.fontManager.addfont('C:/Windows/Fonts/simhei.ttf')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
import pandas as pd
def plot_price_bar(df, out_path='outputs/price_bar.png'):
    """不同运输方式或路线的均价柱状图，带数值标注"""
    if '路线' in df.columns and '价格数值' in df.columns:
        mean_price = df.groupby('路线')['价格数值'].mean()
        # 增加图表宽度，调整高度比例
        plt.figure(figsize=(14, 6))
        bars = plt.bar(mean_price.index, mean_price.values, color='skyblue', label='均价')
        for bar in bars:
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{bar.get_height():.0f}', 
                     ha='center', va='bottom', fontsize=9)
        plt.title('不同路线均价柱状图')
        plt.xlabel('路线')
        plt.ylabel('均价（元）')
        plt.legend()
        # 旋转x轴标签以避免重叠
        plt.xticks(rotation=45, ha='right', fontsize=10)
        # 增加底部边距以容纳旋转的标签
        plt.subplots_adjust(bottom=0.2)
        plt.savefig(out_path, bbox_inches='tight')
        plt.close()
        return out_path
def plot_price_pie(df, out_path='outputs/price_pie.png'):
    """不同路线价格占比饼状图，带数值和百分比"""
    if '路线' in df.columns and '价格数值' in df.columns:
        price_sum = df.groupby('路线')['价格数值'].sum()
        plt.figure(figsize=(7,7))
        def autopct(pct):
            total = price_sum.sum()
            val = int(round(pct*total/100.0))
            return f'{pct:.1f}%\n{val}元'
        plt.pie(price_sum, labels=price_sum.index, autopct=autopct, startangle=90)
        plt.title('不同路线价格占比饼状图')
        plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
        return out_path
def plot_price_donut(df, out_path='outputs/price_donut.png'):
    """环比涨跌幅环形图，带数值和百分比，美化版"""
    if '环比' in df.columns:
        pct = df['环比'].astype(str).str.replace('%','').astype(float)
        # 调整分类区间，使分类更合理
        bins = [-np.inf, -5, -1, 0, 1, 5, np.inf]
        labels = ['大幅下降', '小幅下降', '持平', '小幅上涨', '大幅上涨', '超大幅上涨']
        cats = pd.cut(pct, bins=bins, labels=labels)
        counts = cats.value_counts().sort_index()
        
        # 创建图表，增大尺寸
        plt.figure(figsize=(8, 8))
        
        # 定义颜色方案，确保与图例顺序一致
        # 按照标签顺序设置对应的颜色
        color_map = {
            '大幅下降': '#ff6b6b',   # 红色
            '小幅下降': '#ffd166',   # 黄色
            '持平': '#06d6a0',       # 绿色
            '小幅上涨': '#118ab2',    # 蓝色
            '大幅上涨': '#073b4c',    # 深蓝色
            '超大幅上涨': '#8338ec'   # 紫色
        }
        # 根据实际出现的类别排序颜色列表
        colors = [color_map[cat] for cat in counts.index]
        
        # 自定义百分比和数值显示
        def autopct(pct):
            total = counts.sum()
            val = int(round(pct*total/100.0))
            return f'{pct:.1f}%\n{val}次'
        
        # 创建环形图，添加边框效果
        wedges, texts, autotexts = plt.pie(
            counts, 
            labels=None,  # 不直接显示标签，通过图例显示
            autopct=autopct,
            wedgeprops=dict(
                width=0.3,  # 环形宽度
                edgecolor='white',  # 白色边框
                linewidth=2,  # 边框宽度
                alpha=0.95  # 稍微降低透明度以获得更好的视觉效果
            ), 
            startangle=90,
            colors=colors,
            explode=[0.05]*len(counts),  # 略微分离各个扇形以增强视觉效果
            textprops={'fontsize': 11, 'fontweight': 'bold'},
            shadow=True  # 在pie函数级别添加阴影效果
        )
        
        # 设置自动文本颜色为黑色以提高可读性
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_weight('bold')
            autotext.set_fontsize(10)
        
        # 设置更美观的标题
        plt.title(
            '环比涨跌幅环形图分析', 
            fontsize=16, 
            fontweight='bold',
            pad=20
        )
        
        # 自定义图例，放在环形图右侧
        plt.legend(
            wedges, 
            counts.index, 
            title="涨跌幅类型",
            loc="center left", 
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=10,
            title_fontsize=12,
            frameon=True,
            framealpha=0.9,
            edgecolor='gray'
        )
        
        # 添加中心文本，显示总数
        plt.figtext(0.5, 0.5, f'总计\n{counts.sum()}次', 
                    ha='center', va='center', fontsize=14, fontweight='bold')
        
        # 调整布局，确保图例和文本不会被截断
        plt.tight_layout()
        
        # 保存图片，设置更高的DPI
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        plt.close()
        return out_path
def plot_price_hist(df, out_path='outputs/price_hist.png'):
    """价格分布直方图，带数值标注"""
    if '价格数值' in df.columns:
        plt.figure(figsize=(10,5))
        n, bins, patches = plt.hist(df['价格数值'], bins=20, color='skyblue', edgecolor='black', label='价格分布')
        for i in range(len(n)):
            plt.text((bins[i]+bins[i+1])/2, n[i], f'{int(n[i])}', ha='center', va='bottom', fontsize=8)
        plt.title('价格分布直方图')
        plt.xlabel('价格（元）')
        plt.ylabel('频数')
        plt.legend()
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
        return out_path

"""干线运输价格与成本分析模块"""



def analyze_price_trend(df):
    """分析价格趋势，返回均值、最大、最小、最新价格。"""
    price_col = '价格数值'
    if price_col not in df.columns:
        raise ValueError('缺少价格数值字段')
    trend = {
        'mean_price': df[price_col].mean(),
        'max_price': df[price_col].max(),
        'min_price': df[price_col].min(),
        'latest_price': df[price_col].iloc[0] if len(df) > 0 else None
    }
    return trend

def analyze_price_change(df):
    """统计环比涨跌幅均值。"""
    if '环比' not in df.columns:
        return None
    # 去掉百分号并转为 float
    pct = df['环比'].astype(str).str.replace('%','').astype(float)
    return pct.mean()

def generate_price_suggestion(trend, pct_change):
    """根据价格趋势和环比均值生成建议。"""
    if pct_change is not None and pct_change < 0:
        return '近期价格呈下降趋势，可考虑增加运输批次或议价。'
    elif pct_change is not None and pct_change > 0:
        return '近期价格有上涨趋势，建议提前锁定合同价格。'
    else:
        return '价格稳定，无需特别调整。'


def analyze_warehouse_cost(data):
    """仓储环节成本分析。输入DataFrame，输出总成本和分项。"""
    # 假设有 'storage_cost' 列
    total = data['storage_cost'].sum() if 'storage_cost' in data else 0
    return {'total_warehouse_cost': total}


def analyze_trunkline_cost(data):
    """干线运输成本分析。输入DataFrame，输出总成本和分项。"""
    total = data['trunkline_cost'].sum() if 'trunkline_cost' in data else 0
    return {'total_trunkline_cost': total}


def analyze_delivery_cost(data):
    """配送环节成本分析。输入DataFrame，输出总成本和分项。"""
    total = data['delivery_cost'].sum() if 'delivery_cost' in data else 0
    return {'total_delivery_cost': total}


def evaluate_solution_performance(data):
    """评估方案上线后的运营表现。"""
    raise NotImplementedError("实现方案运营表现评估")


def generate_optimization_suggestions(data):
    """输出运营优化建议。"""
    raise NotImplementedError("实现优化建议输出")


def generate_optimization_suggestions(costs):
    """根据成本分析结果输出优化建议。"""
    suggestions = []
    if costs.get('total_warehouse_cost', 0) > 100000:
        suggestions.append('仓储成本偏高，建议优化库存管理和仓库布局。')
    if costs.get('total_trunkline_cost', 0) > 100000:
        suggestions.append('干线运输成本偏高，建议优化线路和运输批次。')
    if costs.get('total_delivery_cost', 0) > 100000:
        suggestions.append('配送成本偏高，建议优化配送路径和车辆调度。')
    if not suggestions:
        suggestions.append('各环节成本合理，无需优化。')
    return suggestions

def generate_operational_insights(df):
    """根据数据生成运营洞察"""
    insights = []
    if '价格数值' in df.columns:
        avg_price = df['价格数值'].mean()
        if avg_price > 1000:
            insights.append("平均价格较高，表明部分线路存在潜在议价空间。")
        else:
            insights.append("整体价格水平合理，维持当前运输策略。")
    if '路线' in df.columns:
        top_routes = df['路线'].value_counts().head(3).index.tolist()
        insights.append(f"高频运输路线包括：{', '.join(top_routes)}。")
    insights.append("建议持续监控价格波动与区域差异，优化运输组合。")
    return insights


def generate_risk_assessment(df):
    """生成风险评估洞察"""
    risks = []
    if '环比' in df.columns:
        pct = df['环比'].astype(str).str.replace('%', '').astype(float)
        high_volatility = (pct.abs() > 10).mean()
        if high_volatility > 0.3:
            risks.append("价格波动显著，短期存在运输成本上升风险。")
        else:
            risks.append("价格波动较小，运输成本稳定。")
    else:
        risks.append("数据缺少环比字段，无法评估价格波动风险。")
    risks.append("需关注燃油价格及政策调整带来的潜在影响。")
    return risks


def generate_strategy_suggestions(df):
    """生成策略建议"""
    strategies = []
    strategies.append("建立运输价格监控系统，实现动态调价。")
    strategies.append("与核心干线承运商建立长期合作关系，稳定价格。")
    strategies.append("探索多式联运或区域整合，提升整体运输效率。")
    return strategies
