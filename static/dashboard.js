/* 美化版 dashboard.js */

const CSV_FIELD_ROUTE = ['路线', 'route'][0];
const CSV_FIELD_PRICE = ['价格', 'price'][0];
const CSV_FIELD_RATIO = ['环比', 'ratio'][0];
const CSV_FIELD_DATE = ['日期', 'date'][0];

const CSV_FILES = [
  './data/processed/1_clean.csv',
  './data/processed/2_clean.csv',
  './data/processed/3_clean.csv'
];

const THEME = {
  paper_bgcolor: '#ffffff',
  plot_bgcolor: '#f9fbfd',
  font: { family: 'Segoe UI, PingFang SC, Helvetica Neue', color: '#111' },
  title: { font: { size: 16, color: '#08306b' } }
};

document.addEventListener('DOMContentLoaded', async () => {
  document.getElementById('update-time').textContent = new Date().toLocaleDateString();

  const allRows = [];
  await Promise.all(CSV_FILES.map(async f => {
    try {
      const txt = await fetch(f).then(r => r.text());
      const rows = parseCSV(txt);
      if (rows.length) allRows.push(...rows);
    } catch (e) { console.warn('无法加载', f); }
  }));

  if (!allRows.length) return alert('未加载到数据');

  const cleaned = allRows.map(r => ({
    route: r[CSV_FIELD_ROUTE],
    price: parseFloat(String(r[CSV_FIELD_PRICE]).replace(/[^\d.]/g, '')) || NaN,
    ratio: parseFloat(String(r[CSV_FIELD_RATIO]).replace(/[^\d.-]/g, '')) || NaN,
    date: r[CSV_FIELD_DATE]
  }));

  populateRouteSelect(cleaned);
  renderAllCharts(cleaned, '__all__', 'price');

  document.getElementById('route-select').addEventListener('change', e => {
    renderAllCharts(cleaned, e.target.value, document.getElementById('metric-select').value);
  });
  document.getElementById('metric-select').addEventListener('change', e => {
    renderAllCharts(cleaned, document.getElementById('route-select').value, e.target.value);
  });
});

function parseCSV(text) {
  const lines = text.split('\n').filter(l => l.trim());
  const headers = lines[0].split(',').map(h => h.trim());
  return lines.slice(1).map(l => {
    const v = l.split(',');
    const obj = {};
    headers.forEach((h, i) => (obj[h] = v[i]));
    return obj;
  });
}

function populateRouteSelect(data) {
  const sel = document.getElementById('route-select');
  const routes = [...new Set(data.map(r => r.route))];
  routes.forEach(r => {
    const opt = document.createElement('option');
    opt.value = r;
    opt.textContent = r;
    sel.appendChild(opt);
  });
}

