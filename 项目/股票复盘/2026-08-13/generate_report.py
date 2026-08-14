#!/usr/bin/env python3
"""量化反包法2.0 - 断板反包选股报告生成器 | 2026-08-13 盘中"""
import json, os

# 8/13 断板候选（反包日=8/14）
results = [
    {
        "code": "sh603897", "name": "长城科技", "board": 2,
        "close": 33.85, "chg_pct": 5.59,
        "ma5": 29.61, "ma10": 27.66, "dev_ma5": 14.33,
        "vol_ratio": 0.78,
        "tier": "B",
        "tier_reason": "唯一断板日主力净流入+超大单回流（资金面最优），但偏离MA5 +14.3%过高，非标准低吸，仅观察",
        "ff_label": "主力+6267万 超大单+6510万 散户净流出 = 断板日主力不撤 ★（5日累计+1.02亿）",
        "sector": "PCB/覆铜板·算力硬件", "role": "PCB上游CCL分支人气股（对标宝鼎科技/景旺电子反包）",
        "label_tags": "缩量洗盘 | 冲高回落 | 远离MA5"
    },
    {
        "code": "sz002248", "name": "华东数控", "board": 3,
        "close": 11.78, "chg_pct": -3.12,
        "ma5": 10.84, "ma10": 9.87, "dev_ma5": 8.67,
        "vol_ratio": 0.74,
        "tier": "C",
        "tier_reason": "3板掉队 + 断板日主力流出(-2462万)散户接盘 = 出货结构，形态虽缩量小阴但资金面弱",
        "ff_label": "主力-2462万 超大单-2787万 散户+2462万接盘 ⚠（5日累计+1.41亿仍正）",
        "sector": "工业母机/通用设备", "role": "工业母机分支（3进4掉队，前排无合力）",
        "label_tags": "缩量洗盘 | 小阴 | 偏离适中"
    },
    {
        "code": "sz002047", "name": "宝鹰股份", "board": 2,
        "close": 3.83, "chg_pct": -2.30,
        "ma5": 3.55, "ma10": 3.40, "dev_ma5": 8.01,
        "vol_ratio": 2.94,
        "tier": "C",
        "tier_reason": "放量2.94x高开低走大阴 + 主力5/10/20日持续净流出 = 典型出货，长上影线对手盘重",
        "ff_label": "主力-2221万 超大单-3001万 5日-1148万/10日-7637万/20日-1.54亿 持续流出 ⚠⚠",
        "sector": "建筑装饰", "role": "建筑后排跟风",
        "label_tags": "明显放量⚠ | 高开低走 | 长上影线"
    },
    {
        "code": "sh600162", "name": "香江控股", "board": 2,
        "close": 4.89, "chg_pct": 3.60,
        "ma5": 4.30, "ma10": 3.79, "dev_ma5": 13.62,
        "vol_ratio": 1.30,
        "tier": "C",
        "tier_reason": "断板日主力大幅流出(-9567万)超大单-7010万 + 散户流入 = 出货，偏离MA5 +13.6%过高",
        "ff_label": "主力-9567万 超大单-7010万 散户净流入 ⚠（5日+1.24亿但断板日兑现凶猛）",
        "sector": "房地产/粤港澳", "role": "地产补涨股（城建发展/新城控股带动的后排）",
        "label_tags": "温和量 | 小阳 | 远离MA5"
    },
    {
        "code": "sz002031", "name": "巨轮智能", "board": 2,
        "close": 6.41, "chg_pct": -0.16,
        "ma5": 5.84, "ma10": 5.53, "dev_ma5": 9.68,
        "vol_ratio": 1.33,
        "tier": "C",
        "tier_reason": "断板日主力巨量流出(-1.83亿)超大单-1.14亿 + 散户接盘 = 典型出货，机器人后排杂毛",
        "ff_label": "主力-1.83亿 超大单-1.14亿 散户+1.90亿接盘 ⚠⚠（5日+5.58亿高位兑现）",
        "sector": "机器人/减速器", "role": "机器人后排杂毛（龙头秦安股份4板一字）",
        "label_tags": "温和量 | 十字星 | 偏离适中"
    },
]

a_list = [r for r in results if r["tier"] == "A"]
b_list = [r for r in results if r["tier"] == "B"]
c_list = [r for r in results if r["tier"] == "C"]

