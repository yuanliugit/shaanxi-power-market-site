# “陕电现货观察”网页配置与数据接入需求

> 文档用途：整份交给 WorkBuddy，作为网站优化、数据接入、测试和发布的实施要求。  
> 项目名称：陕电现货观察  
> 编制日期：2026-07-30  
> 当前参考站点：<https://yuanliugit.github.io/shaanxi-power-market-site/>  
> Git 仓库：<https://github.com/yuanliugit/shaanxi-power-market-site>

> **核心边界：网站只读取 Codex 已完成并持续自动更新的基础数据文件。陕西电力交易中心网站和微信公众号链接只用于用户主动点击追溯，不参与网页取数、补数或更新。**

## 一、给 WorkBuddy 的执行指令

请在现有“陕电现货观察”网站基础上完成改造，不要另做一套数据口径。

本次 WorkBuddy 工作范围是“网页、静态基础数据接入、质量状态展示、测试和现有 Git 发布流程”，不是重新开发交易中心抓取器、微信公众号采集器或 OCR 引擎。历史数据和后续自动更新数据均由既有 Codex 自动化生成；WorkBuddy 只消费质量检查通过的基础数据文件，不得改变上游数据。

现有实施入口：

```text
本地目录：/Users/ly/WorkBuddy/2026-07-27-23-31-38/output/
Git 仓库：https://github.com/yuanliugit/shaanxi-power-market-site
生产分支：main
发布方式：push main 后由现有 GitHub Pages/EdgeOne 配置自动部署
```

不要修改仓库可见性、删除历史部署、创建重复站点或更换生产分支。若要重新开发上游采集，应另列任务和所需接口资料，不得在本次网页改造中猜测源站请求参数。

必须实现：

1. 页面运行时读取独立 JSON，不把历史数据硬编码进 HTML。
2. 网站唯一基础数据源是 Codex 已生成并持续自动更新的 JSON、质量检查文件和 Excel，不得另行访问交易中心接口或公众号采集数据。
3. 基础数据内部已经区分交易中心口径和公众号风光/OCR口径；WorkBuddy 按既有字段展示，不重新抓取、解析、计算或覆盖。
4. 不得用新能源合计反推风电或光伏；未披露、识别失败或来源缺失的值显示为空，不得自动填 0。
5. 每个交易日必须提供来源追溯链接：交易中心公开页面和基础数据中已保存的对应公众号日报原文。链接仅供用户点击核验，不参与网页数据读取。没有对应日报链接时明确显示“未取得原文”，不得伪造链接。
6. 页面必须展示当前实际读取的数据快照日期、质量门禁状态、已知缺失项、双源差异和 OCR 人工复核状态。
7. 质量门禁未通过时不得发布新数据，应保留上一版已通过数据。静态生产页显示“最近成功更新时间”；失败原因写入自动化/部署日志，不要求未发布的失败批次出现在生产页。
8. 保留 Excel 下载和当前筛选范围 CSV 导出。
9. 网站应兼容桌面和手机浏览器，使用中文界面，价格单位统一为“元/MWh”，电量单位必须随字段明确标注。
10. 完成后提供：源码、数据文件、构建命令、测试结果、发布地址和数据更新说明。

## 二、基础数据与来源追溯关系

### 2.1 网站唯一基础数据源

网站只读取第三节列出的已整理基础数据文件，包括历史数据和后续自动更新数据。页面加载、图表计算、表格展示、CSV 导出和 Excel 下载均以这些文件为准。

WorkBuddy 不得：

- 在页面加载时调用陕西电力交易中心网站或接口；
- 访问微信公众号文章抓取数据、图片或 OCR；
- 从外部网页重新生成或修正任何数值；
- 因溯源网站无法访问而删除或清空已经通过质量检查的基础数据。

基础数据中的口径关系已经固化：

- 总体、火电、新能源价格及总体电量字段来自交易中心口径；
- 风电、光伏分项及 OCR 字段来自已整理的公众号日报口径；
- 双源差异已经由上游自动化计算和记录；
- 网站仅展示这些结果，不重新决定来源优先级。

### 2.2 交易中心追溯地址

<https://snpx.com.cn/#/home/marketData/transactionData/spotmarketsection>

