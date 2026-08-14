#!/usr/bin/env python3
"""量化反包法2.0 - 断板反包选股报告生成器 | 2026-08-12"""
import json, os

# === RAW DATA ===

# K-line: [date, open, close, high, low, volume] - most recent first (15 days)
kline_raw = {
    "sh600664": {
        "name": "哈药股份", "board": 3,
        "prices": [
            ("2026-08-12", 8.27, 8.81, 8.96, 8.27, 5980676),
            ("2026-08-11", 7.76, 8.27, 8.27, 7.76, 6787521),
            ("2026-08-10", 7.52, 7.52, 7.52, 7.40, 1317603),
            ("2026-08-07", 6.65, 6.84, 6.84, 6.45, 2697082),
            ("2026-08-06", 6.85, 6.22, 6.92, 6.10, 5322894),
            ("2026-08-05", 6.40, 6.77, 6.80, 6.31, 4751193),
            ("2026-08-04", 6.00, 6.45, 6.58, 5.93, 4890398),
            ("2026-08-03", 5.89, 5.99, 6.15, 5.71, 3987204),
            ("2026-07-31", 5.22, 5.89, 5.90, 5.22, 4292416),
            ("2026-07-30", 5.36, 5.56, 5.69, 5.20, 4015252),
            ("2026-07-29", 5.47, 5.36, 5.73, 5.17, 3927771),
            ("2026-07-28", 5.60, 5.74, 5.98, 5.36, 5137786),
            ("2026-07-27", 5.38, 5.64, 5.80, 5.14, 5159573),
            ("2026-07-24", 5.54, 5.40, 5.99, 5.40, 5254680),
            ("2026-07-23", 5.87, 6.00, 6.14, 5.74, 5399993),
        ]
    },
    "sh600833": {
        "name": "第一医药", "board": 2,
        "prices": [
            ("2026-08-12", 12.00, 12.49, 12.87, 11.76, 486738),
            ("2026-08-11", 10.89, 12.11, 12.11, 10.61, 380333),
            ("2026-08-10", 10.08, 11.01, 11.01, 10.08, 133683),
            ("2026-08-07", 9.90, 10.01, 10.06, 9.71, 91663),
            ("2026-08-06", 9.77, 10.01, 10.06, 9.66, 93602),
            ("2026-08-05", 9.88, 9.77, 9.93, 9.69, 44030),
            ("2026-08-04", 10.06, 9.86, 10.16, 9.82, 44846),
            ("2026-08-03", 9.70, 9.97, 9.97, 9.68, 36450),
            ("2026-07-31", 9.54, 9.68, 9.69, 9.52, 29729),
            ("2026-07-30", 9.55, 9.52, 9.79, 9.41, 43459),
        ]
    },
    "sz001258": {
        "name": "立新能源", "board": 2,
        "prices": [
            ("2026-08-12", 15.45, 15.46, 16.88, 14.65, 2113350),
            ("2026-08-11", 14.00, 15.93, 15.93, 13.10, 2436951),
            ("2026-08-10", 13.42, 14.48, 14.48, 13.42, 1763391),
            ("2026-08-07", 12.20, 13.16, 13.16, 11.85, 1490819),
            ("2026-08-06", 13.53, 12.19, 13.53, 12.19, 1479227),
            ("2026-08-05", 13.15, 13.53, 13.89, 13.01, 1516441),
            ("2026-08-04", 12.50, 13.40, 13.48, 12.30, 1504259),
            ("2026-08-03", 12.25, 12.73, 12.96, 11.88, 1416288),
            ("2026-07-31", 11.12, 12.34, 12.97, 11.12, 1651695),
            ("2026-07-30", 11.85, 12.35, 12.46, 11.21, 1868895),
        ]
    },
    "sh603188": {
        "name": "亚邦股份", "board": 2,
        "prices": [
            ("2026-08-12", 4.66, 4.91, 5.09, 4.58, 882840),
            ("2026-08-11", 4.76, 4.88, 4.88, 4.76, 220505),
            ("2026-08-10", 4.03, 4.44, 4.44, 4.03, 292400),
            ("2026-08-07", 4.15, 4.04, 4.15, 3.94, 81280),
            ("2026-08-06", 4.00, 4.06, 4.07, 3.98, 85486),
        ]
    },
    "sh603797": {
        "name": "联泰环保", "board": 2,
        "prices": [
            ("2026-08-12", 4.98, 4.85, 5.17, 4.78, 636929),
            ("2026-08-11", 4.68, 5.05, 5.05, 4.66, 316699),
            ("2026-08-10", 4.20, 4.59, 4.59, 4.16, 269597),
            ("2026-08-07", 4.07, 4.17, 4.31, 4.07, 143537),
            ("2026-08-06", 4.06, 4.10, 4.12, 3.99, 68522),
        ]
    },
    "sz000859": {
        "name": "国风新材", "board": 2,
        "prices": [
            ("2026-08-12", 10.38, 10.20, 10.53, 9.99, 1546001),
            ("2026-08-11", 9.56, 10.48, 10.48, 9.53, 1253214),
            ("2026-08-10", 8.66, 9.53, 9.53, 8.40, 723759),
            ("2026-08-07", 8.75, 8.66, 8.85, 8.50, 496557),
            ("2026-08-06", 8.50, 8.91, 9.30, 8.42, 691667),
        ]
    },
}