dev_data = json.dumps([{"name": r["name"], "dev": r["dev_ma5"], "tier": r["tier"]} for r in results], ensure_ascii=False)

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>断板反包选股报告 | 2026-08-13 盘中</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js"></script>
<style>
:root{--bg:#f8f9fa;--card:#fff;--text:#1a1a2e;--sub:#555;--red:#d63031;--green:#00b894;--orange:#e17055;--gray:#b2bec3;--border:#e0e0e0;--a-bg:#d4edda;--a-border:#28a745;--b-bg:#fff3cd;--b-border:#ffc107;--c-bg:#f8d7da;--c-border:#dc3545;}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,"Microsoft YaHei",sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
.container{max-width:1200px;margin:0 auto;padding:20px}
.header{background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;padding:40px 30px;border-radius:12px;margin-bottom:24px}
.header h1{font-size:28px;margin-bottom:8px}
.header .subtitle{color:#a0a0b0;font-size:14px}
.header .date{color:#e17055;font-size:13px;margin-top:4px}
.tldr{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:24px}
.kpi{background:var(--card);border-radius:10px;padding:18px;box-shadow:0 2px 8px rgba(0,0,0,0.06);border-left:4px solid var(--border)}
.kpi .label{font-size:12px;color:var(--sub);text-transform:uppercase;letter-spacing:1px}
.kpi .value{font-size:24px;font-weight:700;margin:4px 0}
.kpi.red .value{color:var(--red)}
.kpi.green .value{color:var(--green)}
.kpi .desc{font-size:12px;color:var(--sub)}
.section{background:var(--card);border-radius:10px;padding:24px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,0.06)}
.section h2{font-size:18px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid var(--border);display:flex;align-items:center;gap:8px}
.chart-container{width:100%;height:380px;margin:16px 0}
table{width:100%;border-collapse:collapse;font-size:13px}
th{background:#f1f2f6;padding:10px 8px;text-align:left;font-weight:600;font-size:12px;color:var(--sub);border-bottom:2px solid var(--border);white-space:nowrap}
td{padding:10px 8px;border-bottom:1px solid var(--border)}
tr:hover{background:#f8f9ff}
.tier-badge{display:inline-block;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:700;color:#fff}
.tier-a{background:var(--a-border)}
.tier-b{background:var(--b-border);color:#333}
.tier-c{background:var(--c-border)}
.chg-up{color:var(--red);font-weight:600}
.chg-down{color:var(--green);font-weight:600}
.code{font-family:"SF Mono","Consolas",monospace;font-size:12px;color:#888}
.warn-box{background:#fff3cd;border:1px solid var(--b-border);border-radius:8px;padding:16px;margin-top:12px;font-size:13px}
.warn-box strong{color:#856404}
.danger-box{background:var(--c-bg);border:1px solid var(--c-border);border-radius:8px;padding:16px;margin-top:12px;font-size:13px}
.danger-box strong{color:#721c24}
.info-box{background:var(--a-bg);border:1px solid var(--a-border);border-radius:8px;padding:16px;margin-top:12px;font-size:13px}
.info-box strong{color:#155724}
.highlight-box{background:#e8f4fd;border:1px solid #4aa3df;border-radius:8px;padding:16px;margin-top:12px;font-size:13px}
.highlight-box strong{color:#1a5276}
.tag{display:inline-block;padding:1px 8px;border-radius:4px;font-size:11px;margin:1px;background:#e8e8e8;color:#555}
.footer{text-align:center;padding:30px;color:var(--sub);font-size:12px;line-height:1.8}
.footer strong{color:var(--red)}
</style>
</head>
<body>
<div class="container">

<div class="header">
<h1>量化反包法2.0 — 断板反包选股报告</h1>
<div class="subtitle">二/三板断板 + 板块龙头 + 贴MA5 + 缩量洗盘 + 资金流验证 五维筛选</div>
<div class="date">数据时点：2026-08-13 盘中(约10:26) | 沪指+0.43% 深成指+0.85% 创业板+1.55%(领涨) | ⚠未收盘，断板状态需尾盘确认</div>
</div>

<!-- TL;DR -->
<div class="tldr">
<div class="kpi green"><div class="label">市场情绪</div><div class="value">双创领涨</div><div class="desc">普涨修复延续 0跌停</div></div>
<div class="kpi"><div class="label">连板梯队</div><div class="value">高位晋级</div><div class="desc">3板→4板6只成功晋级</div></div>
<div class="kpi red"><div class="label">断板候选</div><div class="value">5只</div><div class="desc">A级0 / B级1 / C级4</div></div>
<div class="kpi orange"><div class="label">核心结论</div><div class="value" style="font-size:16px">等回踩不追高</div><div class="desc">无标准A级低吸标的</div></div>
</div>

<!-- 关键提示 -->
<div class="section">
<h2>💡 今日核心判读</h2>
<div class="highlight-box">
<strong>今日(8/13)5只断板股全部是主线跟风后排，且断板日收盘普遍脱离MA5 +8%~+14% → 无标准A级低吸标的。</strong><br>
唯一资金面合格的<b>长城科技</b>(主力净流入+超大单回流)偏离MA5达+14.3%，属高位非标准低吸，仅列B级观察。<br>
其余4只断板日主力全部流出+散户接盘，构成出货结构，一律避雷。<br>
<strong style="color:#d63031">真正值得跟踪的反包对象，是昨日(8/12)断板组的二次确认——哈药股份今日已现"出而后返"强反包信号。</strong>
</div>
</div>

<!-- Chart -->
<div class="section">
<h2>📊 偏离MA5% 对比（越低越接近标准低吸区）</h2>
<div id="devChart" class="chart-container"></div>
</div>

<!-- B级 -->
<div class="section">
<h2>🔍 Tier B — 观察列表 (1只)</h2>
<div class="warn-box">
<strong>📋 长城科技 sh603897</strong> — 2板断板 | PCB/覆铜板·算力硬件<br>
<strong>资金面（唯一合格）：</strong>主力+6267万、超大单+6510万、散户净流出 → 断板日"主力不撤"，5日累计+1.02亿<br>
<strong>形态缺陷：</strong>偏离MA5 +14.3%过高，+5.59%冲高回落(高35.2收33.85)，非标准低吸位<br>
<strong>操作参考：</strong>仅观察，若8/14回踩MA5(29.61)附近企稳且竞价红柱，才考虑低吸；止损MA10(27.66)
</div>
</div>

<!-- C级 -->
<div class="section">
<h2>🚫 Tier C — 避雷/谨慎 (4只)</h2>
<div class="danger-box" style="margin-bottom:8px">
<strong>❌ 巨轮智能 sz002031</strong> — 2板断板 | 机器人后排杂毛（龙头秦安4板一字）<br>
断板日主力-1.83亿、超大单-1.14亿、散户+1.90亿接盘 = 典型高位出货，放弃。
</div>
<div class="danger-box" style="margin-bottom:8px">
<strong>❌ 香江控股 sh600162</strong> — 2板断板 | 地产后排补涨<br>
断板日主力-9567万、超大单-7010万、散户流入 = 出货，偏离MA5 +13.6%过高，放弃。
</div>
<div class="danger-box" style="margin-bottom:8px">
<strong>❌ 宝鹰股份 sz002047</strong> — 2板断板 | 建筑后排跟风<br>
放量2.94x高开低走大阴线 + 主力5/10/20日持续净流出 = 长上影线对手盘重，最差，放弃。
</div>
<div class="danger-box">
<strong>❌ 华东数控 sz002248</strong> — 3板断板 | 工业母机（3进4掉队）<br>
断板日主力-2462万、超大单-2787万、散户接盘 = 出货结构，虽缩量小阴形态尚可但资金面弱，放弃。
</div>
</div>

<!-- Detail table -->
<div class="section">
<h2>📋 全部候选明细</h2>
<div style="overflow-x:auto">
<table>
<thead><tr>
<th>代码</th><th>名称</th><th>板数</th><th>收盘</th><th>涨跌</th><th>MA5</th><th>MA10</th><th>偏离MA5</th><th>量比</th><th>题材</th><th>龙头属性</th><th>形态标签</th><th>评级</th>
</tr></thead>
<tbody>
'''
for r in results:
    chg_cls = "chg-up" if r["chg_pct"] > 0 else "chg-down"
    tier_cls = f"tier-{r['tier'].lower()}"
    html += f'''
<tr>
<td class="code">{r["code"]}</td>
<td><strong>{r["name"]}</strong></td>
<td>{r["board"]}板</td>
<td>{r["close"]:.2f}</td>
<td class="{chg_cls}">{r["chg_pct"]:+.2f}%</td>
<td>{r["ma5"]}</td>
<td>{r["ma10"]}</td>
<td class="chg-up">{r["dev_ma5"]:+.2f}%</td>
<td>{r["vol_ratio"]:.2f}x</td>
<td style="font-size:12px">{r["sector"]}</td>
<td style="font-size:12px">{r["role"]}</td>
<td style="font-size:12px">{r["label_tags"]}</td>
<td><span class="tier-badge {tier_cls}">{r["tier"]}级</span></td>
</tr>'''
html += '''
</tbody></table></div></div>
'''

# Operation framework
html += '''
<div class="section">
<h2>🎯 操作框架（8/14 反包日低吸参考）</h2>
<div style="overflow-x:auto">
<table>
<thead><tr><th>标的</th><th>评级</th><th>MA5低吸区</th><th>MA10止损</th><th>触发条件</th></tr></thead>
<tbody>
'''
for r in results:
    tier_cls = f"tier-{r['tier'].lower()}"
    if r["tier"] == "B":
        cond = "8/14回踩MA5(29.61)企稳+竞价红柱才考虑，不追高"
    else:
        cond = "放弃（断板日主力流出=出货结构）"
    html += f'''
<tr>
<td><strong>{r["name"]}</strong></td>
<td><span class="tier-badge {tier_cls}">{r["tier"]}级</span></td>
<td>{r["ma5"]}</td>
<td>{r["ma10"]}</td>
<td style="font-size:13px">{cond}</td>
</tr>'''
html += '''
</tbody></table></div>
<div class="warn-box" style="margin-top:16px">
<strong>⚡ 核心铁律（量化反包法2.0 + 项目实战经验）：</strong><br>
1. <strong>资金流 &gt; 形态</strong> — 断板日"主力不撤"(主力+超大单流入、散户流出)可覆盖形态瑕疵；反之形态再漂亮，主力流出=出货=放弃<br>
2. 断板日主力流出 + 散户流入 = 出货结构，直接放弃<br>
3. <strong>反包日二次确认更重要</strong> — 断板日主力流出≠必然出货，反包日主力大额回流(超大单转正)即"出而后返"，是强反包信号（哈药股份8/13实证）<br>
4. "贴MA5"实操理解为反包日回踩买点区，连板后偏离MA5通常在+6%~+17%<br>
5. <strong>竞价红柱为最终买点确认，AI无法获取竞价数据，必须用户手动确认</strong>
</div>
</div>
'''

# 8/12 反包跟踪
html += '''
<div class="section">
<h2>🔁 昨日(8/12)断板组 反包跟踪（今日8/13验证）</h2>
<div class="info-box">
<strong>🏆 哈药股份 sh600664（3板断板）— "出而后返"强反包实证</strong><br>
昨日断板日判定"主力流出+散户流入"放弃；今日反包日主力净流入+2.07亿、超大单+2.61亿回流、散户净流出-1.25亿，股价+1.82%创52周新高(9.05)。<br>
<strong>结论：断板日"主力流出"≠必然出货，反包日二次资金流确认才是关键。</strong>此经验已沉淀为项目铁律。
</div>
<div class="warn-box">
<strong>其余4只（国风新材/第一医药/立新能源/亚邦股份）</strong>：早盘全部下跌，验证昨日"放弃/避雷"判断正确。今日资金流二次确认的筛选框架有效。
</div>
</div>
'''

# Disclaimer
html += '''
<div class="footer">
<strong>⚠ 风险提示</strong><br>
本报告基于量化反包法2.0选股框架自动生成，仅用于个人学习与研究目的。<br>
<strong>不构成任何投资建议，不推荐任何具体股票。</strong><br>
短线"断板反包"属于高波动、高回撤玩法，请独立判断、严格控制仓位。<br>
数据来源：腾讯自选股(westock) K线/行情/资金流 + 连板梯队聚合 | 2026-08-13 盘中(未收盘)<br>
生成时间：2026-08-13 10:26 | 量化反包法2.0 自动选股系统
</div>

</div>

<script>
var devData = ''' + dev_data + ''';
var chart = echarts.init(document.getElementById('devChart'));
var names = devData.map(function(d){return d.name;});
var devs = devData.map(function(d){return d.dev;});
var colors = devs.map(function(d){return d<=7?'#28a745':d<=12?'#e17055':'#b2bec3';});
var option = {
  tooltip: {trigger:'axis',formatter:function(p){return p[0].name+'<br/>偏离MA5: '+p[0].value.toFixed(2)+'%';}},
  grid: {left:'3%',right:'4%',bottom:'3%',containLabel:true},
  xAxis: {type:'category',data:names,axisLabel:{fontSize:12}},
  yAxis: {type:'value',name:'偏离MA5(%)',axisLabel:{formatter:'{value}%'}},
  series:[{
    type:'bar',data:devs.map(function(d,i){return {value:d,itemStyle:{color:colors[i]}};}),
    barWidth:'50%',
    label:{show:true,position:'top',formatter:function(p){return p.value.toFixed(1)+'%';}},
    markLine:{silent:true,data:[{yAxis:7,label:{formatter:'贴MA5阈值 7%',fontSize:11},lineStyle:{color:'#28a745',type:'dashed'}},{yAxis:12,label:{formatter:'偏离上限 12%',fontSize:11},lineStyle:{color:'#e17055',type:'dashed'}}]}
  }]
};
chart.setOption(option);
window.addEventListener('resize',function(){chart.resize();});
</script>
</body>
</html>
'''

out_path = 'C:/pkb/个人知识库/项目/股票复盘/2026-08-13/反包选股_2.0_20260813.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Report generated: {out_path}")
print(f"A-level: {len(a_list)}, B-level: {len(b_list)}, C-level: {len(c_list)}")
for r in results:
    print(f"  [{r['tier']}] {r['name']} {r['code']} | {r['board']}板断板 | 偏离MA5 {r['dev_ma5']:.1f}% | 量比 {r['vol_ratio']:.2f}x | {r['chg_pct']:+.2f}% | {r['tier_reason'][:30]}")