该链接只作为“来源追溯地址”展示。网页不得向该网站发起取数请求。基础数据中的 `sourcePage` 已保存此地址，页面直接将其渲染为外链。

### 2.3 公众号追溯地址

公众号名称：陕西电力交易中心。

每条基础数据记录中的 `source_url` 是上游自动化已经保存的对应日报原文链接。网页只把该字段渲染为可点击外链，不主动访问文章、图片，不执行 OCR，也不得自行拼接微信链接。

### 2.4 禁止事项

- 不得用新能源合计减光伏得到风电，或减风电得到光伏。
- 不得把 `null`、空字符串、缺失字段或 OCR 失败改成 `0`。
- 不得把公众号总体值覆盖交易中心总体值。
- 不得因两源数值不一致而选择“看起来更合理”的值。
- 不得通过交易中心网站、接口或公众号补齐基础数据中的空值。
- 不得把追溯链接当成网站运行时数据接口。
- 不得只展示“数据来源：官方”而不提供可点击的原始页面。
- 不得在前端写死“最新日期”或行数。

## 三、基础数据访问方式

### 3.1 当前已公开、可直接访问的数据

以下静态文件是网站的唯一运行时数据入口，已验证可通过 HTTP GET 读取。页面初始化时只能请求这些基础数据文件及同批新增文件，不请求交易中心或公众号：

| 数据 | 网站访问地址 | 用途 |
|---|---|---|
| 总体价格与电量 | <https://yuanliugit.github.io/shaanxi-power-market-site/data/snpx_spot_history.json> | 总体日前/实时价格和电量 |
| 风光/OCR基础数据 | <https://yuanliugit.github.io/shaanxi-power-market-site/data/wechat_wind_solar_prices.json> | 已整理的风电、光伏、OCR字段及追溯链接 |
| 质量快照 | <https://yuanliugit.github.io/shaanxi-power-market-site/data/data_snapshot.json> | 最新日期、行数、质量状态和异常摘要 |
| 完整 Excel | <https://yuanliugit.github.io/shaanxi-power-market-site/downloads/陕西现货市场每日出清价格跟踪_2025至今_含风光分项.xlsx> | 用户下载和人工复核 |

截至 2026-07-30 检查时，公开质量快照显示总体和风光数据最新交易日均为 2026-07-26，质量状态为 `pass_with_recorded_source_gaps`。这只作为验收基线；网页不得把该日期写死。

GitHub Raw 备用读取地址：

```text
https://raw.githubusercontent.com/yuanliugit/shaanxi-power-market-site/main/data/snpx_spot_history.json
https://raw.githubusercontent.com/yuanliugit/shaanxi-power-market-site/main/data/wechat_wind_solar_prices.json
https://raw.githubusercontent.com/yuanliugit/shaanxi-power-market-site/main/data/data_snapshot.json
```

推荐前端读取顺序：

1. 如果 JSON 与网页一起发布，优先读取相对路径 `./data/*.json`；
2. WorkBuddy 独立页面读取上面的 GitHub Pages 绝对地址；
3. GitHub Raw 只作为备用或诊断入口；
4. 生产网页不得混用不同来源或不同批次的多个 JSON；
5. 所有请求使用 `cache: "no-store"`；
6. 页面必须显示本次实际使用的数据地址、数据版本和加载时间；
7. 相对路径失败后才能依次尝试 Pages 和 Raw；若回退后的数据版本不一致，则整批加载失败。

示例：

```js
async function loadJson(url) {
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`数据读取失败：${response.status} ${url}`);
  }
  return response.json();
}

const [official, windSolar, snapshot] = await Promise.all([
  loadJson("./data/snpx_spot_history.json"),
  loadJson("./data/wechat_wind_solar_prices.json"),
  loadJson("./data/data_snapshot.json"),
]);
```

上述代码只是同源读取的最小示例。实际实现须增加超时、逐级回退和版本一致性检查，并区分关键文件失败与可选检查明细失败。

### 3.2 要求新增公开的数据文件

当前公开仓库尚未提供 `snpx_spot_types.json`。WorkBuddy 应将下面的本地主数据文件复制到发布目录 `data/`，并纳入每次更新：

```text
/Users/ly/Documents/Codex/投资策略/snpx_spot_types.json
```

发布后必须可以访问：