function renderAllCharts(data, route, metric) {
  const filtered = route === '__all__' ? data : data.filter(d => d.route === route);

  const avgByRoute = {};
  data.forEach(r => {
    if (!avgByRoute[r.route]) avgByRoute[r.route] = [];
    avgByRoute[r.route].push(r.price);
  });
  const routeNames = Object.keys(avgByRoute);
  const routeAvg = routeNames.map(r => avgByRoute[r].reduce((a,b)=>a+b,0)/avgByRoute[r].length);

  // 均价对比
  Plotly.react('chart-route-bar', [{
    x: routeNames, y: routeAvg, type:'bar',
    marker:{color:'#0d6efd'}
  }], { title:'不同路线均价对比', xaxis:{tickangle:-45}, yaxis:{title:'均价(元)'}, ...THEME });

  // 占比饼图
  Plotly.react('chart-pie', [{
    labels: routeNames, values: routeAvg, type:'pie', hole:0.4,
    marker:{line:{color:'#fff',width:2}}
  }], { title:'不同路线价格占比', ...THEME });


// 按月份聚合订单量与平均价格
const monthAgg = {};
data.forEach(d => {
  const month = d.date.slice(0, 7); // YYYY-MM
  if (!monthAgg[month]) monthAgg[month] = { count: 0, totalPrice: 0, num: 0 };
  monthAgg[month].count += 1;
  if (!isNaN(d.price)) {
    monthAgg[month].totalPrice += d.price;
    monthAgg[month].num += 1;
  }
});

// 转换为可视化数据
const monthsAll = Object.keys(monthAgg).sort((a, b) => new Date(a) - new Date(b));
const countsAll = monthsAll.map(m => monthAgg[m].count);
const avgPricesAll = monthsAll.map(m =>
  monthAgg[m].num > 0 ? monthAgg[m].totalPrice / monthAgg[m].num : null
);

// 每隔 3 个月抽样一次（季度）
const step = Math.ceil(monthsAll.length / 12); // 控制最多 12~15 个点
const months = monthsAll.filter((_, i) => i % step === 0);
const orderCounts = countsAll.filter((_, i) => i % step === 0);
const avgPrices = avgPricesAll.filter((_, i) => i % step === 0);

// 轨迹定义
const traceOrders = {
  x: months,
  y: orderCounts,
  name: '订单量',
  type: 'scatter',
  mode: 'lines+markers',
  line: { color: '#2563eb', width: 2 },
  marker: { size: 6, color: '#2563eb' },
  yaxis: 'y1',
  hovertemplate: '月份: %{x}<br>订单量: %{y}<extra></extra>'
};

const traceAvgPrice = {
  x: months,
  y: avgPrices,
  name: '平均价格',
  type: 'scatter',
  mode: 'lines+markers',
  line: { color: '#10b981', width: 3, shape: 'spline' },
  marker: { size: 5, color: '#10b981' },
  yaxis: 'y2',
  hovertemplate: '月份: %{x}<br>平均价格: %{y:.0f} 元<extra></extra>'
};

// 图表布局
const layoutTrend = {
  xaxis: {
    title: '月份',
    tickangle: -30,
    showgrid: true,
    gridcolor: 'rgba(230,230,230,0.4)'
  },
  yaxis: {
    title: '订单量',
    showgrid: true,
    gridcolor: 'rgba(220,220,220,0.3)',
    zeroline: false
  },
  yaxis2: {
    title: '平均价格 (元)',
    overlaying: 'y',
    side: 'right',
    showgrid: false
  },
  plot_bgcolor: '#fff',
  paper_bgcolor: '#fff',
  font: { family: 'PingFang SC, Microsoft YaHei', color: '#111' },
  margin: { t: 60, l: 70, r: 70, b: 80 },
  width: 380,
  height: 400,
  showlegend: true,
  legend: {
    orientation: 'h',
    xanchor: 'center',
    x: 0.5,
    y: -0.25,
    font: { size: 12 }
    }
  };

  // 绘制图表
  Plotly.newPlot('chart-trend', [traceOrders, traceAvgPrice], layoutTrend);


  // 环比涨跌
  const rise = filtered.filter(d=>d.ratio>0).length;
  const flat = filtered.filter(d=>d.ratio===0).length;
  const fall = filtered.filter(d=>d.ratio<0).length;
  Plotly.react('chart-ratio', [{
    x:['上涨','持平','下降'], y:[rise,flat,fall],
    type:'bar', marker:{color:['#ff6b6b','#ffc107','#08fcb2ff']}
  }], { title:'环比涨跌分析', yaxis:{title:'次数'}, ...THEME });

  // 直方图
  Plotly.react('chart-hist', [{
    x: filtered.map(d=>d.price), type:'histogram', nbinsx:30,
    marker:{color:'rgba(13,110,253,0.7)',line:{color:'#fff',width:1}}, opacity:0.8
  }], { title:'价格分布直方图', xaxis:{title:'价格(元)'}, yaxis:{title:'频数'}, ...THEME });

  // 热力图
  const heatRoutes = [...new Set(data.map(d=>d.route))];
  const heatDates = [...new Set(data.map(d=>d.date))];
  const zMatrix = heatRoutes.map(r=>heatDates.map(d=>{
    const f=data.find(v=>v.route===r && v.date===d);
    return f?f.price:NaN;
  }));
  Plotly.react('chart-heat', [{
    z:zMatrix, x:heatDates, y:heatRoutes, type:'heatmap',
    colorscale:'RdBu', reversescale:true, zsmooth:'best',
    colorbar:{title:'价格(元)'}
  }], { title:'价格波动热力图', xaxis:{tickangle:-45}, ...THEME });
}
