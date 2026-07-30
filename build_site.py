#!/usr/bin/env python3
"""
构建陕电现货观察网站 index.html（运行时 fetch 数据，不内联数据）。

用法：
  python3 build_site.py

输出：index.html（含内联 CSS+JS，不含数据）
数据：运行时从 ./data/*.json fetch，带 SHA-256 校验

遵循需求文档《WorkBuddy网页配置与数据接入需求.md》全部要求。
"""
from pathlib import Path

OUT = Path(__file__).parent / "index.html"

CSS = r"""
/* ============================================================
   陕电现货观察 — Apple 风格视觉系统 v2
   设计语言：SF Pro / 大留白 / 圆角卡片 / 毛玻璃 / 系统蓝
   遵循需求文档：运行时 fetch / 来源追溯 / 质量展示 / 缺失值不补零
   ============================================================ */

:root {
  --bg: #fbfbfd;
  --surface: #ffffff;
  --ink: #1d1d1f;
  --muted: #6e6e73;
  --subtle: #86868b;
  --accent: #0071e3;
  --accent-hover: #0077ed;
  --accent-soft: #e8f1fd;
  --line: #d2d2d7;
  --soft: #f5f5f7;
  --up: #e34c3e;
  --down: #34c759;
  --warn: #ff9500;
  --danger: #ff3b30;
  --radius-sm: 10px;
  --radius: 18px;
  --radius-lg: 24px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,.04), 0 1px 3px rgba(0,0,0,.05);
  --shadow: 0 4px 16px rgba(0,0,0,.04), 0 1px 4px rgba(0,0,0,.04);
  --shadow-lg: 0 18px 44px rgba(0,0,0,.06), 0 4px 12px rgba(0,0,0,.04);
  --maxw: 1120px;
  --font: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text",
    "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif;
  /* 10 条价格曲线配色 */
  --c-overall-da: #0071e3;
  --c-overall-rt: #34c759;
  --c-thermal-da: #ff9500;
  --c-thermal-rt: #bf5af2;
  --c-renew-da:   #5ac8fa;
  --c-renew-rt:   #0046a8;
  --c-wind-da:    #30b0c7;
  --c-wind-rt:    #1d1d1f;
  --c-solar-da:   #ffcc00;
  --c-solar-rt:   #ff3b30;
}

* { box-sizing: border-box; }

html { scroll-behavior: smooth; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }

body {
  margin: 0; background: var(--bg); color: var(--ink);
  font-family: var(--font); font-size: 17px; line-height: 1.47; letter-spacing: -0.01em;
}

button, a { font: inherit; color: inherit; text-decoration: none; }
button { background: none; border: 0; cursor: pointer; color: inherit; }

/* ============ 顶部导航（毛玻璃） ============ */
.site-header {
  position: sticky; top: 0; z-index: 30;
  display: flex; align-items: center; justify-content: space-between;
  width: min(var(--maxw), calc(100% - 48px)); margin: 0 auto; padding: 14px 0;
  background: rgba(251,251,253,.72);
  backdrop-filter: saturate(180%) blur(20px); -webkit-backdrop-filter: saturate(180%) blur(20px);
}
.brand { display: inline-flex; align-items: center; gap: 12px; }
.brand-mark {
  display: grid; width: 36px; height: 36px; place-items: center; border-radius: 10px;
  background: linear-gradient(135deg, #1d1d1f 0%, #3a3a3c 100%); color: white;
  font-weight: 700; font-size: 16px; letter-spacing: -0.02em;
}
.brand b, .brand small { display: block; }
.brand b { font-size: 15px; font-weight: 600; letter-spacing: -0.01em; }
.brand small { margin-top: 1px; color: var(--subtle); font-size: 10px; letter-spacing: .04em; text-transform: uppercase; }
nav { display: flex; gap: 28px; color: var(--muted); font-size: 14px; }
nav a { position: relative; transition: color 160ms ease; }
nav a:hover { color: var(--ink); }
nav a::after {
  position: absolute; right: 0; bottom: -7px; left: 0; height: 2px;
  background: var(--ink); border-radius: 2px; content: "";
  transform: scaleX(0); transform-origin: center; transition: transform 200ms ease;
}
nav a:hover::after { transform: scaleX(1); }

/* ============ 按钮 ============ */
.btn-primary, .btn-outline, .btn-text {
  display: inline-flex; align-items: center; justify-content: center;
  min-height: 44px; padding: 0 22px; border: 0; border-radius: 980px;
  cursor: pointer; font-weight: 400; font-size: 15px; letter-spacing: -0.01em;
  transition: transform 180ms ease, background 180ms ease, box-shadow 180ms ease;
}
.btn-primary { background: var(--accent); color: white; }
.btn-primary:hover { background: var(--accent-hover); transform: scale(1.02); }
.btn-primary:active { transform: scale(.99); }
.btn-primary.compact { min-height: 34px; padding: 0 16px; font-size: 13px; }
.btn-outline { min-height: 40px; border: 1px solid var(--line); background: var(--surface); color: var(--ink); }
.btn-outline:hover { background: var(--soft); }
.btn-outline.active { background: var(--accent-soft); border-color: var(--accent); color: var(--accent); }
.btn-text { background: transparent; color: var(--accent); padding: 0 12px; min-height: 36px; }
.btn-text:hover { text-decoration: underline; }

/* ============ Hero ============ */
.hero {
  display: grid; grid-template-columns: 1.1fr .9fr; gap: clamp(40px, 7vw, 96px);
  align-items: center; width: min(var(--maxw), calc(100% - 48px));
  min-height: 520px; margin: 0 auto; padding: 60px 0 70px;
}
.eyebrow, .section-kicker { color: var(--accent); font-size: 13px; font-weight: 500; }
.eyebrow { display: flex; align-items: center; gap: 9px; color: var(--muted); }
.live-dot {
  width: 8px; height: 8px; border-radius: 50%; background: var(--down);
  box-shadow: 0 0 0 4px rgba(52,199,89,.18); animation: pulse 2.2s ease-in-out infinite;
}
@keyframes pulse {
  0%,100% { box-shadow: 0 0 0 4px rgba(52,199,89,.18); }
  50% { box-shadow: 0 0 0 7px rgba(52,199,89,.08); }
}
h1, h2, h3, p { margin-top: 0; }
h1 {
  margin: 22px 0; font-size: clamp(44px, 5.6vw, 76px); font-weight: 700;
  letter-spacing: -0.04em; line-height: 1.05;
}
h1 em {
  background: linear-gradient(135deg, #0071e3 0%, #42a5f5 100%);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; font-style: normal;
}
.hero-copy > p { max-width: 560px; margin-bottom: 32px; color: var(--muted); font-size: 19px; line-height: 1.5; }
.hero-actions { display: flex; gap: 16px; align-items: center; flex-wrap: wrap; }

/* ============ Hero 状态卡（深色玻璃） ============ */
.hero-status {
  position: relative; overflow: hidden; padding: 30px; border-radius: var(--radius-lg);
  background: radial-gradient(circle at 92% 8%, rgba(0,113,227,.45), transparent 40%),
    linear-gradient(160deg, #1d1d1f 0%, #2c2c2e 100%);
  box-shadow: var(--shadow-lg); color: white;
}
.hero-status::after {
  position: absolute; right: -90px; bottom: -110px; width: 280px; height: 280px;
  border: 50px solid rgba(255,255,255,.04); border-radius: 50%; content: "";
}
.status-topline, .status-foot {
  position: relative; z-index: 1; display: flex; align-items: center; justify-content: space-between;
  color: rgba(255,255,255,.7); font-size: 13px;
}
.quality-badge {
  padding: 5px 12px; border-radius: 980px; font-size: 12px; font-weight: 500;
}
.quality-badge.pass { background: rgba(52,199,89,.16); color: #7ee29a; border: 1px solid rgba(52,199,89,.3); }
.quality-badge.gaps { background: rgba(255,149,0,.16); color: #ffc580; border: 1px solid rgba(255,149,0,.3); }
.quality-badge.fail { background: rgba(255,59,48,.16); color: #ff8a80; border: 1px solid rgba(255,59,48,.3); }
.latest-date {
  position: relative; z-index: 1; margin: 16px 0 26px; padding-bottom: 20px;
  border-bottom: 1px solid rgba(255,255,255,.1); font-size: 24px; font-weight: 600; letter-spacing: -0.02em;
}
.latest-prices { position: relative; z-index: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 28px; }
.latest-prices > div + div { padding-left: 24px; border-left: 1px solid rgba(255,255,255,.1); }
.latest-prices span, .latest-prices strong, .latest-prices small { display: block; }
.latest-prices span { color: rgba(255,255,255,.6); font-size: 13px; }
.latest-prices strong { margin: 8px 0 2px; font-size: clamp(28px, 3.4vw, 38px); font-weight: 700; letter-spacing: -0.03em; }
.latest-prices small { color: rgba(255,255,255,.5); font-size: 12px; }

/* ============ 加载状态条 ============ */
.load-bar {
  width: min(var(--maxw), calc(100% - 48px)); margin: 0 auto 24px;
  padding: 14px 20px; border-radius: var(--radius-sm); background: var(--soft);
  font-size: 13px; color: var(--muted); display: flex; flex-wrap: wrap; gap: 6px 24px; align-items: center;
}
.load-bar .lbl { color: var(--subtle); }
.load-bar code { color: var(--ink); font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 12px; }
.load-bar .ok { color: var(--down); font-weight: 600; }
.load-bar .err { color: var(--danger); font-weight: 600; }

/* ============ 概览卡片 ============ */
.summary-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;
  width: min(var(--maxw), calc(100% - 48px)); margin: 0 auto 80px;
}
.metric-card {
  padding: 24px; border-radius: var(--radius); background: var(--surface);
  box-shadow: var(--shadow); min-width: 0;
}
.metric-card.primary {
  background: linear-gradient(155deg, #0071e3 0%, #42a5f5 100%); color: white;
  box-shadow: 0 12px 32px rgba(0,113,227,.22);
}
.metric-card > span, .metric-card > strong, .metric-card > small { display: block; }
.metric-card > span { color: var(--muted); font-size: 13px; }
.metric-card.primary > span { color: rgba(255,255,255,.78); }
.metric-card > strong {
  overflow: hidden; margin-top: 10px; font-size: clamp(26px, 3vw, 36px);
  font-weight: 700; letter-spacing: -0.03em; text-overflow: ellipsis;
}
.metric-card > small { margin-top: 2px; color: var(--subtle); font-size: 12px; }
.metric-card.primary > small { color: rgba(255,255,255,.7); }
.metric-card .delta { margin-top: 14px; font-size: 13px; }
.metric-card .delta.up { color: var(--up); }
.metric-card .delta.down { color: var(--down); }
.metric-card.primary .delta.up { color: #ffd67a; }
.metric-card.primary .delta.down { color: #7ee29a; }
.metric-card .null-val { color: var(--subtle); font-weight: 400; }

/* ============ 区块通用 ============ */
.section {
  width: min(var(--maxw), calc(100% - 48px)); margin: 0 auto; padding: 18px 0 80px;
}
.section-heading { display: flex; align-items: flex-end; justify-content: space-between; gap: 30px; margin-bottom: 28px; flex-wrap: wrap; }
.section-heading h2 { margin: 8px 0; font-size: clamp(28px, 3.6vw, 40px); font-weight: 700; letter-spacing: -0.035em; }
.section-heading p { margin: 0; color: var(--muted); font-size: 16px; max-width: 540px; }

/* ============ 视图切换 / 范围切换 ============ */
.tabs-row { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
.segmented {
  display: inline-flex; padding: 3px; border: 1px solid var(--line); border-radius: 980px; background: var(--soft);
}
.segmented button {
  padding: 8px 14px; border-radius: 980px; background: transparent; cursor: pointer;
  color: var(--muted); font-size: 13px; font-weight: 500; transition: all 180ms ease; white-space: nowrap;
}
.segmented button.active { background: var(--surface); box-shadow: var(--shadow-sm); color: var(--ink); font-weight: 600; }
.segmented button:hover:not(.active) { color: var(--ink); }

/* 日期范围自定义输入 */
.date-range-inputs { display: inline-flex; gap: 8px; align-items: center; font-size: 13px; color: var(--muted); }
.date-range-inputs input {
  padding: 7px 10px; border: 1px solid var(--line); border-radius: 8px;
  font-size: 13px; font-family: inherit; color: var(--ink); background: var(--surface);
}

/* ============ 图表卡 ============ */
.chart-card { overflow: hidden; border-radius: var(--radius-lg); background: var(--surface); box-shadow: var(--shadow); }
.chart-toolbar {
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
  padding: 18px 22px; border-bottom: 1px solid var(--soft); flex-wrap: wrap;
}
.legend { display: flex; gap: 14px; flex-wrap: wrap; }
.legend button { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--muted); transition: color 160ms ease; }
.legend button:hover { color: var(--ink); }
.legend button.muted { opacity: .35; }
.legend .dot { display: inline-block; width: 10px; height: 3px; border-radius: 2px; }
.chart-wrap { position: relative; padding: 18px 16px 8px; }
.price-chart { display: block; width: 100%; height: auto; min-height: 340px; overflow: visible; }
.chart-grid { stroke: #ececf0; stroke-width: 1; }
.axis-label, .date-label, .axis-unit { fill: var(--subtle); font-size: 11px; font-family: var(--font); }
.axis-label { text-anchor: end; }
.date-label { text-anchor: middle; }
.axis-unit { font-size: 10px; }
.line { fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-width: 2; vector-effect: non-scaling-stroke; }
.line.disabled { display: none; }
.hover-line { stroke: var(--subtle); stroke-dasharray: 4 4; stroke-width: 1; }
.hover-dot { stroke: white; stroke-width: 2; }
.chart-tooltip {
  position: absolute; top: 28px; z-index: 5; display: grid; gap: 6px; width: max-content;
  max-width: 280px; padding: 12px 14px; border: 1px solid var(--line); border-radius: 12px;
  background: rgba(255,255,255,.94); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  box-shadow: var(--shadow-lg); color: var(--muted); font-size: 12px; pointer-events: none;
}
.chart-tooltip.align-right { transform: translateX(calc(-100% - 10px)); }
.chart-tooltip strong { color: var(--ink); font-weight: 600; }
.chart-tooltip .tt-row { display: flex; align-items: center; gap: 7px; justify-content: space-between; }
.chart-tooltip .tt-val { color: var(--ink); font-weight: 500; }
.chart-tooltip .tt-null { color: var(--subtle); }
.loading-chart, .empty-chart { display: grid; min-height: 340px; place-items: center; color: var(--subtle); font-size: 15px; }

/* ============ 风光分项区 ============ */
.renewables-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.renewable-card { padding: 24px; border-radius: var(--radius); background: var(--surface); box-shadow: var(--shadow); }
.renewable-card h3 { margin: 0 0 4px; font-size: 17px; font-weight: 600; }
.renewable-card .sub { color: var(--subtle); font-size: 12px; margin-bottom: 16px; }
.renewable-prices { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }
.renewable-prices > div { padding: 12px; border-radius: var(--radius-sm); background: var(--soft); }
.renewable-prices span { display: block; color: var(--muted); font-size: 11px; }
.renewable-prices strong { display: block; margin-top: 4px; font-size: 22px; font-weight: 700; letter-spacing: -0.02em; }
.renewable-prices .null-val { color: var(--subtle); font-weight: 400; font-size: 18px; }
.renewable-meta { display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: 12px; color: var(--muted); }
.ocr-tag { padding: 3px 9px; border-radius: 980px; font-size: 11px; font-weight: 500; }
.ocr-tag.ok { background: rgba(52,199,89,.12); color: #1a8c3e; }
.ocr-tag.warn { background: rgba(255,149,0,.14); color: #b06700; }
.ocr-tag.fail { background: rgba(255,59,48,.12); color: #c41e14; }

/* ============ 数据表 ============ */
.table-section { width: min(var(--maxw), calc(100% - 48px)); margin: 0 auto; padding: 18px 0 80px; }
.table-toolbar { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; margin-bottom: 16px; }
.table-toolbar input[type="search"] {
  flex: 1; min-width: 180px; padding: 9px 14px; border: 1px solid var(--line); border-radius: 980px;
  font-size: 14px; font-family: inherit; background: var(--surface);
}
.table-toolbar input[type="search"]:focus { outline: none; border-color: var(--accent); }
.col-toggle { position: relative; }
.col-toggle-menu {
  position: absolute; top: calc(100% + 6px); right: 0; z-index: 20;
  min-width: 220px; max-height: 360px; overflow-y: auto; padding: 10px; border-radius: var(--radius-sm);
  background: var(--surface); box-shadow: var(--shadow-lg); border: 1px solid var(--line);
  display: none;
}
.col-toggle-menu.open { display: block; }
.col-toggle-menu label { display: flex; align-items: center; gap: 8px; padding: 6px 4px; font-size: 13px; cursor: pointer; }
.col-toggle-menu label:hover { background: var(--soft); border-radius: 6px; }
.table-wrap { overflow-x: auto; border-radius: var(--radius); background: var(--surface); box-shadow: var(--shadow); }
table { width: 100%; border-collapse: collapse; font-size: 13px; white-space: nowrap; }
th, td { padding: 12px 16px; border-bottom: 1px solid var(--soft); text-align: right; }
th { background: var(--soft); color: var(--muted); font-size: 11px; font-weight: 600; letter-spacing: .01em; position: sticky; top: 0; }
th:first-child, td:first-child { text-align: left; }
th.src, td.src { text-align: center; white-space: nowrap; }
tbody tr:last-child td { border-bottom: 0; }
tbody tr { transition: background 120ms ease; }
tbody tr:hover { background: var(--soft); }
td a { color: var(--accent); font-weight: 500; }
td a:hover { text-decoration: underline; }
td .null-cell { color: var(--subtle); }
td .src-link { display: inline-flex; align-items: center; gap: 3px; padding: 4px 8px; border-radius: 6px; font-size: 11px; }
td .src-link.snpx { background: rgba(0,113,227,.08); color: var(--accent); }
td .src-link.wechat { background: rgba(52,199,89,.08); color: #1a8c3e; }
td .src-link.missing { color: var(--subtle); background: var(--soft); cursor: default; }
.row-tag { display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 600; margin-left: 6px; }
.row-tag.orphan { background: rgba(255,149,0,.14); color: #b06700; }
.row-tag.gap { background: rgba(255,59,48,.1); color: #c41e14; }
.row-tag.review { background: rgba(90,200,250,.14); color: #0066a8; }

/* ============ 质量与异常区 ============ */
.quality-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.q-card { padding: 22px; border-radius: var(--radius); background: var(--surface); box-shadow: var(--shadow); }
.q-card h3 { margin: 0 0 12px; font-size: 15px; font-weight: 600; }
.q-list { list-style: none; padding: 0; margin: 0; font-size: 13px; }
.q-list li { display: flex; justify-content: space-between; gap: 12px; padding: 7px 0; border-bottom: 1px solid var(--soft); }
.q-list li:last-child { border-bottom: 0; }
.q-list .q-key { color: var(--muted); }
.q-list .q-val { color: var(--ink); font-weight: 500; text-align: right; }
.q-list .q-val.ok { color: var(--down); }
.q-list .q-val.warn { color: var(--warn); }
.q-list .q-val.bad { color: var(--danger); }
.q-detail { margin-top: 12px; padding: 12px; border-radius: var(--radius-sm); background: var(--soft); font-size: 12px; color: var(--muted); max-height: 180px; overflow-y: auto; }
.q-detail code { color: var(--ink); font-family: ui-monospace, "SF Mono", Menlo, monospace; }
.q-note { margin-top: 14px; padding: 12px 14px; border-radius: var(--radius-sm); background: var(--accent-soft); font-size: 12px; color: #0046a8; line-height: 1.5; }

/* ============ 数据与方法区 ============ */
.method-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.method-card { padding: 24px; border-radius: var(--radius); background: var(--surface); box-shadow: var(--shadow); }
.method-card h3 { margin: 0 0 10px; font-size: 16px; font-weight: 600; }
.method-card p, .method-card li { color: var(--muted); font-size: 13px; line-height: 1.6; }
.method-card ul { padding-left: 18px; margin: 8px 0; }
.method-card code { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 12px; color: var(--ink); background: var(--soft); padding: 1px 5px; border-radius: 4px; }
.raw-buttons { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.raw-buttons a { padding: 7px 13px; border: 1px solid var(--line); border-radius: 980px; font-size: 12px; color: var(--accent); background: var(--surface); transition: all 160ms ease; }
.raw-buttons a:hover { background: var(--accent-soft); border-color: var(--accent); }

/* ============ 加载错误屏 ============ */
.error-screen {
  width: min(var(--maxw), calc(100% - 48px)); margin: 40px auto; padding: 40px;
  border-radius: var(--radius-lg); background: var(--surface); box-shadow: var(--shadow);
  text-align: center;
}
.error-screen h2 { font-size: 28px; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 12px; }
.error-screen p { color: var(--muted); font-size: 15px; max-width: 520px; margin: 0 auto 20px; }
.error-screen .err-detail { padding: 14px; border-radius: var(--radius-sm); background: var(--soft); font-size: 12px; color: var(--danger); font-family: ui-monospace, "SF Mono", Menlo, monospace; text-align: left; max-width: 600px; margin: 0 auto 24px; word-break: break-all; }

/* ============ 下载横幅 ============ */
.download-banner {
  display: flex; align-items: center; justify-content: space-between; gap: 40px;
  width: min(var(--maxw), calc(100% - 48px)); margin: 10px auto 60px; padding: 44px 48px;
  border-radius: var(--radius-lg);
  background: radial-gradient(circle at 88% 18%, rgba(0,113,227,.5), transparent 38%),
    linear-gradient(155deg, #1d1d1f 0%, #2c2c2e 100%);
  box-shadow: var(--shadow-lg); color: white;
}
.download-banner .section-kicker { color: #6cb6ff; }
.download-banner h2 { margin-bottom: 10px; }
.download-banner p { color: rgba(255,255,255,.72); }
.btn-primary.light { flex: none; background: white; box-shadow: 0 8px 24px rgba(0,0,0,.18); color: var(--ink); }
.btn-primary.light:hover { background: #f5f5f7; }
.btn-primary.light span { margin-left: 8px; color: var(--accent); }

/* ============ 页脚 ============ */
footer {
  display: flex; align-items: center; justify-content: space-between;
  width: min(var(--maxw), calc(100% - 48px)); margin: 0 auto; padding: 24px 0 36px;
  border-top: 1px solid var(--soft); flex-wrap: wrap; gap: 16px;
}
footer p { margin: 0; color: var(--subtle); font-size: 12px; }
footer .foot-links { display: flex; gap: 18px; }
footer .foot-links a { color: var(--muted); font-size: 12px; }
footer .foot-links a:hover { color: var(--ink); text-decoration: underline; }

/* ============ 响应式 ============ */
@media (max-width: 900px) {
  nav { display: none; }
  .hero { grid-template-columns: 1fr; min-height: auto; padding-top: 40px; }
  .summary-grid { grid-template-columns: 1fr 1fr; }
  .renewables-grid, .quality-grid, .method-grid { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .site-header, .hero, .summary-grid, .section, .table-section, .download-banner, footer, .load-bar {
    width: min(100% - 32px, var(--maxw));
  }
  .site-header .btn-primary { display: none; }
  .hero { gap: 28px; padding: 30px 0 48px; }
  h1 { font-size: 38px; }
  .hero-copy > p { font-size: 16px; }
  .hero-actions { flex-direction: column; align-items: stretch; }
  .hero-status { padding: 22px; border-radius: 20px; }
  .latest-prices { gap: 14px; }
  .latest-prices > div + div { padding-left: 14px; }
  .latest-prices strong { font-size: 26px; }
  .summary-grid { grid-template-columns: 1fr; margin-bottom: 60px; }
  .section-heading { flex-direction: column; align-items: flex-start; }
  .chart-toolbar { flex-direction: column; align-items: flex-start; }
  .price-chart { min-height: 260px; }
  .download-banner { flex-direction: column; align-items: flex-start; padding: 28px 24px; }
  .btn-primary.light { width: 100%; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
"""