```text
./data/snpx_spot_types.json
https://yuanliugit.github.io/shaanxi-power-market-site/data/snpx_spot_types.json
```

禁止只把某一个“日期更晚”的 JSON 单独上线。总体、分类型、风光、质量快照和 Excel 必须来自同一次质量检查批次；若最新完整披露日不同，应在质量快照和页面中分别显示，而不是伪装成相同日期。

该文件用于总体、火电、新能源六类价格：

| JSON 字段 | 含义 |
|---|---|
| `time` | 交易日，格式 `YYYY-MM-DD` |
| `firstPrice` | 总体日前出清加权均价 |
| `secondPrice` | 总体实时出清加权均价 |
| `thirdPrice` | 火电日前出清加权均价 |
| `fourPrice` | 火电实时出清加权均价 |
| `fivePrice` | 新能源日前出清加权均价 |
| `sixPrice` | 新能源实时出清加权均价 |

必须同时公开以下检查文件，供“质量与追溯”页面使用：

```text
./data/snpx_quality_checks.json
./data/snpx_source_discrepancies.json
./data/snpx_run_changes.json
```

对应本地源文件：

```text
/Users/ly/Documents/Codex/投资策略/outputs/019f56ea-7c73-7fa0-98d0-2a7c7bf2a11b/snpx_quality_checks.json
/Users/ly/Documents/Codex/投资策略/outputs/019f56ea-7c73-7fa0-98d0-2a7c7bf2a11b/snpx_source_discrepancies.json
/Users/ly/Documents/Codex/投资策略/outputs/019f56ea-7c73-7fa0-98d0-2a7c7bf2a11b/snpx_run_changes.json
```

同时新增 `./data/data_manifest.json`，将同一批数据绑定为一个版本：

```json
{
  "schemaVersion": "1.0",
  "datasetVersion": "ISO-8601 时间或 Git 提交号",
  "generatedAt": "ISO-8601 时间",
  "files": {
    "history": {"path": "snpx_spot_history.json", "sha256": "64位十六进制"},
    "types": {"path": "snpx_spot_types.json", "sha256": "64位十六进制"},
    "windSolar": {"path": "wechat_wind_solar_prices.json", "sha256": "64位十六进制"},
    "snapshot": {"path": "data_snapshot.json", "sha256": "64位十六进制"},
    "quality": {"path": "snpx_quality_checks.json", "sha256": "64位十六进制"},
    "differences": {"path": "snpx_source_discrepancies.json", "sha256": "64位十六进制"},
    "changes": {"path": "snpx_run_changes.json", "sha256": "64位十六进制"},
    "workbook": {
      "path": "../downloads/陕西现货市场每日出清价格跟踪_2025至今_含风光分项.xlsx",
      "sha256": "64位十六进制"
    }
  },
  "latestTradingDate": "YYYY-MM-DD",
  "latestWindSolarDate": "YYYY-MM-DD",
  "qualityGate": "pass 或 pass_with_recorded_source_gaps"
}
```

发布前须计算并校验清单中的 SHA-256，保证所有 JSON 和 Excel 属于同一次质量检查批次。无需修改既有上游 JSON 增加 `datasetVersion`；一致性以清单哈希为准。

## 四、JSON 字段定义

### 4.1 `snpx_spot_history.json`

顶层字段：

- `extractedAt`：抓取时间；
- `sourcePage`：交易中心公开页面，仅作为来源追溯链接；
- `endpoint`：结构化接口路径；
- `mapping`：字段中文含义；
- `rows`：每日数据；
- `calls`：抓取批次记录，仅用于追溯，不作为图表数据。

`rows` 字段：

| 字段 | 含义 | 单位 |
|---|---|---|
| `time` | 交易日 | `YYYY-MM-DD` |
| `firstPower` | 日前出清电量 | MWh |
| `secondPower` | 实时出清电量 | MWh |
| `firstPrice` | 日前出清加权均价 | 元/MWh |
| `secondPrice` | 实时出清加权均价 | 元/MWh |

这些数值目前可能以字符串保存。前端仅在值不是 `null`、空字符串或非数字时转换为 `Number`。缺失值显示“—”。

### 4.2 `snpx_spot_types.json`

