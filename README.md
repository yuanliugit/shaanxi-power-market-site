# 陕电现货观察

公网访问地址：**https://yuanliugit.github.io/shaanxi-power-market-site/**

通过 GitHub Pages 托管，监听 `main` 分支自动部署，长期稳定免费。

## 数据口径

- **总体、火电、新能源价格及总体电量**来自陕西电力交易中心公开页面。
- **风电、光伏分项及 OCR 字段**来自陕西电力交易中心微信公众号日报。
- **双源差异只记录，不覆盖交易中心主序列**；未披露字段显示为"—"，不自动填 0。
- 网页不直接访问交易中心接口，不抓取公众号文章；相关链接仅供用户点击追溯。
- 数据表格每一行都提供交易中心公开页面和公众号日报原文链接。

## 运行时数据架构

`index.html` 是单文件静态应用（内联 CSS+JS），**不硬编码历史数据**。

页面初始化时运行时读取以下静态 JSON，并逐文件校验 `data_manifest.json` 中的 SHA-256：

| 文件 | 说明 |
|---|---|
| `data/data_manifest.json` | 数据清单，绑定同一批次所有文件的 SHA-256 |
| `data/snpx_spot_history.json` | 总体日前/实时价格和电量 |
| `data/snpx_spot_types.json` | 火电、新能源日前/实时价格 |
| `data/wechat_wind_solar_prices.json` | 风电、光伏分项、OCR 字段、公众号日报链接 |
| `data/data_snapshot.json` | 最新交易日、质量门禁、行数等摘要 |
| `data/snpx_quality_checks.json` | 质量门禁、重复/缺失/范围错误、OCR 复核 |
| `data/snpx_source_discrepancies.json` | 双源差异明细 |
| `data/snpx_run_changes.json` | 本次更新新增/修订/删除记录 |
| `downloads/陕西现货市场每日出清价格跟踪_2025至今_含风光分项.xlsx` | 完整 Excel 底表 |

加载顺序：优先读取相对路径 `./data/*.json`；失败后回退到 GitHub Pages 绝对地址，再到 GitHub Raw。所有请求使用 `cache: "no-store"`。

## 部署架构

| 项目 | 配置 |
|---|---|
| 托管平台 | GitHub Pages |
| 仓库 | `yuanliugit/shaanxi-power-market-site`（public） |
| 源分支 | `main` |
| 源路径 | `/`（仓库根目录） |
| 构建命令 | 无（index.html 已是最终产物） |
| HTTPS | 强制启用 |
| 域名 | `yuanliugit.github.io/shaanxi-power-market-site/` |

## 本地构建

```bash
cd output

# 1. 确认 data/ 目录已包含同批次的全部 JSON 和 Excel
ls data/

# 2. 生成/更新 data_manifest.json（SHA-256）
python3 build_manifest.py

# 3. 生成 index.html（内联 CSS+JS，不含数据）
python3 build_site.py

# 4. 本地预览
python3 -m http.server 8765
# 打开 http://localhost:8765
```

## 自动更新

`publish_verified_update.sh` 会先运行质量门禁和网站测试。只有数据或工作簿确有变化且全部检查通过时，才重新构建并推送 Git；GitHub Pages 监听 `main` 分支后自动重新部署（约 30-60 秒生效）。

更新流程：

```
Codex 上游生成 JSON + 质量检查 + Excel
→ 同步到 output/data/ 和 output/downloads/
→ python3 build_manifest.py
→ python3 build_site.py
→ publish_verified_update.sh 跑质量门禁与测试
→ git push origin main
→ GitHub Pages 自动部署
```

## 备选方案

如需中国境内加速或自定义域名，可改用腾讯云 EdgeOne Pages（监听同一仓库 `main` 分支），配置说明见 `EdgeOne_Pages_部署指引.md`。EdgeOne 与 GitHub Pages 可并存。