# JS 逻辑（运行时 fetch / 合并 / 渲染 / 交互）
JS = r"""
/* ============================================================
   陕电现货观察 — 前端逻辑
   运行时 fetch data/*.json，SHA-256 校验，渲染所有区块
   遵循需求文档：不补零、不反推、缺失显示—、来源追溯
   ============================================================ */

(function () {
  "use strict";

  // ============ 配置 ============
  // 数据源优先级：相对路径 → Pages 绝对 → Raw 绝对
  const PAGES_BASE = "https://yuanliugit.github.io/shaanxi-power-market-site/";
  const RAW_BASE = "https://raw.githubusercontent.com/yuanliugit/shaanxi-power-market-site/main/";
  const FILES = [
    { key: "manifest",    rel: "data/data_manifest.json" },
    { key: "history",     rel: "data/snpx_spot_history.json" },
    { key: "types",       rel: "data/snpx_spot_types.json" },
    { key: "windSolar",   rel: "data/wechat_wind_solar_prices.json" },
    { key: "snapshot",    rel: "data/data_snapshot.json" },
    { key: "quality",     rel: "data/snpx_quality_checks.json" },
    { key: "differences", rel: "data/snpx_source_discrepancies.json" },
    { key: "changes",     rel: "data/snpx_run_changes.json" },
  ];
  // 关键文件（失败则整批失败）；可选文件（失败只影响质量区）
  const CRITICAL = new Set(["manifest", "history", "types", "windSolar", "snapshot"]);
  const OPTIONAL = new Set(["quality", "differences", "changes"]);

  // ============ 状态 ============
  const state = {
    loaded: {},          // key → { data, url, sha256 }
    merged: [],          // 合并后的主序列
    orphans: [],         // 孤立来源记录
    duplicateErrors: [], // 重复日期错误
    activeCurves: {},    // 曲线开关
    range: "90d",        // 时间范围
    customStart: "",
    customEnd: "",
    view: "all",         // 图表视图：all / thermal / renewable / wind / solar
    search: "",
    visibleCols: {},     // 表格列开关
    chartSvg: null,
    chartW: 0, chartH: 0, chartPad: { t: 16, r: 16, b: 36, l: 48 },
  };

  // 10 条曲线定义
  const CURVES = [
    { id: "overallDa", label: "总体日前",   color: "var(--c-overall-da)", field: "overallDayAheadPrice" },
    { id: "overallRt", label: "总体实时",   color: "var(--c-overall-rt)", field: "overallRealTimePrice" },
    { id: "thermalDa", label: "火电日前",   color: "var(--c-thermal-da)", field: "thermalDayAheadPrice" },
    { id: "thermalRt", label: "火电实时",   color: "var(--c-thermal-rt)", field: "thermalRealTimePrice" },
    { id: "renewDa",   label: "新能源日前", color: "var(--c-renew-da)",   field: "renewableDayAheadPrice" },
    { id: "renewRt",   label: "新能源实时", color: "var(--c-renew-rt)",   field: "renewableRealTimePrice" },
    { id: "windDa",    label: "风电日前",   color: "var(--c-wind-da)",    field: "windDayAheadPrice" },
    { id: "windRt",    label: "风电实时",   color: "var(--c-wind-rt)",    field: "windRealTimePrice" },
    { id: "solarDa",   label: "光伏日前",   color: "var(--c-solar-da)",   field: "solarDayAheadPrice" },
    { id: "solarRt",   label: "光伏实时",   color: "var(--c-solar-rt)",   field: "solarRealTimePrice" },
  ];
  // 默认全部开启
  CURVES.forEach(c => { state.activeCurves[c.id] = true; });

  // 表格列定义
  const COLS = [
    { id: "date",          label: "日期",       always: true },
    { id: "overallDa",     label: "总体日前",   field: "overallDayAheadPrice" },
    { id: "overallRt",     label: "总体实时",   field: "overallRealTimePrice" },
    { id: "thermalDa",     label: "火电日前",   field: "thermalDayAheadPrice" },
    { id: "thermalRt",     label: "火电实时",   field: "thermalRealTimePrice" },
    { id: "renewDa",       label: "新能源日前", field: "renewableDayAheadPrice" },
    { id: "renewRt",       label: "新能源实时", field: "renewableRealTimePrice" },
    { id: "windDa",        label: "风电日前",   field: "windDayAheadPrice" },
    { id: "windRt",        label: "风电实时",   field: "windRealTimePrice" },
    { id: "solarDa",       label: "光伏日前",   field: "solarDayAheadPrice" },
    { id: "solarRt",       label: "光伏实时",   field: "solarRealTimePrice" },
    { id: "daPower",       label: "日前电量(MWh)", field: "dayAheadPower" },
    { id: "rtPower",       label: "实时电量(MWh)", field: "realTimePower" },
    { id: "ocrStatus",     label: "OCR状态" },
    { id: "src",           label: "原始来源",   always: true },
  ];
  COLS.forEach(c => { if (!c.always) state.visibleCols[c.id] = true; });

  // ============ 工具函数 ============
  function toNullableNumber(v) {
    if (v === null || v === undefined || v === "") return null;
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
  }

  function fmtNum(v, digits) {
    if (v === null || v === undefined) return "—";
    const n = toNullableNumber(v);
    if (n === null) return "—";
    return n.toLocaleString("zh-CN", { minimumFractionDigits: digits || 2, maximumFractionDigits: digits || 2 });
  }

  function fmtPower(v) {
    if (v === null || v === undefined) return "—";
    const n = toNullableNumber(v);
    if (n === null) return "—";
    // MWh，保留整数
    return Math.round(n).toLocaleString("zh-CN");
  }

  function fmtDate(d) {
    if (!d) return "—";
    return d;
  }

  // SHA-256（用 SubtleCrypto，浏览器原生）
  async function sha256Hex(text) {
    const buf = new TextEncoder().encode(text);
    const hash = await crypto.subtle.digest("SHA-256", buf);
    return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, "0")).join("");
  }

  // ============ 数据加载（带回退 + SHA-256 校验） ============
  async function fetchWithFallback(rel) {
    const urls = [
      "./" + rel,
      PAGES_BASE + rel,
      RAW_BASE + rel,
    ];
    let lastErr = null;
    for (const url of urls) {
      try {
        const resp = await fetch(url, { cache: "no-store" });
        if (!resp.ok) { lastErr = new Error("HTTP " + resp.status + " " + url); continue; }
        const text = await resp.text();
        return { text, url, data: JSON.parse(text) };
      } catch (e) {
        lastErr = e;
      }
    }
    throw lastErr || new Error("全部数据源失败：" + rel);
  }

  async function loadAll() {
    const errors = [];
    // 先加载 manifest
    let manifestInfo;
    try {
      manifestInfo = await fetchWithFallback(FILES[0].rel);
      state.loaded.manifest = { data: manifestInfo.data, url: manifestInfo.url };
    } catch (e) {
      throw new Error("数据清单（data_manifest.json）加载失败：" + e.message + "\n网页无法校验数据完整性，已停止加载。");
    }
    const manifest = manifestInfo.data;

    // 并行加载其余文件
    const rest = FILES.slice(1);
    const results = await Promise.all(rest.map(async (f) => {
      try {
        const r = await fetchWithFallback(f.rel);
        return { key: f.key, ...r, ok: true };
      } catch (e) {
        return { key: f.key, ok: false, error: e };
      }
    }));

    // 校验 SHA-256
    const hashChecks = [];
    for (const r of results) {
      if (!r.ok) {
        if (CRITICAL.has(r.key)) errors.push(r.key + " 加载失败：" + (r.error.message || r.error));
        else state.loaded[r.key] = null; // 可选文件缺失
        continue;
      }
      // 校验哈希（manifest 里有记录的）
      const mfEntry = manifest.files[r.key];
      if (mfEntry) {
        const computed = await sha256Hex(r.text);
        if (computed !== mfEntry.sha256) {
          if (CRITICAL.has(r.key)) {
            errors.push(r.key + " SHA-256 校验失败（期望 " + mfEntry.sha256.slice(0, 12) + "，实际 " + computed.slice(0, 12) + "）— 数据版本不一致，整批加载失败。");
          } else {
            state.loaded[r.key] = null; // 可选文件哈希不符，忽略
          }
          continue;
        }
      }
      state.loaded[r.key] = { data: r.data, url: r.url, sha256: mfEntry ? mfEntry.sha256 : null };
    }

    if (errors.length > 0) {
      throw new Error(errors.join("\n"));
    }
    return manifest;
  }

  // ============ 数据合并（严格遵循需求文档第七节） ============
  function mergeData() {
    const history = state.loaded.history.data;
    const types = state.loaded.types.data;
    const windSolar = state.loaded.windSolar.data;
    const byDate = new Map();
    state.orphans = [];
    state.duplicateErrors = [];

    // 1. 总体主序列（左表）
    for (const row of history.rows) {
      if (byDate.has(row.time)) {
        state.duplicateErrors.push("总体数据重复日期：" + row.time);
        continue; // 阻断该行，不静默覆盖
      }
      byDate.set(row.time, {
        date: row.time,
        officialSourceUrl: history.sourcePage,
        dayAheadPower: toNullableNumber(row.firstPower),
        realTimePower: toNullableNumber(row.secondPower),
        overallDayAheadPrice: toNullableNumber(row.firstPrice),
        overallRealTimePrice: toNullableNumber(row.secondPrice),
        thermalDayAheadPrice: null,
        thermalRealTimePrice: null,
        renewableDayAheadPrice: null,
        renewableRealTimePrice: null,
        windDayAheadPrice: null,
        windRealTimePrice: null,
        solarDayAheadPrice: null,
        solarRealTimePrice: null,
        wechatSourceUrl: null,
        ocrStatus: null,
        ocrMinConfidence: null,
        windDayAheadVolume: null,
        windRealTimeVolume: null,
        solarDayAheadVolume: null,
        solarRealTimeVolume: null,
      });
    }

    // 2. 分类型价格（火电/新能源）
    for (const row of types.rows) {
      const item = byDate.get(row.time);
      if (!item) {
        state.orphans.push({ date: row.time, source: "types", reason: "分类型中存在但主序列无此日期" });
        continue;
      }
      item.thermalDayAheadPrice = toNullableNumber(row.thirdPrice);
      item.thermalRealTimePrice = toNullableNumber(row.fourPrice);
      item.renewableDayAheadPrice = toNullableNumber(row.fivePrice);
      item.renewableRealTimePrice = toNullableNumber(row.sixPrice);
    }

    // 3. 风光分项 + OCR
    for (const row of windSolar.rows) {
      const item = byDate.get(row.date);
      if (!item) {
        state.orphans.push({ date: row.date, source: "windSolar", reason: "公众号风光中存在但主序列无此日期" });
        continue;
      }
      item.windDayAheadPrice = toNullableNumber(row.dayAhead && row.dayAhead.wind && row.dayAhead.wind.weighted);
      item.windRealTimePrice = toNullableNumber(row.realTime && row.realTime.wind && row.realTime.wind.weighted);
      item.solarDayAheadPrice = toNullableNumber(row.dayAhead && row.dayAhead.solar && row.dayAhead.solar.weighted);
      item.solarRealTimePrice = toNullableNumber(row.realTime && row.realTime.solar && row.realTime.solar.weighted);
      item.wechatSourceUrl = row.source_url || null;
      item.ocrStatus = row.overallStatus || row.status || null;
      // 最低 OCR 置信度（取四组中最低）
      const confs = [];
      ["dayAhead", "realTime"].forEach(k => {
        ["wind", "solar"].forEach(s => {
          if (row[k] && row[k][s] && row[k][s].minConfidence != null) confs.push(toNullableNumber(row[k][s].minConfidence));
        });
      });
      item.ocrMinConfidence = confs.length ? Math.min.apply(null, confs) : null;
      // 电量（公众号口径，亿千瓦时，独立展示，不混入主序列）
      item.windDayAheadVolume = toNullableNumber(row.dayAhead && row.dayAhead.wind && row.dayAhead.wind.volume);
      item.windRealTimeVolume = toNullableNumber(row.realTime && row.realTime.wind && row.realTime.wind.volume);
      item.solarDayAheadVolume = toNullableNumber(row.dayAhead && row.dayAhead.solar && row.dayAhead.solar.volume);
      item.solarRealTimeVolume = toNullableNumber(row.realTime && row.realTime.solar && row.realTime.solar.volume);
    }

    // 按日期升序
    state.merged = Array.from(byDate.values()).sort((a, b) => a.date < b.date ? -1 : a.date > b.date ? 1 : 0);
  }

  // ============ 范围筛选 ============
  function getFilteredRows() {
    const all = state.merged;
    if (!all.length) return [];
    const last = all[all.length - 1].date;
    const first = all[0].date;
    let startD = null, endD = null;

    if (state.range === "7d") {
      const d = new Date(last); d.setDate(d.getDate() - 6); startD = d.toISOString().slice(0, 10);
      endD = last;
    } else if (state.range === "30d") {
      const d = new Date(last); d.setDate(d.getDate() - 29); startD = d.toISOString().slice(0, 10);
      endD = last;
    } else if (state.range === "90d") {
      const d = new Date(last); d.setDate(d.getDate() - 89); startD = d.toISOString().slice(0, 10);
      endD = last;
    } else if (state.range === "ytd") {
      const year = last.slice(0, 4); startD = year + "-01-01"; endD = last;
    } else if (state.range === "all") {
      startD = first; endD = last;
    } else if (state.range === "custom") {
      startD = state.customStart || first;
      endD = state.customEnd || last;
    }
    return all.filter(r => r.date >= startD && r.date <= endD);
  }

  // ============ 渲染 ============
  function renderLoadBar(manifest) {
    const bar = document.getElementById("load-bar");
    const snap = state.loaded.snapshot ? state.loaded.snapshot.data : null;
    const parts = [];
    parts.push('<span class="lbl">数据版本</span><code>' + (manifest.datasetVersion || "—") + '</code>');
    if (snap) {
      parts.push('<span class="lbl">快照时间</span><code>' + (snap.generatedAt || "—") + '</code>');
    }
    parts.push('<span class="lbl">主序列最新日</span><code>' + (manifest.latestTradingDate || "—") + '</code>');
    parts.push('<span class="lbl">风光最新日</span><code>' + (manifest.latestWindSolarDate || "—") + '</code>');
    if (manifest.latestCompleteDate) {
      parts.push('<span class="lbl">共同最新日</span><code>' + manifest.latestCompleteDate + '</code>');
    }
    // 实际加载的 URL（取 manifest 的）
    parts.push('<span class="lbl">数据源</span><code>' + state.loaded.manifest.url + '</code>');
    parts.push('<span class="ok">● 已校验</span>');
    bar.innerHTML = parts.join("");
  }

  function renderHero(manifest, snap) {
    // 最新日
    document.getElementById("latest-date").textContent = manifest.latestCompleteDate || manifest.latestTradingDate || "—";
    // 质量徽章
    const badge = document.getElementById("quality-badge");
    const qg = manifest.qualityGate || (snap && snap.qualityGate);
    if (qg === "pass") {
      badge.className = "quality-badge pass"; badge.textContent = "质量通过";
    } else if (qg === "pass_with_recorded_source_gaps") {
      badge.className = "quality-badge gaps"; badge.textContent = "通过 · 存在已记录源站缺口";
    } else {
      badge.className = "quality-badge fail"; badge.textContent = "质量未通过";
    }
    // 最新价格
    const last = state.merged[state.merged.length - 1];
    if (last) {
      document.getElementById("da-price").textContent = last.overallDayAheadPrice !== null ? fmtNum(last.overallDayAheadPrice) : "—";
      document.getElementById("rt-price").textContent = last.overallRealTimePrice !== null ? fmtNum(last.overallRealTimePrice) : "—";
    }
    // 三个日期
    document.getElementById("date-trading").textContent = manifest.latestTradingDate || "—";
    document.getElementById("date-windsolar").textContent = manifest.latestWindSolarDate || "—";
    document.getElementById("date-complete").textContent = manifest.latestCompleteDate || "—";
  }

  function renderSummary(manifest, snap) {
    const last = state.merged[state.merged.length - 1];
    const prev = state.merged.length > 1 ? state.merged[state.merged.length - 2] : null;
    if (!last) return;

    // 日前价 + 涨跌
    const daEl = document.getElementById("m-da");
    const daDelta = prev && prev.overallDayAheadPrice !== null && last.overallDayAheadPrice !== null
      ? last.overallDayAheadPrice - prev.overallDayAheadPrice : null;
    daEl.querySelector("strong").textContent = last.overallDayAheadPrice !== null ? fmtNum(last.overallDayAheadPrice) : "—";
    daEl.querySelector("strong").className = last.overallDayAheadPrice === null ? "null-val" : "";
    const daDeltaEl = daEl.querySelector(".delta");
    if (daDelta !== null) {
      daDeltaEl.className = "delta " + (daDelta >= 0 ? "up" : "down");
      daDeltaEl.textContent = (daDelta >= 0 ? "▲ " : "▼ ") + fmtNum(Math.abs(daDelta)) + " 元/MWh";
    } else { daDeltaEl.textContent = "—"; }

    // 实时价
    const rtEl = document.getElementById("m-rt");
    rtEl.querySelector("strong").textContent = last.overallRealTimePrice !== null ? fmtNum(last.overallRealTimePrice) : "—";
    rtEl.querySelector("strong").className = last.overallRealTimePrice === null ? "null-val" : "";

    // 价差
    const spreadEl = document.getElementById("m-spread");
    const spread = (last.overallDayAheadPrice !== null && last.overallRealTimePrice !== null)
      ? last.overallDayAheadPrice - last.overallRealTimePrice : null;
    spreadEl.querySelector("strong").textContent = spread !== null ? fmtNum(spread) : "—";
    spreadEl.querySelector("strong").className = spread === null ? "null-val" : "";

    // 日前电量
    const daPowEl = document.getElementById("m-da-power");
    daPowEl.querySelector("strong").textContent = last.dayAheadPower !== null ? fmtPower(last.dayAheadPower) : "—";
    daPowEl.querySelector("strong").className = last.dayAheadPower === null ? "null-val" : "";

    // 实时电量
    const rtPowEl = document.getElementById("m-rt-power");
    rtPowEl.querySelector("strong").textContent = last.realTimePower !== null ? fmtPower(last.realTimePower) : "—";
    rtPowEl.querySelector("strong").className = last.realTimePower === null ? "null-val" : "";

    // 质量状态
    const qEl = document.getElementById("m-quality");
    const qg = manifest.qualityGate || (snap && snap.qualityGate);
    let qText = "—", qClass = "";
    if (qg === "pass") { qText = "通过"; qClass = "ok"; }
    else if (qg === "pass_with_recorded_source_gaps") { qText = "通过 · 有已记录缺口"; qClass = "warn"; }
    else { qText = "未通过"; qClass = "bad"; }
    qEl.querySelector("strong").textContent = qText;
    qEl.querySelector("strong").className = qClass;

    // 火电/新能源/风电/光伏 最新价
    const setCard = (id, val) => {
      const el = document.getElementById(id);
      el.querySelector("strong").textContent = val !== null ? fmtNum(val) : "—";
      el.querySelector("strong").className = val === null ? "null-val" : "";
    };
    setCard("m-thermal-da", last.thermalDayAheadPrice);
    setCard("m-renew-da", last.renewableDayAheadPrice);
    setCard("m-wind-da", last.windDayAheadPrice);
    setCard("m-solar-da", last.solarDayAheadPrice);
  }

  // ============ SVG 折线图 ============
  function renderChart() {
    const wrap = document.getElementById("chart-wrap");
    const rows = getFilteredRows();
    if (!rows.length) {
      wrap.innerHTML = '<div class="empty-chart">当前范围无数据</div>';
      return;
    }

    // 计算可见曲线的值域
    const activeCurveObjs = CURVES.filter(c => state.activeCurves[c.id]);
    let yMin = Infinity, yMax = -Infinity;
    rows.forEach(r => {
      activeCurveObjs.forEach(c => {
        const v = r[c.field];
        if (v !== null && v !== undefined) {
          if (v < yMin) yMin = v;
          if (v > yMax) yMax = v;
        }
      });
    });
    if (yMin === Infinity) { yMin = 0; yMax = 100; }
    // 留 10% 边距
    const yRange = yMax - yMin || 1;
    yMin -= yRange * 0.08; yMax += yRange * 0.08;

    // SVG 尺寸
    const W = Math.max(640, wrap.clientWidth - 32);
    const H = 360;
    const pad = state.chartPad;
    const innerW = W - pad.l - pad.r;
    const innerH = H - pad.t - pad.b;

    const xScale = i => pad.l + (rows.length === 1 ? innerW / 2 : (i / (rows.length - 1)) * innerW);
    const yScale = v => pad.t + innerH - ((v - yMin) / (yMax - yMin)) * innerH;

    // Y 轴刻度（5 条）
    const yTicks = [];
    for (let i = 0; i <= 4; i++) {
      const v = yMin + (yMax - yMin) * (i / 4);
      yTicks.push({ v, y: yScale(v) });
    }
    // X 轴刻度（约 6 个）
    const xTickIdx = [];
    const xTickCount = Math.min(6, rows.length);
    for (let i = 0; i < xTickCount; i++) {
      xTickIdx.push(Math.round(i * (rows.length - 1) / (xTickCount - 1 || 1)));
    }

    let svg = '<svg class="price-chart" viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="xMidYMid meet">';
    // 网格线 + Y 轴标签
    yTicks.forEach(t => {
      svg += '<line class="chart-grid" x1="' + pad.l + '" y1="' + t.y + '" x2="' + (W - pad.r) + '" y2="' + t.y + '"/>';
      svg += '<text class="axis-label" x="' + (pad.l - 8) + '" y="' + (t.y + 4) + '">' + Math.round(t.v) + '</text>';
    });
    svg += '<text class="axis-unit" x="' + (pad.l - 8) + '" y="' + (pad.t - 6) + '">元/MWh</text>';
    // X 轴标签
    xTickIdx.forEach(idx => {
      const x = xScale(idx);
      svg += '<text class="date-label" x="' + x + '" y="' + (H - pad.b + 18) + '">' + rows[idx].date.slice(5) + '</text>';
    });

    // 曲线（缺失值断线）
    activeCurveObjs.forEach(c => {
      let d = "";
      let pen = false;
      rows.forEach((r, i) => {
        const v = r[c.field];
        if (v === null || v === undefined) { pen = false; return; }
        const x = xScale(i), y = yScale(v);
        d += (pen ? " L" : " M") + x.toFixed(1) + " " + y.toFixed(1);
        pen = true;
      });
      svg += '<path class="line" style="stroke:' + c.color + '" d="' + d + '"/>';
    });

    // hover 层
    svg += '<line class="hover-line" id="hover-line" style="display:none"/>';
    activeCurveObjs.forEach(c => {
      svg += '<circle class="hover-dot" id="hover-dot-' + c.id + '" r="4" style="fill:' + c.color + ';display:none"/>';
    });

    // 透明 hover 捕获区
    svg += '<rect id="hover-capture" x="' + pad.l + '" y="' + pad.t + '" width="' + innerW + '" height="' + innerH + '" fill="transparent"/>';
    svg += '</svg>';

    wrap.innerHTML = svg;
    bindChartHover(rows, xScale, yScale, activeCurveObjs, W, pad);
  }

  function bindChartHover(rows, xScale, yScale, curves, W, pad) {
    const svg = wrap.querySelector("svg"); // wrap 是 chart-wrap
    const capture = document.getElementById("hover-capture");
    const tooltip = document.getElementById("chart-tooltip");
    const hline = document.getElementById("hover-line");
    const dots = {};
    curves.forEach(c => { dots[c.id] = document.getElementById("hover-dot-" + c.id); });

    function move(e) {
      const rect = svg.getBoundingClientRect();
      const scaleX = W / rect.width;
      const mx = (e.clientX - rect.left) * scaleX;
      // 找最近的数据点
      let nearestIdx = 0, nearestDist = Infinity;
      for (let i = 0; i < rows.length; i++) {
        const dx = Math.abs(xScale(i) - mx);
        if (dx < nearestDist) { nearestDist = dx; nearestIdx = i; }
      }
      const r = rows[nearestIdx];
      const x = xScale(nearestIdx);
      // 竖线
      hline.setAttribute("x1", x); hline.setAttribute("x2", x);
      hline.setAttribute("y1", pad.t); hline.setAttribute("y2", pad.t + (360 - pad.t - pad.b));
      hline.style.display = "";
      // 点 + tooltip
      let ttHtml = '<strong>' + r.date + '</strong>';
      curves.forEach(c => {
        const v = r[c.field];
        const dot = dots[c.id];
        if (v !== null && v !== undefined) {
          dot.setAttribute("cx", x); dot.setAttribute("cy", yScale(v)); dot.style.display = "";
          ttHtml += '<div class="tt-row"><span><span class="dot" style="background:' + c.color + '"></span>' + c.label + '</span><span class="tt-val">' + fmtNum(v) + '</span></div>';
        } else {
          dot.style.display = "none";
          ttHtml += '<div class="tt-row"><span><span class="dot" style="background:' + c.color + ';opacity:.4"></span>' + c.label + '</span><span class="tt-null">—</span></div>';
        }
      });
      tooltip.innerHTML = ttHtml;
      tooltip.style.display = "grid";
      // 定位 tooltip
      const wrapRect = wrap.getBoundingClientRect();
      const ttX = (e.clientX - wrapRect.left) + 14;
      const ttW = tooltip.offsetWidth;
      if (ttX + ttW > wrapRect.width) {
        tooltip.style.left = (e.clientX - wrapRect.left - ttW - 14) + "px";
        tooltip.classList.add("align-right");
      } else {
        tooltip.style.left = ttX + "px";
        tooltip.classList.remove("align-right");
      }
      tooltip.style.top = "28px";
    }
    function leave() {
      hline.style.display = "none";
      curves.forEach(c => { dots[c.id].style.display = "none"; });
      tooltip.style.display = "none";
    }
    capture.addEventListener("mousemove", move);
    capture.addEventListener("mouseleave", leave);
    // 触摸支持
    capture.addEventListener("touchmove", e => { e.preventDefault(); const t = e.touches[0]; move({ clientX: t.clientX, clientY: t.clientY }); }, { passive: false });
    capture.addEventListener("touchend", leave);
  }

  // ============ 风光分项区 ============
  function renderRenewables() {
    const rows = getFilteredRows();
    const last = rows[rows.length - 1];
    if (!last) return;

    // 风电卡
    const windCard = document.getElementById("renew-wind");
    windCard.querySelector(".da-price").textContent = last.windDayAheadPrice !== null ? fmtNum(last.windDayAheadPrice) : "—";
    windCard.querySelector(".da-price").className = last.windDayAheadPrice === null ? "da-price null-val" : "da-price";
    windCard.querySelector(".rt-price").textContent = last.windRealTimePrice !== null ? fmtNum(last.windRealTimePrice) : "—";
    windCard.querySelector(".rt-price").className = last.windRealTimePrice === null ? "rt-price null-val" : "rt-price";

    // 光伏卡
    const solarCard = document.getElementById("renew-solar");
    solarCard.querySelector(".da-price").textContent = last.solarDayAheadPrice !== null ? fmtNum(last.solarDayAheadPrice) : "—";
    solarCard.querySelector(".da-price").className = last.solarDayAheadPrice === null ? "da-price null-val" : "da-price";
    solarCard.querySelector(".rt-price").textContent = last.solarRealTimePrice !== null ? fmtNum(last.solarRealTimePrice) : "—";
    solarCard.querySelector(".rt-price").className = last.solarRealTimePrice === null ? "rt-price null-val" : "rt-price";

    // OCR 状态 + 公众号链接
    [windCard, solarCard].forEach((card, idx) => {
      const ocrTag = card.querySelector(".ocr-tag");
      const conf = last.ocrMinConfidence;
      if (last.ocrStatus === "ok") { ocrTag.className = "ocr-tag ok"; ocrTag.textContent = "OCR 正常"; }
      else if (last.ocrStatus) { ocrTag.className = "ocr-tag warn"; ocrTag.textContent = "OCR：" + last.ocrStatus; }
      else { ocrTag.className = "ocr-tag fail"; ocrTag.textContent = "无 OCR"; }
      const confEl = card.querySelector(".ocr-conf");
      confEl.textContent = conf !== null ? "最低置信度 " + (conf * 100).toFixed(1) + "%" : "—";
      // 公众号链接
      const linkEl = card.querySelector(".wechat-link");
      if (last.wechatSourceUrl) {
        linkEl.innerHTML = '<a href="' + last.wechatSourceUrl + '" target="_blank" rel="noopener noreferrer">公众号日报 ↗</a>';
      } else {
        linkEl.innerHTML = '<span class="null-cell">未取得日报</span>';
      }
    });
  }

  // ============ 数据表 ============
  function renderTable() {
    const tbody = document.getElementById("table-body");
    let rows = getFilteredRows().slice().reverse(); // 倒序
    if (state.search) {
      rows = rows.filter(r => r.date.indexOf(state.search) >= 0);
    }
    // 限制最多 500 行（性能）
    const MAX = 500;
    const truncated = rows.length > MAX;
    rows = rows.slice(0, MAX);

    // 已知缺失/缺口/复核集合（从 quality 文件）
    const gaps = state.loaded.quality ? (state.loaded.quality.data.qualityGate.recordedSourceGaps || []) : [];
    const reviewDates = state.loaded.quality ? (state.loaded.quality.data.wechat.ocrReviewDates || []) : [];
    const gapDates = new Set();
    gaps.forEach(g => { const d = g.split(":")[0]; if (d) gapDates.add(d); });

    const html = rows.map(r => {
      let cells = "";
      // 日期 + 标签
      let tags = "";
      if (gapDates.has(r.date)) tags += '<span class="row-tag gap">缺口</span>';
      if (reviewDates.indexOf(r.date) >= 0) tags += '<span class="row-tag review">待复核</span>';
      cells += '<td>' + r.date + tags + '</td>';
      // 各价格列
      COLS.forEach(c => {
        if (c.always || c.id === "src") return;
        if (!state.visibleCols[c.id]) return;
        if (c.id === "ocrStatus") {
          const s = r.ocrStatus;
          let t = '<span class="null-cell">—</span>';
          if (s === "ok") t = '<span class="ocr-tag ok">正常</span>';
          else if (s) t = '<span class="ocr-tag warn">' + s + '</span>';
          cells += '<td>' + t + '</td>';
          return;
        }
        if (c.field) {
          const v = r[c.field];
          if (c.id === "daPower" || c.id === "rtPower") {
            cells += '<td>' + (v !== null ? fmtPower(v) : '<span class="null-cell">—</span>') + '</td>';
          } else {
            cells += '<td>' + (v !== null ? fmtNum(v) : '<span class="null-cell">—</span>') + '</td>';
          }
        }
      });
      // 来源链接
      let src = "";
      src += '<a class="src-link snpx" href="' + r.officialSourceUrl + '" target="_blank" rel="noopener noreferrer" title="交易中心公开页面">交易中心 ↗</a>';
      if (r.wechatSourceUrl) {
        src += ' <a class="src-link wechat" href="' + r.wechatSourceUrl + '" target="_blank" rel="noopener noreferrer" title="公众号日报原文">公众号 ↗</a>';
      } else {
        src += ' <span class="src-link missing">未取得日报</span>';
      }
      cells += '<td class="src">' + src + '</td>';
      return '<tr>' + cells + '</tr>';
    }).join("");

    let note = truncated ? '<tr><td colspan="20" style="text-align:center;color:var(--subtle);padding:16px">仅显示最近 ' + MAX + ' 行，共 ' + rows.length + ' 条匹配（使用日期搜索缩小范围）</td></tr>' : "";
    tbody.innerHTML = html + note;
  }

  // ============ 质量与异常区 ============
  function renderQuality(manifest) {
    const q = state.loaded.quality ? state.loaded.quality.data : null;
    const d = state.loaded.differences ? state.loaded.differences.data : null;
    const c = state.loaded.changes ? state.loaded.changes.data : null;
    const snap = state.loaded.snapshot ? state.loaded.snapshot.data : null;

    // 门禁卡
    const gateEl = document.getElementById("q-gate");
    if (q) {
      const status = q.qualityGate.status;
      let cls = "ok", text = "通过";
      if (status === "pass_with_recorded_source_gaps") { cls = "warn"; text = "通过，但存在已记录的源站缺口"; }
      else if (status !== "pass") { cls = "bad"; text = status; }
      let html = '<h3>质量门禁</h3><ul class="q-list">';
      html += '<li><span class="q-key">门禁状态</span><span class="q-val ' + cls + '">' + text + '</span></li>';
      html += '<li><span class="q-key">阻断问题</span><span class="q-val ' + (q.qualityGate.blockingIssues.length ? "bad" : "ok") + '">' + q.qualityGate.blockingIssues.length + ' 项</span></li>';
      html += '<li><span class="q-key">已记录源站缺口</span><span class="q-val ' + (q.qualityGate.recordedSourceGaps.length ? "warn" : "ok") + '">' + q.qualityGate.recordedSourceGaps.length + ' 项</span></li>';
      html += '<li><span class="q-key">禁止自动补零</span><span class="q-val ' + (q.noAutoZeroFill ? "ok" : "bad") + '">' + (q.noAutoZeroFill ? "是（noAutoZeroFill=true）" : "否") + '</span></li>';
      html += '</ul>';
      if (q.qualityGate.recordedSourceGaps.length) {
        html += '<div class="q-detail">缺口明细：<br>' + q.qualityGate.recordedSourceGaps.map(g => '<code>' + g + '</code>').join("<br>") + '</div>';
      }
      html += '<div class="q-note">双源差异只记录，不覆盖主序列。缺失值显示"—"，不自动填 0。</div>';
      gateEl.innerHTML = html;
    } else {
      gateEl.innerHTML = '<h3>质量门禁</h3><p style="color:var(--subtle);font-size:13px">质量检查文件不可用</p>';
    }

    // 日期与行数卡
    const rangeEl = document.getElementById("q-range");
    if (q) {
      let html = '<h3>日期范围与行数</h3><ul class="q-list">';
      html += '<li><span class="q-key">总体日期范围</span><span class="q-val">' + (q.website.dateRange.join(" ~ ")) + '</span></li>';
      html += '<li><span class="q-key">总体行数</span><span class="q-val">' + q.website.historyRows + '</span></li>';
      html += '<li><span class="q-key">分类型行数</span><span class="q-val">' + q.website.typeRows + '</span></li>';
      html += '<li><span class="q-key">重复日期（总体）</span><span class="q-val ' + (q.website.duplicateHistoryDates.length ? "bad" : "ok") + '">' + q.website.duplicateHistoryDates.length + '</span></li>';
      html += '<li><span class="q-key">重复日期（分类型）</span><span class="q-val ' + (q.website.duplicateTypeDates.length ? "bad" : "ok") + '">' + q.website.duplicateTypeDates.length + '</span></li>';
      html += '<li><span class="q-key">缺失日期</span><span class="q-val ' + (q.website.missingDates.length ? "warn" : "ok") + '">' + q.website.missingDates.length + '</span></li>';
      html += '<li><span class="q-key">已知缺失字段（总体）</span><span class="q-val ' + (q.website.knownMissingHistoryFields.length ? "warn" : "ok") + '">' + q.website.knownMissingHistoryFields.length + '</span></li>';
      html += '<li><span class="q-key">价格范围错误</span><span class="q-val ' + (q.website.priceRangeErrors.length ? "bad" : "ok") + '">' + q.website.priceRangeErrors.length + '</span></li>';
      html += '<li><span class="q-key">风光日期范围</span><span class="q-val">' + (q.wechat.windSolarRange.join(" ~ ")) + '</span></li>';
      html += '<li><span class="q-key">风光行数</span><span class="q-val">' + q.wechat.windSolarRows + '</span></li>';
      html += '<li><span class="q-key">OCR 缺口日期</span><span class="q-val ' + (q.wechat.missingOcrDates.length ? "warn" : "ok") + '">' + q.wechat.missingOcrDates.length + '</span></li>';
      html += '<li><span class="q-key">OCR 待复核</span><span class="q-val ' + (q.wechat.ocrReviewDates.length ? "warn" : "ok") + '">' + q.wechat.ocrReviewDates.length + '</span></li>';
      html += '<li><span class="q-key">最低 OCR 置信度</span><span class="q-val">' + (q.wechat.minOcrConfidence !== null && q.wechat.minOcrConfidence !== undefined ? (q.wechat.minOcrConfidence * 100).toFixed(2) + "%" : "—") + '</span></li>';
      html += '</ul>';
      rangeEl.innerHTML = html;
    }

    // 双源差异卡
    const diffEl = document.getElementById("q-diff");
    if (d) {
      let html = '<h3>双源差异</h3><ul class="q-list">';
      html += '<li><span class="q-key">价格阈值</span><span class="q-val">' + d.thresholds.priceCnyPerMWh + ' 元/MWh</span></li>';
      html += '<li><span class="q-key">电量阈值</span><span class="q-val">' + d.thresholds.powerPercent + '%</span></li>';
      html += '<li><span class="q-key">重叠日数</span><span class="q-val">' + d.overlapDays + '</span></li>';
      html += '<li><span class="q-key">超阈值日数</span><span class="q-val ' + (d.overThresholdDays > 0 ? "warn" : "ok") + '">' + d.overThresholdDays + '</span></li>';
      html += '</ul>';
      html += '<div class="q-note">差异主要为电量单位不同（交易中心 MWh vs 公众号亿千瓦时），价格差异多为 0。差异只记录，不覆盖主序列。</div>';
      diffEl.innerHTML = html;
    }

    // 变更记录卡
    const chgEl = document.getElementById("q-changes");
    if (c) {
      let html = '<h3>本次更新变更</h3><ul class="q-list">';
      const cats = [["websiteHistory", "总体"], ["websiteTypes", "分类型"], ["wechatArticles", "公众号文章"], ["windSolar", "风光分项"]];
      cats.forEach(([k, label]) => {
        const s = c[k];
        html += '<li><span class="q-key">' + label + ' 新增/修订/删除</span><span class="q-val">' + s.added.length + ' / ' + s.revised.length + ' / ' + s.removed.length + '</span></li>';
      });
      html += '</ul>';
      html += '<div class="q-detail">生成时间：' + c.generatedAt + '</div>';
      chgEl.innerHTML = html;
    }

    // 孤立来源记录
    const orphanEl = document.getElementById("q-orphans");
    let oHtml = '<h3>孤立来源记录</h3>';
    if (state.orphans.length) {
      oHtml += '<ul class="q-list">';
      state.orphans.forEach(o => {
        oHtml += '<li><span class="q-key">' + o.date + '（' + o.source + '）</span><span class="q-val warn">' + o.reason + '</span></li>';
      });
      oHtml += '</ul>';
    } else {
      oHtml += '<ul class="q-list"><li><span class="q-key">孤立记录</span><span class="q-val ok">无</span></li></ul>';
    }
    if (state.duplicateErrors.length) {
      oHtml += '<div class="q-detail" style="color:var(--danger)">重复日期错误：<br>' + state.duplicateErrors.map(e => '<code>' + e + '</code>').join("<br>") + '</div>';
    }
    orphanEl.innerHTML = oHtml;
  }

  // ============ 数据与方法区 ============
  function renderMethod(manifest) {
    const snpxUrl = state.loaded.history ? state.loaded.history.data.sourcePage : "https://snpx.com.cn/#/home/marketData/transactionData/spotmarketsection";
    const lastWindSolarRow = state.merged.slice().reverse().find(r => r.wechatSourceUrl);
    const latestWechatUrl = lastWindSolarRow ? lastWindSolarRow.wechatSourceUrl : null;

    const wechatLinkEl = document.getElementById("latest-wechat-link");
    if (latestWechatUrl) {
      wechatLinkEl.innerHTML = '<a href="' + latestWechatUrl + '" target="_blank" rel="noopener noreferrer">' + latestWechatUrl.slice(0, 60) + '...</a>';
    } else {
      wechatLinkEl.innerHTML = '<span class="null-cell">未取得原文</span>';
    }
    document.getElementById("snpx-link").innerHTML = '<a href="' + snpxUrl + '" target="_blank" rel="noopener noreferrer">' + snpxUrl + '</a>';
  }

  // ============ CSV 导出 ============
  function exportCSV() {
    const rows = getFilteredRows();
    const headers = ["日期", "总体日前(元/MWh)", "总体实时(元/MWh)", "火电日前(元/MWh)", "火电实时(元/MWh)", "新能源日前(元/MWh)", "新能源实时(元/MWh)", "风电日前(元/MWh)", "风电实时(元/MWh)", "光伏日前(元/MWh)", "光伏实时(元/MWh)", "日前电量(MWh)", "实时电量(MWh)", "OCR状态", "交易中心链接", "公众号链接"];
    const lines = [headers.join(",")];
    rows.forEach(r => {
      const vals = [
        r.date,
        r.overallDayAheadPrice, r.overallRealTimePrice,
        r.thermalDayAheadPrice, r.thermalRealTimePrice,
        r.renewableDayAheadPrice, r.renewableRealTimePrice,
        r.windDayAheadPrice, r.windRealTimePrice,
        r.solarDayAheadPrice, r.solarRealTimePrice,
        r.dayAheadPower, r.realTimePower,
        r.ocrStatus || "",
        r.officialSourceUrl || "",
        r.wechatSourceUrl || "",
      ];
      lines.push(vals.map(v => v === null || v === undefined ? "" : String(v)).map(v => '"' + v.replace(/"/g, '""') + '"').join(","));
    });
    const csv = "\ufeff" + lines.join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "陕电现货_" + (state.range) + "_" + new Date().toISOString().slice(0, 10) + ".csv";
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  // ============ 交互绑定 ============
  function renderTableHead() {
    const head = document.getElementById("table-head");
    let html = "<tr>";
    COLS.forEach(c => {
      if (c.always || c.id === "src") {
        html += '<th class="' + (c.id === "src" ? "src" : "") + '">' + c.label + '</th>';
      } else if (state.visibleCols[c.id]) {
        html += '<th>' + c.label + '</th>';
      }
    });
    html += "</tr>";
    head.innerHTML = html;

    // 列选择菜单
    const menu = document.getElementById("col-menu");
    let mHtml = "";
    COLS.forEach(c => {
      if (c.always) return;
      mHtml += '<label><input type="checkbox" data-col="' + c.id + '" ' + (state.visibleCols[c.id] ? "checked" : "") + '> ' + c.label + '</label>';
    });
    menu.innerHTML = mHtml;
  }

  function bindInteractions() {
    // 范围切换
    document.querySelectorAll(".range-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".range-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        state.range = btn.dataset.range;
        document.getElementById("date-custom").style.display = state.range === "custom" ? "inline-flex" : "none";
        renderChart(); renderRenewables(); renderTable();
      });
    });
    document.getElementById("custom-start").addEventListener("change", e => { state.customStart = e.target.value; renderChart(); renderRenewables(); renderTable(); });
    document.getElementById("custom-end").addEventListener("change", e => { state.customEnd = e.target.value; renderChart(); renderRenewables(); renderTable(); });

    // 曲线开关
    document.querySelectorAll(".legend button").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.dataset.curve;
        state.activeCurves[id] = !state.activeCurves[id];
        btn.classList.toggle("muted", !state.activeCurves[id]);
        renderChart();
      });
    });

    // 视图预设
    document.querySelectorAll(".view-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".view-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        const v = btn.dataset.view;
        const presets = {
          all: CURVES.map(c => c.id),
          overall: ["overallDa", "overallRt"],
          thermal: ["thermalDa", "thermalRt"],
          renewable: ["renewDa", "renewRt"],
          wind: ["windDa", "windRt"],
          solar: ["solarDa", "solarRt"],
        };
        const active = presets[v] || presets.all;
        CURVES.forEach(c => { state.activeCurves[c.id] = active.indexOf(c.id) >= 0; });
        document.querySelectorAll(".legend button").forEach(b => {
          b.classList.toggle("muted", !state.activeCurves[b.dataset.curve]);
        });
        renderChart();
      });
    });

    // 搜索
    document.getElementById("table-search").addEventListener("input", e => { state.search = e.target.value; renderTable(); });

    // 列选择
    const colBtn = document.getElementById("col-toggle-btn");
    const colMenu = document.getElementById("col-menu");
    colBtn.addEventListener("click", e => { e.stopPropagation(); colMenu.classList.toggle("open"); });
    document.addEventListener("click", () => colMenu.classList.remove("open"));
    colMenu.addEventListener("click", e => e.stopPropagation());
    colMenu.querySelectorAll("input").forEach(cb => {
      cb.addEventListener("change", () => {
        state.visibleCols[cb.dataset.col] = cb.checked;
        renderTableHead();
        renderTable();
      });
    });

    // CSV 导出
    document.getElementById("csv-export").addEventListener("click", exportCSV);

    // 重载
    document.getElementById("reload-btn").addEventListener("click", () => location.reload());

    // 窗口 resize 重绘图表
    let resizeTimer;
    window.addEventListener("resize", () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(renderChart, 200);
    });
  }

  // ============ 错误屏 ============
  function showError(msg) {
    document.getElementById("main-content").style.display = "none";
    const screen = document.getElementById("error-screen");
    screen.style.display = "block";
    document.getElementById("err-detail").textContent = msg;
  }

  // ============ 入口 ============
  async function init() {
    try {
      const manifest = await loadAll();
      mergeData();
      if (state.duplicateErrors.length) {
        // 重复日期阻断，但仍渲染（已跳过重复行）
        console.warn("重复日期：", state.duplicateErrors);
      }
      renderLoadBar(manifest);
      const snap = state.loaded.snapshot ? state.loaded.snapshot.data : null;
      renderHero(manifest, snap);
      renderSummary(manifest, snap);
      renderTableHead();
      renderChart();
      renderRenewables();
      renderTable();
      renderQuality(manifest);
      renderMethod(manifest);
      bindInteractions();
      document.getElementById("main-content").style.display = "";
    } catch (e) {
      console.error(e);
      showError(e.message || String(e));
    }
  }

  // 暴露 wrap 给 bindChartHover 用
  var wrap = null;
  document.addEventListener("DOMContentLoaded", () => {
    wrap = document.getElementById("chart-wrap");
    init();
  });
})();
"""