顶层结构与 `snpx_spot_history.json` 相同，必须包含 `extractedAt`、`sourcePage`、`endpoint`、`mapping`、`rows` 和 `calls`。`rows` 是数组，字段映射以第三节表格为准。所有价格单位均为元/MWh。

### 4.3 `wechat_wind_solar_prices.json`

顶层：

- `parsedAt`：OCR/解析生成时间；
- `rows`：按交易日排列的日报数据。

每行主要字段：

- `date`：交易日；
- `source_url`：上游自动化已保存的该日微信公众号原文，仅作为来源追溯链接；
- `image_index`：数据所在原图序号；
- `dayAhead`：日前数据；
- `realTime`：实时数据；
- `status`、`overallStatus`：识别状态；
- `ocr_text_count`：OCR 文本块数量。

`dayAhead` 和 `realTime` 下分别有：

- `overall`：公众号披露的总体数据，只用于交叉核验；
- `wind`：风电；
- `solar`：光伏。

每个对象可能包含：

| 字段 | 含义 |
|---|---|
| `status` | OCR/字段解析状态 |
| `volume` | 公众号披露电量；当前原始单位为亿千瓦时，空值保持空 |
| `max` | 最高价，元/MWh |
| `min` | 最低价，元/MWh |
| `weighted` | 加权均价，元/MWh |
| `minConfidence` | 该组关键字段最低 OCR 置信度 |
| `raw` | OCR 原始字符串，仅供追溯 |

网页重点展示四个风光价格字段：

```text
dayAhead.wind.weighted
realTime.wind.weighted
dayAhead.solar.weighted
realTime.solar.weighted
```

如需把公众号电量转换为 MWh 进行双源比较，必须明确使用 `1 亿千瓦时 = 100,000 MWh`，并在界面标注“公众号披露口径”；不得直接与交易中心总体电量合并为一条序列。

所有 `volume`、`max`、`min`、`weighted` 和 `minConfidence` 都必须经过 `toNullableNumber`，不能只转换交易中心字段。

### 4.4 `data_snapshot.json`

至少展示：

| 字段 | 页面含义 |
|---|---|
| `generatedAt` | 快照生成时间 |
| `latestTradingDate` | 总体主序列最新交易日 |
| `latestWindSolarDate` | 风光分项最新交易日 |
| `qualityGate` | 质量门禁 |
| `rowCounts.official` | 总体行数 |
| `rowCounts.windSolar` | 风光行数 |
| `recordedSourceGapCount` | 已记录源站缺口数量 |
| `overThresholdDifferenceDays` | 双源差异超阈值日期数 |
| `ocrReviewDates` | 需要人工复核的日期 |
| `minOcrConfidence` | 全量最低 OCR 置信度 |
| `noAutoZeroFill` | 是否禁止自动补零，必须为 `true` |

日期术语必须区分：

- `latestTradingDate`：交易中心主序列最新日期；
- `latestWindSolarDate`：公众号风光分项最新日期；
- `latestCompleteDate`：所有网站必需数据都已通过质量检查的共同最新日期，由构建脚本计算；
- 当风光晚于或早于主序列时，分别显示两个日期，不得把 `latestTradingDate` 称为“全部数据最新完整日”。

质量页所需但 `data_snapshot.json` 尚未覆盖的重复日期、缺失日期、字段缺失、范围错误和新增/修订行数，从三个强制检查 JSON 中读取。WorkBuddy 应为这些检查文件补充 JSON Schema 或运行时字段校验，不得凭字段名猜测。

### 4.5 三个质量检查文件的页面映射

`snpx_quality_checks.json`：

| 页面指标 | JSON 路径 |
|---|---|
| 门禁状态 | `qualityGate.status` |
| 阻断问题 | `qualityGate.blockingIssues[]` |
| 已记录源站缺口 | `qualityGate.recordedSourceGaps[]` |
| 总体日期范围 | `website.dateRange` |
| 总体/分类型行数 | `website.historyRows` / `website.typeRows` |
| 重复日期 | `website.duplicateHistoryDates[]` / `website.duplicateTypeDates[]` |
| 缺失日期 | `website.missingDates[]` |
| 缺失字段 | `website.missingHistoryFields[]` / `website.missingTypeFields[]` |
| 价格范围错误 | `website.priceRangeErrors[]` |
| 风光日期范围/行数 | `wechat.windSolarRange` / `wechat.windSolarRows` |
| OCR 缺口和复核 | `wechat.missingOcrDates[]` / `wechat.ocrReviewDates[]` |
| 最低 OCR 置信度 | `wechat.minOcrConfidence` |
| 禁止补零 | `noAutoZeroFill`，必须为 `true` |