# Fund flow (today only)
fund_flow = {
    "sh600664": {"main_net": -179277232, "jumbo_net": -111761725, "mid_net": 72784737, "small_net": 106492495,
                 "main5d": 302151245, "main10d": 289649749, "main20d": -390799456},
    "sh600833": {"main_net": -38722629, "jumbo_net": -34226599, "mid_net": 18120903, "small_net": 20601727,
                 "main5d": 92655938, "main10d": 87515824, "main20d": 92716739},
    "sz001258": {"main_net": -73611585, "jumbo_net": -69169163, "mid_net": -105842288, "small_net": 179453873,
                 "main5d": 408556542, "main10d": 218798164, "main20d": 30675769},
    "sh603188": {"main_net": 12591943, "jumbo_net": 12357349, "mid_net": 28898424, "small_net": -41490367,
                 "main5d": 35620172, "main10d": 48641653, "main20d": 66469008},
    "sh603797": {"main_net": -2706496, "jumbo_net": -3596957, "mid_net": 24752722, "small_net": -22046226,
                 "main5d": 38093356, "main10d": 35937400, "main20d": 35998243},
    "sz000859": {"main_net": -139182413, "jumbo_net": -125399575, "mid_net": 33700546, "small_net": 105481867,
                 "main5d": 288156934, "main10d": 232308415, "main20d": 252869707},
}

# Market cap etc from quote
extra = {
    "sh600664": {"pe": 71.62, "pb": 3.79, "mcap": 221.88, "sector": "医药生物·化学制药", "role": "医药人气龙头(二波形态)", "leader": "龙头但非总龙头"},
    "sh600833": {"pe": 36.53, "pb": 2.39, "mcap": 27.86, "sector": "医药生物·医药商业", "role": "医药商业跟风补涨", "leader": "后排杂毛"},
    "sz001258": {"pe": 96.74, "pb": 4.67, "mcap": 144.29, "sector": "公用事业·电力", "role": "电力二波模仿盘", "leader": "非主线"},
    "sh603188": {"pe": -62.52, "pb": 3.97, "mcap": 28.00, "sector": "基础化工·化学制品", "role": "染料化工跟随", "leader": "后排跟风"},
    "sh603797": {"pe": 22.15, "pb": 0.83, "mcap": 27.97, "sector": "环保·环境治理", "role": "环保补涨股", "leader": "非主线"},
    "sz000859": {"pe": -130.70, "pb": 3.39, "mcap": 91.39, "sector": "基础化工·塑料/MLCC", "role": "MLCC/光刻胶连板先锋", "leader": "分支先锋"},
}

# === COMPUTE ===
def calc_ma(closes, n):
    if len(closes) < n: return sum(closes)/len(closes)
    return sum(closes[-n:])/n