# HTML 结构
HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>陕电现货观察</title>
<meta name="description" content="陕西电力现货市场每日出清价格跟踪 — 总体、火电、新能源、风电、光伏价格与电量">
<style>
__CSS__
</style>
</head>
<body>

<header class="site-header">
  <a class="brand" href="#">
    <span class="brand-mark">陕</span>
    <span>
      <b>陕电现货观察</b>
      <small>Shaanxi Power Spot Market</small>
    </span>
  </a>
  <nav>
    <a href="#overview">概览</a>
    <a href="#prices">价格趋势</a>
    <a href="#renewables">风光分项</a>
    <a href="#table">每日数据</a>
    <a href="#quality">数据质量</a>
    <a href="#method">数据与方法</a>
  </nav>
  <a class="btn-primary compact" href="./downloads/陕西现货市场每日出清价格跟踪_2025至今_含风光分项.xlsx">下载 Excel</a>
</header>

<main id="main-content" style="display:none">

  <!-- Hero -->
  <section class="hero" id="overview">
    <div class="hero-copy">
      <span class="eyebrow"><span class="live-dot"></span>陕西电力现货市场 · 每日更新</span>
      <h1>看见<em>陕电现货</em>的每一天</h1>
      <p>跟踪陕西电力现货市场每日出清价格与电量，覆盖总体、火电、新能源、风电、光伏五类口径。数据来自交易中心公开页面与公众号日报，所有数值均可追溯至原始来源。</p>
      <div class="hero-actions">
        <a class="btn-primary" href="#prices">查看价格趋势</a>
        <a class="btn-outline" href="#method">数据与方法</a>
      </div>
    </div>
    <div class="hero-status">
      <div class="status-topline">
        <span>最新观测</span>
        <span class="quality-badge gaps" id="quality-badge">—</span>
      </div>
      <div class="latest-date" id="latest-date">加载中…</div>
      <div class="latest-prices">
        <div>
          <span>总体日前加权均价</span>
          <strong id="da-price">—</strong>
          <small>元/MWh</small>
        </div>
        <div>
          <span>总体实时加权均价</span>
          <strong id="rt-price">—</strong>
          <small>元/MWh</small>
        </div>
      </div>
      <div class="status-foot">
        <span>主序列最新：<code id="date-trading" style="font-family:inherit">—</code></span>
        <span>风光最新：<code id="date-windsolar" style="font-family:inherit">—</code></span>
        <span>共同最新：<code id="date-complete" style="font-family:inherit">—</code></span>
      </div>
    </div>
  </section>

  <!-- 加载状态条 -->
  <div class="load-bar" id="load-bar">
    <span class="lbl">正在加载数据…</span>
  </div>

  <!-- 概览卡片 -->
  <section class="summary-grid">
    <div class="metric-card primary" id="m-da">
      <span>总体日前加权均价</span>
      <strong>—</strong>
      <small>元/MWh · 最新交易日</small>
      <div class="delta">—</div>
    </div>
    <div class="metric-card" id="m-rt">
      <span>总体实时加权均价</span>
      <strong>—</strong>
      <small>元/MWh · 最新交易日</small>
    </div>
    <div class="metric-card" id="m-spread">
      <span>日前—实时价差</span>
      <strong>—</strong>
      <small>元/MWh · 正值=日前高于实时</small>
    </div>
    <div class="metric-card" id="m-quality">
      <span>数据质量状态</span>
      <strong>—</strong>
      <small>质量门禁</small>
    </div>
    <div class="metric-card" id="m-da-power">
      <span>日前出清电量</span>
      <strong>—</strong>
      <small>MWh · 交易中心口径</small>
    </div>
    <div class="metric-card" id="m-rt-power">
      <span>实时出清电量</span>
      <strong>—</strong>
      <small>MWh · 交易中心口径</small>
    </div>
    <div class="metric-card" id="m-thermal-da">
      <span>火电日前均价</span>
      <strong>—</strong>
      <small>元/MWh · 最新交易日</small>
    </div>
    <div class="metric-card" id="m-renew-da">
      <span>新能源日前均价</span>
      <strong>—</strong>
      <small>元/MWh · 最新交易日</small>
    </div>
    <div class="metric-card" id="m-wind-da">
      <span>风电日前均价</span>
      <strong>—</strong>
      <small>元/MWh · 公众号口径</small>
    </div>
    <div class="metric-card" id="m-solar-da">
      <span>光伏日前均价</span>
      <strong>—</strong>
      <small>元/MWh · 公众号口径</small>
    </div>
  </section>

  <!-- 价格趋势 -->
  <section class="section" id="prices">
    <div class="section-heading">
      <div>
        <span class="section-kicker">价格趋势</span>
        <h2>十类出清价格</h2>
        <p>总体、火电、新能源、风电、光伏的日前与实时加权均价。缺失值断线，不补零。点击图例可隐藏/显示。</p>
      </div>
    </div>
    <div class="chart-card">
      <div class="chart-toolbar">
        <div class="legend" id="legend">
          <button data-curve="overallDa"><span class="dot" style="background:var(--c-overall-da)"></span>总体日前</button>
          <button data-curve="overallRt"><span class="dot" style="background:var(--c-overall-rt)"></span>总体实时</button>
          <button data-curve="thermalDa"><span class="dot" style="background:var(--c-thermal-da)"></span>火电日前</button>
          <button data-curve="thermalRt"><span class="dot" style="background:var(--c-thermal-rt)"></span>火电实时</button>
          <button data-curve="renewDa"><span class="dot" style="background:var(--c-renew-da)"></span>新能源日前</button>
          <button data-curve="renewRt"><span class="dot" style="background:var(--c-renew-rt)"></span>新能源实时</button>
          <button data-curve="windDa"><span class="dot" style="background:var(--c-wind-da)"></span>风电日前</button>
          <button data-curve="windRt"><span class="dot" style="background:var(--c-wind-rt)"></span>风电实时</button>
          <button data-curve="solarDa"><span class="dot" style="background:var(--c-solar-da)"></span>光伏日前</button>
          <button data-curve="solarRt"><span class="dot" style="background:var(--c-solar-rt)"></span>光伏实时</button>
        </div>
        <div class="tabs-row">
          <div class="segmented">
            <button class="view-btn active" data-view="all">全部</button>
            <button class="view-btn" data-view="overall">总体</button>
            <button class="view-btn" data-view="thermal">火电</button>
            <button class="view-btn" data-view="renewable">新能源</button>
            <button class="view-btn" data-view="wind">风电</button>
            <button class="view-btn" data-view="solar">光伏</button>
          </div>
        </div>
      </div>
      <div class="chart-toolbar" style="border-bottom:1px solid var(--soft)">
        <div class="segmented">
          <button class="range-btn" data-range="7d">近7天</button>
          <button class="range-btn active" data-range="30d">近30天</button>
          <button class="range-btn" data-range="90d">近90天</button>
          <button class="range-btn" data-range="ytd">今年</button>
          <button class="range-btn" data-range="all">全部</button>
          <button class="range-btn" data-range="custom">自定义</button>
        </div>
        <div class="date-range-inputs" id="date-custom" style="display:none">
          <input type="date" id="custom-start">
          <span>至</span>
          <input type="date" id="custom-end">
        </div>
      </div>
      <div class="chart-wrap" id="chart-wrap">
        <div class="loading-chart">加载中…</div>
        <div class="chart-tooltip" id="chart-tooltip" style="display:none"></div>
      </div>
    </div>
  </section>

  <!-- 风光分项 -->
  <section class="section" id="renewables">
    <div class="section-heading">
      <div>
        <span class="section-kicker">风光分项</span>
        <h2>风电与光伏</h2>
        <p>来自公众号日报口径，含 OCR 识别状态与最低置信度。公众号电量单位为亿千瓦时，独立展示，不与交易中心电量混并。</p>
      </div>
    </div>
    <div class="renewables-grid">
      <div class="renewable-card" id="renew-wind">
        <h3>风电</h3>
        <div class="sub">公众号口径 · 加权均价（元/MWh）</div>
        <div class="renewable-prices">
          <div><span>日前</span><strong class="da-price">—</strong></div>
          <div><span>实时</span><strong class="rt-price">—</strong></div>
        </div>
        <div class="renewable-meta">
          <span class="ocr-tag ok">OCR 正常</span>
          <span class="ocr-conf">最低置信度 —</span>
          <span class="wechat-link"></span>
        </div>
      </div>
      <div class="renewable-card" id="renew-solar">
        <h3>光伏</h3>
        <div class="sub">公众号口径 · 加权均价（元/MWh）</div>
        <div class="renewable-prices">
          <div><span>日前</span><strong class="da-price">—</strong></div>
          <div><span>实时</span><strong class="rt-price">—</strong></div>
        </div>
        <div class="renewable-meta">
          <span class="ocr-tag ok">OCR 正常</span>
          <span class="ocr-conf">最低置信度 —</span>
          <span class="wechat-link"></span>
        </div>
      </div>
    </div>
  </section>

  <!-- 每日数据表 -->
  <section class="table-section" id="table">
    <div class="section-heading">
      <div>
        <span class="section-kicker">每日数据</span>
        <h2>明细表</h2>
        <p>按日期倒序，缺失值显示"—"。每行提供交易中心和公众号原文追溯链接。</p>
      </div>
      <div class="tabs-row">
        <button class="btn-outline compact" id="csv-export">导出当前范围 CSV</button>
        <div class="col-toggle">
          <button class="btn-outline compact" id="col-toggle-btn">选择列 ▾</button>
          <div class="col-toggle-menu" id="col-menu"></div>
        </div>
      </div>
    </div>
    <div class="table-toolbar">
      <input type="search" id="table-search" placeholder="搜索日期（如 2026-07）…">
    </div>
    <div class="table-wrap">
      <table>
        <thead id="table-head"></thead>
        <tbody id="table-body">
          <tr><td colspan="20" style="text-align:center;color:var(--subtle);padding:24px">加载中…</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <!-- 质量与异常 -->
  <section class="section" id="quality">
    <div class="section-heading">
      <div>
        <span class="section-kicker">数据质量</span>
        <h2>质量与异常</h2>
        <p>门禁状态、日期范围、重复/缺失、价格范围错误、OCR 复核、双源差异、变更记录。</p>
      </div>
    </div>
    <div class="quality-grid">
      <div class="q-card" id="q-gate"></div>
      <div class="q-card" id="q-range"></div>
      <div class="q-card" id="q-diff"></div>
      <div class="q-card" id="q-changes"></div>
      <div class="q-card" id="q-orphans"></div>
    </div>
  </section>

  <!-- 数据与方法 -->
  <section class="section" id="method">
    <div class="section-heading">
      <div>
        <span class="section-kicker">来源追溯</span>
        <h2>数据与方法</h2>
        <p>网站只读取已公开的静态 JSON，不直接访问交易中心或公众号。所有链接仅供追溯核验。</p>
      </div>
    </div>
    <div class="method-grid">
      <div class="method-card">
        <h3>基础数据源</h3>
        <p>网站运行时只读取 <code>./data/*.json</code>，由上游 Codex 自动化生成并经质量检查后发布。网页不调用交易中心接口，不抓取公众号文章。</p>
        <div class="raw-buttons">
          <a href="./data/snpx_spot_history.json" target="_blank" rel="noopener noreferrer">总体 JSON</a>
          <a href="./data/snpx_spot_types.json" target="_blank" rel="noopener noreferrer">分类型 JSON</a>
          <a href="./data/wechat_wind_solar_prices.json" target="_blank" rel="noopener noreferrer">风光/OCR JSON</a>
          <a href="./data/data_snapshot.json" target="_blank" rel="noopener noreferrer">质量快照</a>
          <a href="./data/data_manifest.json" target="_blank" rel="noopener noreferrer">数据清单</a>
          <a href="./data/snpx_quality_checks.json" target="_blank" rel="noopener noreferrer">质量检查</a>
          <a href="./data/snpx_source_discrepancies.json" target="_blank" rel="noopener noreferrer">双源差异</a>
          <a href="./data/snpx_run_changes.json" target="_blank" rel="noopener noreferrer">变更记录</a>
          <a href="./downloads/陕西现货市场每日出清价格跟踪_2025至今_含风光分项.xlsx" target="_blank" rel="noopener noreferrer">完整 Excel</a>
        </div>
      </div>
      <div class="method-card">
        <h3>追溯链接</h3>
        <p><strong>交易中心公开页面：</strong><span id="snpx-link">—</span></p>
        <p><strong>最新公众号日报：</strong><span id="latest-wechat-link">—</span></p>
        <p style="margin-top:12px"><strong>口径说明：</strong></p>
        <ul>
          <li>总体、火电、新能源价格及总体电量 → 交易中心口径</li>
          <li>风电、光伏分项及 OCR 字段 → 公众号日报口径</li>
          <li>双源差异由上游自动化计算并记录，网页只展示</li>
        </ul>
      </div>
      <div class="method-card">
        <h3>核心规则</h3>
        <ul>
          <li>不反推：不用新能源合计减光伏得风电</li>
          <li>不补零：<code>null</code>/空值显示"—"，图表断线</li>
          <li>不覆盖：公众号总体值不覆盖交易中心总体值</li>
          <li>不取数：追溯链接仅供用户点击核验，不参与网页取数</li>
          <li>不混并：公众号电量独立展示，不并入交易中心主序列</li>
        </ul>
      </div>
      <div class="method-card">
        <h3>数据完整性</h3>
        <p>每次发布通过 <code>data_manifest.json</code> 绑定同一批次的所有文件 SHA-256。前端加载时逐文件校验哈希，任一不符则整批加载失败，不跨版本混合展示。</p>
        <p style="margin-top:10px">质量门禁仅以下状态允许发布：<code>pass</code> / <code>pass_with_recorded_source_gaps</code>。失败时保留上一版已发布数据。</p>
      </div>
    </div>
  </section>

  <!-- 下载横幅 -->
  <section class="download-banner">
    <div>
      <span class="section-kicker">完整数据集</span>
      <h2>下载完整 Excel 底表</h2>
      <p>含全部交易日、五类价格、电量、风光分项与 OCR 字段，可用于人工复核与离线分析。</p>
    </div>
    <a class="btn-primary light" href="./downloads/陕西现货市场每日出清价格跟踪_2025至今_含风光分项.xlsx">下载 Excel<span>↗</span></a>
  </section>

</main>

<!-- 加载错误屏 -->
<div class="error-screen" id="error-screen" style="display:none">
  <h2>数据加载失败</h2>
  <p>网页无法加载或校验基础数据。请检查网络连接或稍后重试。所有数据文件必须属于同一质量检查批次，SHA-256 校验通过后才会展示。</p>
  <div class="err-detail" id="err-detail"></div>
  <button class="btn-primary" id="reload-btn">重新加载</button>
</div>

<footer>
  <p>陕电现货观察 · 数据来自陕西电力交易中心公开页面与公众号日报 · 仅供研究参考</p>
  <div class="foot-links">
    <a href="./data/data_manifest.json" target="_blank" rel="noopener noreferrer">数据清单</a>
    <a href="https://github.com/yuanliugit/shaanxi-power-market-site" target="_blank" rel="noopener noreferrer">GitHub 仓库</a>
  </div>
</footer>

<script>
__JS__
</script>
</body>
</html>
"""

def main():
    html = HTML.replace("__CSS__", CSS.strip()).replace("__JS__", JS.strip())
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"已生成 {OUT}")
    print(f"  大小: {len(html):,} 字符")
    print(f"  CSS: {len(CSS):,} 字符")
    print(f"  JS: {len(JS):,} 字符")

if __name__ == "__main__":
    main()