`snpx_source_discrepancies.json`：

- 阈值：`thresholds.priceCnyPerMWh`、`thresholds.powerPercent`；
- 重叠日数：`overlapDays`；
- 超阈值日数：`overThresholdDays`；
- 每日明细：`rows[]`，其中使用 `date`、`website`、`wechat`、`difference`、`overThreshold` 和 `action`；
- 页面只展示差异和处理动作，不用该文件覆盖主序列。

`snpx_run_changes.json`：

- 生成时间：`generatedAt`；
- 总体变化：`websiteHistory.added[]`、`revised[]`、`removed[]`；
- 分类型变化：`websiteTypes.added[]`、`revised[]`、`removed[]`；
- 公众号文章变化：`wechatArticles.added[]`、`revised[]`、`removed[]`；
- 风光变化：`windSolar.added[]`、`revised[]`、`removed[]`；
- “新增/修订行数”分别取对应数组长度，不从日期差推算。

## 五、原始数据链接与追溯功能

### 5.1 每日表格

每日表格必须增加“原始来源”列。每一行按交易日显示：

- `交易中心 ↗`：使用 `snpx_spot_history.json.sourcePage`；
- `公众号日报 ↗`：使用同日 `wechat_wind_solar_prices.json.rows[].source_url`；
- 公众号当日不存在时显示“未取得日报”，不生成空链接。

交易中心目前只提供统一市场数据页面链接，不是每个交易日独立的原始响应链接。因此按钮应标为“交易中心公开页面 ↗”，不得宣称它是“该日原始接口响应”。公众号 `source_url` 是基础数据中保存的逐日原文链接。两类链接都只在用户主动点击时打开，不参与页面取数。

链接要求：

```html
target="_blank"
rel="noopener noreferrer"
```

链接旁应有来源说明：

```text
基础数据中的交易中心口径：总体、火电、新能源主序列
基础数据中的公众号口径：风电、光伏分项及交叉核验
交易中心和公众号链接：仅供追溯核验，不用于网页取数
```

### 5.2 数据源与方法页面

页面应设置“数据与方法”或“来源追溯”区块，至少包含：

1. 网站基础数据文件及其更新机制；
2. 交易中心公开页面追溯链接；
3. 最新公众号日报原文追溯链接；
4. 数据清单、全部公开 JSON 和 Excel 访问链接；
5. 字段口径；
6. 双源优先级规则；
7. 不反推风光、不自动补零规则；
8. 当前质量门禁和已知源站缺口；
9. 数据抓取/快照生成时间；
10. “网页不直接访问交易中心或公众号，相关链接仅供追溯”的明确说明。

### 5.3 原始 JSON 访问

增加“查看原始数据”按钮组：

- 查看总体 JSON；
- 查看分类型价格 JSON；
- 查看风光/OCR JSON；
- 查看质量快照；
- 下载完整 Excel。

按钮直接链接到文件，不要把 JSON 内容复制成另一个可能过期的页面。

## 六、页面结构与功能

### 6.1 顶部概览

展示：

- 交易中心主序列最新日；
- 风光分项最新日；
- 全部必需数据共同最新日（若已生成 `latestCompleteDate`）；
- 总体日前加权均价；
- 总体实时加权均价；
- 日前/实时价差；
- 总体日前/实时出清电量；
- 数据质量状态。

所有数字从 JSON 动态计算。三个日期均须校验其确实存在于对应数据中，且不得用一个日期覆盖另一个日期。

### 6.2 价格趋势

至少支持以下曲线开关：

- 总体日前、总体实时；
- 火电日前、火电实时；
- 新能源日前、新能源实时；
- 风电日前、风电实时；
- 光伏日前、光伏实时。

支持：

- 最近 7 天、30 天、90 天、今年、全部；
- 自定义起止日期；
- 图例开关；
- 鼠标/触摸悬浮显示日期和数值；
- 缺失值断线，不连接为 0；
- CSV 导出仅导出当前筛选范围。