results = []
for code, d in kline_raw.items():
    closes = [p[2] for p in d["prices"]]  # close prices (most recent first)
    # reverse for time order (oldest first)
    closes_rev = list(reversed(closes))
    
    ma5 = calc_ma(closes_rev, 5)
    ma10 = calc_ma(closes_rev, 10) if len(closes_rev) >= 10 else calc_ma(closes_rev, len(closes_rev))
    
    today_close = closes[0]  # 8/12 close
    yesterday_close = closes[1]  # 8/11 close (涨停日)
    dev_ma5 = (today_close - ma5) / ma5 * 100
    
    today_vol = d["prices"][0][5]
    yesterday_vol = d["prices"][1][5]
    vol_ratio = today_vol / yesterday_vol
    
    chg_pct = (today_close - yesterday_close) / yesterday_close * 100
    
    ff = fund_flow.get(code, {})
    ex = extra.get(code, {})
    
    # Grading
    tier = "C"
    tier_reason = ""
    
    # Check C first (worst)
    if vol_ratio > 3.0:
        tier = "C"; tier_reason = "爆量(>3x)，对手盘极重"
    elif ex.get("leader","") in ("后排杂毛", "后排跟风") and abs(chg_pct) < 3 and vol_ratio > 1.3:
        tier = "C"; tier_reason = "后排+放量，辨识度不足"
    elif chg_pct < -3 and vol_ratio > 1.5:
        tier = "C"; tier_reason = "中阴放量(跌幅>3%+量比>1.5)"
    elif ex.get("leader","") in ("后排杂毛", "后排跟风"):
        tier = "B" if dev_ma5 < 10 and vol_ratio < 1.5 else "C"
        tier_reason = "后排跟风/补涨，非龙头逻辑" if tier == "C" else "后排但形态尚可，弱观察"
    elif dev_ma5 <= 8 and vol_ratio <= 1.5 and abs(chg_pct) <= 3:
        tier = "A"; tier_reason = "贴MA5+温和量+小阴洗盘"
    elif dev_ma5 <= 12 and vol_ratio < 1.0 and abs(chg_pct) <= 3:
        tier = "A"; tier_reason = "缩量小阴洗盘，偏离可控"
    elif dev_ma5 > 12:
        tier = "B"; tier_reason = f"高位偏离MA5 {dev_ma5:.1f}%，非标准低吸区"
    else:
        tier = "B"; tier_reason = "形态存疑，需观察"
    
    # fund flow label
    ff_label = ""
    if ff.get("main_net", 0) > 0:
        ff_label = f"主力净流入 {ff['main_net']/1e8:+.2f}亿 ★"
    elif ff.get("main5d", 0) > ff.get("main_net", 0) * 2 and ff.get("main5d", 0) > 2e8:
        ff_label = f"断板日主力-{abs(ff['main_net'])/1e8:.2f}亿，但5日累计+{ff['main5d']/1e8:.2f}亿(部分兑现)"
    elif ff.get("main5d", 0) > 3e8:
        ff_label = f"断板日主力-{abs(ff['main_net'])/1e8:.2f}亿，5日累计+{ff['main5d']/1e8:.2f}亿(获利部分流出)"
    else:
        ff_label = f"主力净流出 {abs(ff['main_net'])/1e8:.2f}亿 ⚠"
    
    label_tags = []
    if vol_ratio < 0.8: label_tags.append("缩量洗盘")
    elif vol_ratio < 1.3: label_tags.append("温和量")
    elif vol_ratio < 2.0: label_tags.append("放量分歧")
    elif vol_ratio < 3.0: label_tags.append("明显放量⚠")
    else: label_tags.append("爆量⚠⚠")
    
    if abs(chg_pct) < 1: label_tags.append("十字星")
    elif chg_pct > 0 and chg_pct < 3: label_tags.append("小阳断板")
    elif chg_pct >= 3: label_tags.append("中阳未封")
    elif chg_pct > -3: label_tags.append("小阴洗盘")
    else: label_tags.append("中阴回踩")
    
    if dev_ma5 <= 7: label_tags.append("贴MA5(优)")
    elif dev_ma5 <= 12: label_tags.append("偏离适中")
    else: label_tags.append("远离MA5")
    
    results.append({
        "code": code, "name": d["name"], "board": d["board"],
        "close": today_close, "prev_close": yesterday_close,
        "chg_pct": chg_pct,
        "ma5": round(ma5, 2), "ma10": round(ma10, 2),
        "dev_ma5": round(dev_ma5, 2),
        "vol_ratio": round(vol_ratio, 2),
        "tier": tier, "tier_reason": tier_reason,
        "ff_label": ff_label,
        "label_tags": " | ".join(label_tags),
        "sector": ex.get("sector", ""),
        "role": ex.get("role", ""),
        "leader": ex.get("leader", ""),
        "pe": ex.get("pe", 0), "pb": ex.get("pb", 0),
        "mcap": ex.get("mcap", 0),
        "main_net": ff.get("main_net", 0),
        "main5d": ff.get("main5d", 0),
        "main10d": ff.get("main10d", 0),
    })

