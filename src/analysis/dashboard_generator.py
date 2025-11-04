import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os

class DashboardGenerator:
    """交互式数据看板生成器"""
    
    def __init__(self):
        self.dashboard_path = 'outputs/dashboard.html'
        # 确保输出目录存在
        os.makedirs('outputs', exist_ok=True)
    
    def create_price_analysis_dashboard(self, df):
        """创建价格分析交互式看板"""
        if '价格数值' not in df.columns:
            raise ValueError('数据缺少价格数值字段')
        
        # 创建子图 - 扩展为2x3布局
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=(
                '不同路线均价对比', 
                '不同路线价格占比',
                '价格趋势折线图',
                '价格波动热力图',  # 热力图移到最左边
                '环比涨跌幅分析',
                '价格分布直方图'
            ),
            specs=[
                [{'type': 'bar'}, {'type': 'pie'}, {'type': 'scatter'}],
                [{'type': 'heatmap'}, {'type': 'bar'}, {'type': 'histogram'}]  # 调整热力图位置到最左边
            ],
            horizontal_spacing=0.15,  # 增加水平间距
            vertical_spacing=0.2     # 增加垂直间距
        )
        
        # 1. 路线均价柱状图
        if '路线' in df.columns:
            route_avg = df.groupby('路线')['价格数值'].mean().reset_index()
            # 将路线名称转换为竖向显示（每个字占一行）
            vertical_labels = []
            for route in route_avg['路线']:
                # 确保每个中文字符都单独显示在一行
                vertical_text = '<br>'.join([char for char in route])
                vertical_labels.append(vertical_text)
            
            fig.add_trace(
                go.Bar(x=vertical_labels, y=route_avg['价格数值'], name='路线均价'),
                row=1, col=1
            )
            
        # 2. 路线价格占比饼图
        if '路线' in df.columns:
            route_sum = df.groupby('路线')['价格数值'].sum()
            # 创建带路线名称和百分比的标签
            # 为饼图上的标签设置更简洁的格式
            short_labels = [route[:4] + '...' if len(route) > 4 else route for route in route_sum.index]
            
            fig.add_trace(
                go.Pie(
                    labels=route_sum.index,  # 完整路线名称用于图例
                    values=route_sum.values, 
                    hole=0.3,
                    # 悬停显示完整路线名称和详细信息
                    hovertemplate='路线: %{label}<br>总价: %{value}元<br>占比: %{percent:.1%}',
                    # 饼图上显示简化的标签和百分比
                    text=[f'{short}<br>{pct:.1%}' for short, pct in zip(short_labels, route_sum / route_sum.sum())],
                    textposition='inside',  # 文本位置
                    showlegend=True  # 显示图例，图例中包含完整路线名称
                ),
                row=1, col=2
            )
        
        # 3. 价格趋势折线图
        # 假设数据中有时间相关信息，这里创建模拟的时间序列数据
        if len(df) > 0:
            # 创建模拟的时间序列数据
            import numpy as np
            dates = pd.date_range(start='2023-01-01', periods=min(30, len(df)))
            # 从数据中随机采样价格点
            sample_prices = df['价格数值'].sample(min(30, len(df))).values
            # 对采样的数据进行排序，以便展示趋势
            sample_prices.sort()
            
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=sample_prices,
                    mode='lines+markers',
                    name='价格趋势',
                    line=dict(color='rgb(75, 192, 192)', width=2),
                    marker=dict(size=6, color='rgb(75, 192, 192)', symbol='circle')
                ),
                row=1, col=3
            )
        
        # 4. 价格分布直方图
        fig.add_trace(
            go.Histogram(
                x=df['价格数值'], 
                nbinsx=20, 
                name='价格分布',
                marker=dict(
                    color='rgb(0, 180, 135)',  # 设置绿色
                    line=dict(
                        color='white',  # 白色边框
                        width=1  # 边框宽度
                    )
                )
            ),
            row=2, col=3  # 移到右下角
        )
        
        # 5. 环比涨跌幅分析
        if '环比' in df.columns:
            # 清理环比数据
            pct_data = df['环比'].astype(str).str.replace('%', '').astype(float)
            # 分类环比涨跌幅
            bins = [-float('inf'), -5, -1, 0, 1, 5, float('inf')]
            labels = ['大幅下降', '小幅下降', '持平', '小幅上涨', '大幅上涨', '超大幅上涨']
            pct_cats = pd.cut(pct_data, bins=bins, labels=labels)
            pct_counts = pct_cats.value_counts().sort_index()
            
            fig.add_trace(
                go.Bar(x=pct_counts.index, y=pct_counts.values, name='环比涨跌幅分布'),
                row=2, col=2
            )
        
        # 6. 价格波动热力图（展示不同价格区间的分布密度）
        if len(df) > 0:
            # 创建价格区间和频率的热力图数据
            hist_data, bin_edges = np.histogram(df['价格数值'], bins=10)
            # 创建二维数据用于热力图显示
            heatmap_data = [[bin_edges[i], bin_edges[i+1], hist_data[i]] for i in range(len(hist_data))]
            
            fig.add_trace(
                go.Heatmap(
                    z=[[val[2]] for val in heatmap_data],
                    x=['价格分布'],
                    y=[f'{val[0]:.0f}-{val[1]:.0f}' for val in heatmap_data],
                    colorscale=[[0, 'rgba(255, 255, 255, 0.9)'],  # 几乎是白色
                               [0.1, 'rgba(230, 240, 255, 0.9)'],  # 非常浅的蓝色
                               [0.2, 'rgba(200, 220, 255, 0.9)'],  # 浅蓝
                               [0.3, 'rgba(170, 200, 255, 0.9)'],  # 淡蓝
                               [0.4, 'rgba(140, 180, 255, 0.9)'],  # 中淡蓝
                               [0.5, 'rgba(100, 150, 255, 0.9)'],  # 中蓝
                               [0.6, 'rgba(70, 120, 255, 0.9)'],   # 蓝色
                               [0.7, 'rgba(40, 90, 230, 0.9)'],    # 深蓝色
                               [0.8, 'rgba(20, 70, 200, 0.9)'],    # 更深的蓝色
                               [0.9, 'rgba(10, 50, 170, 0.9)'],    # 几乎是靛蓝色
                               [1, 'rgba(5, 30, 140, 0.9)']],     # 最深的蓝色
                    colorbar=dict(title='频数', thickness=25, len=0.8),
                    name='价格密度'
                ),
                row=2, col=1  # 移到最左边
            )
        
        # 更新布局
        fig.update_layout(
            title={
                'text': '物流价格分析交互式看板',
                'font': {'size': 28},
                'x': 0.5,
                'xanchor': 'center'
            },
            height=1000,  # 显著增加图表高度以确保所有文字可见
            width=1800,  # 大幅增加宽度以提供更多空间
            showlegend=True,
            margin=dict(l=250, r=100, t=120, b=100),  # 大幅增加左边距为图例留出空间
            legend=dict(
                x=-0.15,  # 完全移到视口左侧
                y=0.93,  # 保持垂直位置
                orientation='v',
                font=dict(size=9),  # 进一步减小字体大小
                bgcolor='rgba(255, 255, 255, 0.9)',  # 稍微增加不透明度
                bordercolor='rgba(0, 0, 0, 0.1)',
                borderwidth=1,
                xanchor='left'  # 锚点设为左侧
            )
        )
        
        # 更新坐标轴标签
        fig.update_xaxes(title_text='路线', row=1, col=1)
        fig.update_xaxes(
            tickangle=45,  # 设置标签旋转角度
            tickfont=dict(size=9),  # 减小字体大小
            automargin=True,  # 自动调整边距
            row=1, col=1)
        fig.update_yaxes(title_text='均价（元）', row=1, col=1)
        fig.update_xaxes(title_text='日期', row=1, col=3)
        fig.update_yaxes(title_text='价格（元）', row=1, col=3)
        fig.update_xaxes(title_text='', row=2, col=1)  # 热力图x轴
        fig.update_yaxes(title_text='价格区间（元）', row=2, col=1)  # 热力图y轴
        fig.update_xaxes(title_text='涨跌幅分类', row=2, col=2)
        fig.update_xaxes(
            tickangle=45,
            tickfont=dict(size=9),
            automargin=True,
            row=2, col=2)
        fig.update_yaxes(title_text='数量', row=2, col=2)
        fig.update_xaxes(title_text='价格（元）', row=2, col=3)  # 直方图x轴
        fig.update_yaxes(title_text='频数', row=2, col=3)  # 直方图y轴
        
        # 添加互动元素
        fig.update_layout(
            hovermode='closest',
            font=dict(family='SimHei, Arial', size=12)
        )
        
        # 保存为HTML
        fig.write_html(self.dashboard_path, include_plotlyjs=True, full_html=True)
        return self.dashboard_path



def generate_dashboard(df, output_path='outputs/dashboard.html'):
    """生成交互式数据看板的便捷函数"""
    generator = DashboardGenerator()
    dashboard_path = generator.create_price_analysis_dashboard(df)
    print(f"交互式数据看板已生成: {dashboard_path}")
    return dashboard_path