### 6.3 电量趋势

总体日前和实时电量只读取基础数据文件 `snpx_spot_history.json`。`wechat_wind_solar_prices.json` 中保存的公众号电量只能作为独立的“公众号披露口径”比较项，不得与交易中心电量混在同一条主序列；网页不得为此访问公众号。

### 6.4 风电与光伏

单独设置风光分项区块，展示：

- 风电日前/实时加权均价；
- 光伏日前/实时加权均价；
- 可选展示电量、最高价、最低价；
- OCR 状态和最低置信度；
- 对应公众号日报链接。

### 6.5 每日数据表

要求：

- 默认按日期倒序；
- 可按日期范围过滤；
- 可搜索日期；
- 可选择显示列；
- 缺失值显示“—”；
- 异常值、源站缺口、待人工复核用标签标记；
- 每行提供交易中心和公众号原文链接；
- 手机端允许横向滚动。

### 6.6 质量与异常

至少显示：

- 质量门禁状态；
- 日期范围和行数；
- 重复日期数量；
- 缺失日期；
- 已知缺失字段；
- 价格范围错误；
- OCR 待复核日期；
- 最低 OCR 置信度；
- 双源差异超阈值日期数；
- 最近一次新增/修订行数；
- “双源差异只记录，不覆盖主序列”的说明。

`pass_with_recorded_source_gaps` 应显示为“通过，但存在已记录的源站缺口”，不能显示成完全无异常。

## 七、数据合并规则

以交易中心总体主序列为左表、日期为主键建立主展示行。分类型或公众号中存在但主序列中不存在的日期，不进入主图表，单独列入“孤立来源记录”质量提示。

合并前必须分别检查每个 `rows` 数组的重复日期；发现重复时阻断该批数据，不允许 `Map` 静默用后值覆盖前值。

```js
const byDate = new Map();

for (const row of officialHistory.rows) {
  if (byDate.has(row.time)) throw new Error(`总体数据重复日期：${row.time}`);
  byDate.set(row.time, {
    date: row.time,
    officialSourceUrl: officialHistory.sourcePage,
    dayAheadPower: toNullableNumber(row.firstPower),
    realTimePower: toNullableNumber(row.secondPower),
    overallDayAheadPrice: toNullableNumber(row.firstPrice),
    overallRealTimePrice: toNullableNumber(row.secondPrice),
  });
}

for (const row of officialTypes.rows) {
  const item = byDate.get(row.time);
  if (!item) continue; // 记录为孤立来源行，不进入主序列
  item.thermalDayAheadPrice = toNullableNumber(row.thirdPrice);
  item.thermalRealTimePrice = toNullableNumber(row.fourPrice);
  item.renewableDayAheadPrice = toNullableNumber(row.fivePrice);
  item.renewableRealTimePrice = toNullableNumber(row.sixPrice);
  byDate.set(row.time, item);
}

for (const row of windSolar.rows) {
  const item = byDate.get(row.date);
  if (!item) continue; // 记录为孤立来源行，不进入主序列
  item.windDayAheadPrice = toNullableNumber(row.dayAhead?.wind?.weighted);
  item.windRealTimePrice = toNullableNumber(row.realTime?.wind?.weighted);
  item.solarDayAheadPrice = toNullableNumber(row.dayAhead?.solar?.weighted);
  item.solarRealTimePrice = toNullableNumber(row.realTime?.solar?.weighted);
  item.wechatSourceUrl = row.source_url ?? null;
  item.ocrStatus = row.overallStatus ?? row.status ?? null;
  byDate.set(row.date, item);
}
```

转换函数必须保留空值：

```js
function toNullableNumber(value) {
  if (value === null || value === undefined || value === "") return null;
  const n = Number(value);
  return Number.isFinite(n) ? n : null;
}
```

## 八、更新、质量门禁与部署

### 8.1 更新频率

每周一北京时间 10:30 更新，覆盖上次成功更新日至最新完整披露日。

### 8.2 发布顺序

```text
Codex 上游自动化完成历史数据延续、源站更新和 OCR
→ Codex 生成并验证 JSON、质量检查和 Excel
→ Codex 完成日期连续性/重复/缺失/范围/OCR/双源差异检查
→ 质量门禁通过
→ WorkBuddy/发布脚本接收同批基础数据并同步到网站 data 和 downloads
→ 构建与测试
→ Git 提交并 push main
→ 自动部署
```