# Sort: A first, then by dev_ma5 ascending
results.sort(key=lambda x: ({"A":0,"B":1,"C":2}[x["tier"]], x["dev_ma5"]))

# === GENERATE HTML ===
a_list = [r for r in results if r["tier"] == "A"]
b_list = [r for r in results if r["tier"] == "B"]
c_list = [r for r in results if r["tier"] == "C"]

def fmt_val(v, unit="亿"):
    if v is None: return "-"
    if unit == "亿":
        return f"{v/1e8:+.2f}亿"
    return str(v)

dev_data = json.dumps([{"name": r["name"], "dev": r["dev_ma5"], "tier": r["tier"]} for r in results])

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>断板反包选股报告 | 2026-08-12 收盘</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js"></script>
<style>
:root{{--bg:#f8f9fa;--card:#fff;--text:#1a1a2e;--sub:#555;--red:#d63031;--green:#00b894;--orange:#e17055;--gray:#b2bec3;--border:#e0e0e0;--a-bg:#d4edda;--a-border:#28a745;--b-bg:#fff3cd;--b-border:#ffc107;--c-bg:#f8d7da;--c-border:#dc3545;}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,"Microsoft YaHei",sans-serif;background:var(--bg);color:var(--text);line-height:1.6}}
.container{{max-width:1200px;margin:0 auto;padding:20px}}
.header{{background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;padding:40px 30px;border-radius:12px;margin-bottom:24px}}
.header h1{{font-size:28px;margin-bottom:8px}}
.header .subtitle{{color:#a0a0b0;font-size:14px}}
.header .date{{color:#e17055;font-size:13px;margin-top:4px}}
.tldr{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:24px}}
.kpi{{background:var(--card);border-radius:10px;padding:18px;box-shadow:0 2px 8px rgba(0,0,0,0.06);border-left:4px solid var(--border)}}
.kpi .label{{font-size:12px;color:var(--sub);text-transform:uppercase;letter-spacing:1px}}
.kpi .value{{font-size:24px;font-weight:700;margin:4px 0}}
.kpi.red .value{{color:var(--red)}}
.kpi.green .value{{color:var(--green)}}
.kpi .desc{{font-size:12px;color:var(--sub)}}
.section{{background:var(--card);border-radius:10px;padding:24px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,0.06)}}
.section h2{{font-size:18px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid var(--border);display:flex;align-items:center;gap:8px}}
.chart-container{{width:100%;height:380px;margin:16px 0}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{background:#f1f2f6;padding:10px 8px;text-align:left;font-weight:600;font-size:12px;color:var(--sub);border-bottom:2px solid var(--border);white-space:nowrap}}
td{{padding:10px 8px;border-bottom:1px solid var(--border)}}
tr:hover{{background:#f8f9ff}}
.tier-badge{{display:inline-block;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:700;color:#fff}}
.tier-a{{background:var(--a-border)}}
.tier-b{{background:var(--b-border);color:#333}}
.tier-c{{background:var(--c-border)}}
.chg-up{{color:var(--red);font-weight:600}}
.chg-down{{color:var(--green);font-weight:600}}
.code{{font-family:"SF Mono","Consolas",monospace;font-size:12px;color:#888}}
.warn-box{{background:#fff3cd;border:1px solid var(--b-border);border-radius:8px;padding:16px;margin-top:12px;font-size:13px}}
.warn-box strong{{color:#856404}}
.danger-box{{background:var(--c-bg);border:1px solid var(--c-border);border-radius:8px;padding:16px;margin-top:12px;font-size:13px}}
.danger-box strong{{color:#721c24}}
.info-box{{background:var(--a-bg);border:1px solid var(--a-border);border-radius:8px;padding:16px;margin-top:12px;font-size:13px}}
.info-box strong{{color:#155724}}
.tag{{display:inline-block;padding:1px 8px;border-radius:4px;font-size:11px;margin:1px;background:#e8e8e8;color:#555}}
.tag-good{{background:#d4edda;color:#155724}}
.tag-warn{{background:#fff3cd;color:#856404}}
.tag-bad{{background:#f8d7da;color:#721c24}}
.ops-table td:first-child{{font-weight:600}}
.footer{{text-align:center;padding:30px;color:var(--sub);font-size:12px;line-height:1.8}}
.footer strong{{color:var(--red)}}
</style>
</head>
<body>
<div class="container">

<div class="header">
<h1>量化反包法2.0 — 断板反包选股报告</h1>
<div class="subtitle">基于二/三板断板+板块龙头+贴MA5+缩量洗盘四维筛选</div>
<div class="date">数据时点：2026-08-12 收盘 | 上证 3946.68(+0.32%) 深成指 14414.43(+1.09%) 创业板 3602.08(+1.49%)</div>
</div>

<!-- TL;DR -->
<div class="tldr">
<div class="kpi green"><div class="label">市场情绪</div><div class="value">96涨停 0跌停</div><div class="desc">上涨4128只(74%) | 封板率88%</div></div>
<div class="kpi"><div class="label">成交额</div><div class="value">2.15万亿</div><div class="desc">缩量1686亿 | 连续3日缩量</div></div>
<div class="kpi"><div class="label">连板梯队</div><div class="value">7-5-4-3-2</div><div class="desc">晋级率56.25% | 百花医药7板</div></div>
<div class="kpi red"><div class="label">断板候选</div><div class="value">{len(results)}只</div><div class="desc">A级{len(a_list)} / B级{len(b_list)} / C级{len(c_list)}</div></div>
<div class="kpi green"><div class="label">首选标的</div><div class="value">{a_list[0]['name'] if a_list else '无'}</div><div class="desc">{a_list[0]['code'] if a_list else '-'} | {a_list[0]['sector'] if a_list else '-'}</div></div>
</div>

<!-- Chart -->
<div class="section">
<h2>📊 偏离MA5% 对比</h2>
<div id="devChart" class="chart-container"></div>
</div>

<!-- A级 -->
<div class="section">
<h2>⭐ Tier A — 首选低吸候选 ({len(a_list)}只)</h2>
'''
if a_list:
    for r in a_list:
        chg_cls = "chg-up" if r["chg_pct"]>0 else "chg-down"
        html += f'''
<div class="info-box">
<strong>🏆 {r["name"]} {r["code"]}</strong> — {r["board"]}板断板 | {r["sector"]}<br>
<strong>等级理由：</strong>{r["tier_reason"]}<br>
<strong>资金面：</strong>{r["ff_label"]}<br>
<strong>操作参考：</strong>明日(T+1)若回踩MA5({r["ma5"]})附近可低吸，止损MA10({r["ma10"]})，竞价需手动确认红柱抢筹
</div>'''
else:
    html += '<p style="color:var(--sub)">今日无A级候选</p>'
html += '</div>'

# B级
html += f'''
<div class="section">
<h2>🔍 Tier B — 观察列表 ({len(b_list)}只)</h2>
'''
if b_list:
    for r in b_list:
        chg_cls = "chg-up" if r["chg_pct"]>0 else "chg-down"
        html += f'''
<div class="warn-box" style="margin-bottom:8px">
<strong>📋 {r["name"]} {r["code"]}</strong> — {r["board"]}板断板 | {r["sector"]}<br>
<strong>等级理由：</strong>{r["tier_reason"]}<br>
<strong>资金面：</strong>{r["ff_label"]}
</div>'''
else:
    html += '<p style="color:var(--sub)">无B级候选</p>'
html += '</div>'

# C级
html += f'''
<div class="section">
<h2>🚫 Tier C — 避雷/谨慎 ({len(c_list)}只)</h2>
'''
if c_list:
    for r in c_list:
        chg_cls = "chg-up" if r["chg_pct"]>0 else "chg-down"
        html += f'''
<div class="danger-box" style="margin-bottom:8px">
<strong>❌ {r["name"]} {r["code"]}</strong> — {r["board"]}板断板 | {r["sector"]}<br>
<strong>等级理由：</strong>{r["tier_reason"]}
</div>'''
else:
    html += '<p style="color:var(--sub)">无C级候选</p>'
html += '</div>'

# Detail table
html += '''
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
    chg_cls = "chg-up" if r["chg_pct"]>0 else "chg-down"
    dev_cls = "chg-up" if r["dev_ma5"] > 0 else "chg-down"
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
<td class="{dev_cls}">{r["dev_ma5"]:+.2f}%</td>
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
<h2>🎯 操作框架（T+1 反包日低吸参考）</h2>
<div style="overflow-x:auto">
<table class="ops-table">
<thead><tr><th>标的</th><th>MA5低吸区</th><th>MA10止损</th><th>触发条件</th><th>竞价确认</th></tr></thead>
<tbody>
'''
for r in results:
    if r["tier"] in ("A", "B"):
        cond = "开在MA5附近→沿MA5低吸" if r["dev_ma5"]<12 else "仅回踩至MA5下方才考虑小量试仓"
        html += f'''
<tr>
<td><strong>{r["name"]}</strong> <span class="tier-badge tier-{r['tier'].lower()}">{r["tier"]}级</span></td>
<td>{r["ma5"]} (偏离{r["dev_ma5"]:+.1f}%)</td>
<td>{r["ma10"]}</td>
<td style="font-size:13px">{cond}</td>
<td>9:24-9:25竞价红柱抢筹确认</td>
</tr>'''
html += '''
</tbody></table></div>
<div class="warn-box" style="margin-top:16px">
<strong>⚡ 核心提醒（来自量化反包法2.0）：</strong><br>
1. 断板日"主力不撤"是最硬核的证据 — 资金流比形态重要得多<br>
2. 断板日主力流出+散户流入=出货结构，直接放弃<br>
3. "贴MA5"实操中理解为反包日回踩买点区，连板后偏离MA5通常在+6%~+17%<br>
4. <strong>竞价红柱为最终买点确认，AI无法获取竞价数据，必须用户手动确认</strong>
</div>
</div>
'''

# Disclaimer
html += f'''
<div class="footer">
<strong>⚠ 风险提示</strong><br>
本报告基于量化反包法2.0选股框架自动生成，仅用于个人学习与研究目的。<br>
<strong>不构成任何投资建议，不推荐任何具体股票。</strong><br>
短线"断板反包"属于高波动、高回撤玩法，请独立判断、严格控制仓位。<br>
所有数据来源：腾讯自选股(westock) K线/行情/资金流 | 2026-08-12 收盘<br>
生成时间：2026-08-12 21:59 | 量化反包法2.0 自动选股系统
</div>

</div>

<script>
var devData = {dev_data};
var chart = echarts.init(document.getElementById('devChart'));
var names = devData.map(function(d){{return d.name;}});
var devs = devData.map(function(d){{return d.dev;}});
var colors = devs.map(function(d){{return d<=7?'#28a745':d<=12?'#e17055':'#b2bec3';}});
var option = {{
  tooltip: {{trigger:'axis',formatter:function(p){{return p[0].name+'<br/>偏离MA5: '+p[0].value.toFixed(2)+'%';}}}},
  grid: {{left:'3%',right:'4%',bottom:'3%',containLabel:true}},
  xAxis: {{type:'category',data:names,axisLabel:{{fontSize:12}}}},
  yAxis: {{type:'value',name:'偏离MA5(%)',axisLabel:{{formatter:'{{value}}%'}}}},
  series:[{{
    type:'bar',data:devs.map(function(d,i){{return {{value:d,itemStyle:{{color:colors[i]}}}};}}),
    barWidth:'50%',
    markLine:{{silent:true,data:[{{yAxis:7,label:{{formatter:'贴MA5阈值 7%',fontSize:11}},lineStyle:{{color:'#28a745',type:'dashed'}}}},{{yAxis:12,label:{{formatter:'偏离上限 12%',fontSize:11}},lineStyle:{{color:'#e17055',type:'dashed'}}}}]}}
  }}]
}};
chart.setOption(option);
window.addEventListener('resize',function(){{chart.resize();}});
</script>
</body>
</html>'''

out_dir = os.path.join(os.path.dirname(__file__) if '__file__' in dir() else 'C:/pkb/个人知识库/项目/股票复盘/2026-8-12')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, '断板反包_选股报告_2026-08-12.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Report generated: {out_path}")
print(f"A-level: {len(a_list)}, B-level: {len(b_list)}, C-level: {len(c_list)}")
for r in results:
    print(f"  [{r['tier']}] {r['name']} {r['code']} | {r['board']}板断板 | 偏离MA5 {r['dev_ma5']:.1f}% | 量比 {r['vol_ratio']:.2f}x | {r['chg_pct']:+.2f}% | {r['tier_reason']}")