WorkBuddy 从“接收同批基础数据”开始执行，不负责前面三步，也不得自行访问交易中心或公众号补做数据。

只有以下状态允许发布：

```text
pass
pass_with_recorded_source_gaps
```

出现阻断问题时：

- 不覆盖上一版已发布数据；
- 不创建空数据版本；
- 页面继续显示上一版快照及最近成功更新时间；
- 在自动化/部署日志中记录失败原因；
- 不把缺失值写成 0。

生产发布必须采用整包方式：先在临时构建目录生成全部 JSON、清单、Excel 和页面，完成 Schema、质量门禁、构建和测试后，再一次性提交同一个 Git 版本。禁止先覆盖生产 JSON 再检查。每次成功发布保留上一个通过门禁的 Git 提交号作为回滚点，并避免两个更新任务并发 push。

### 8.3 Git 与发布

当前仓库：

```text
https://github.com/yuanliugit/shaanxi-power-market-site
生产分支：main
```

要求：

- 数据和代码变更才提交；无变化不生成空提交；
- 每次提交信息包含最新交易日；
- GitHub Pages 或 EdgeOne 使用 `main` 自动部署；
- 不创建新的重复网站项目；
- 自定义域名备案完成前，不把临时预览链接称为长期生产地址。

## 九、加载失败与安全要求

### 9.1 加载失败

任一关键 JSON 加载失败时：

- 页面显示明确错误和失败的数据 URL；
- 不展示全 0 图表；
- 不用另一个来源补齐主序列；
- 提供“重新加载”按钮；
- 保留页头、数据说明和下载入口；
- 在控制台记录可诊断错误，不显示用户隐私或凭证。

### 9.2 安全

- 不在前端放置 Cookie、Token、账号密码或私有接口密钥；
- 公开页面仅读取已经公开的静态 JSON；
- 页面自动加载产生的网络请求中不得出现 `snpx.com.cn` 或 `mp.weixin.qq.com`；只有用户主动点击追溯链接时才能跳转；
- 所有外链使用 `noopener noreferrer`；
- 不执行 JSON 中的 HTML；
- 文本插入使用 `textContent` 或框架默认转义；
- Excel 与 JSON 文件名保持稳定，方便自动更新。

## 十、验收测试

WorkBuddy 必须逐项测试并报告结果：

1. 首页、`data_manifest.json` 中列出的全部 JSON 和 Excel 均返回 HTTP 200。
2. 最新交易日来自 JSON，不是写死文本。
3. 总体、火电、新能源、风电、光伏价格映射正确。
4. 任取 3 个日期，页面值与 JSON 原值一致。
5. 任取 3 个日期，公众号链接与对应 `source_url` 一致。
6. 交易中心链接指向 `sourcePage`。
7. `null` 在图表中断线、表格显示“—”，不显示 0。
8. 删除或改名一个测试 JSON 后，页面出现明确加载错误。
9. `qualityGate` 非允许状态时，发布脚本停止。
10. CSV 只包含当前筛选日期范围，Excel 可正常下载打开。
11. 手机宽度 375px 和桌面宽度 1440px 均无内容遮挡。
12. 构建和现有自动化测试全部通过。
13. 人为制造重复日期时质量门禁阻断，不能静默覆盖。
14. 人为修改任一数据文件使其 SHA-256 与 `data_manifest.json` 不一致时，整批加载失败，不能跨版本混合展示。
15. 打开页面并不点击任何追溯链接时，网络请求中没有交易中心或微信公众号域名；图表和表格仍可完全加载。

## 十一、最终交付清单

WorkBuddy 完成后需交付：

- 网站源码；
- `data/` 下的全部 JSON；
- `downloads/` 下的 Excel；
- 数据字段说明；
- 本地预览命令；
- 构建和测试命令；
- Git 仓库和生产分支；
- 自动部署配置；
- 生产访问地址；
- 本次最新交易日；
- 测试结果；
- 已知缺失字段、双源差异和 OCR 人工复核清单。

不得只回复“已完成”。必须提供可访问链接、文件路径和测试证据。
