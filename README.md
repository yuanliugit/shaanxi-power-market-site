# 陕电现货观察

公网访问地址：**https://yuanliugit.github.io/shaanxi-power-market-site/**

通过 GitHub Pages 托管，监听 `main` 分支自动部署，长期稳定免费。

## 数据口径

- 陕西电力交易中心结构化数据是市场总体价格和电量的主时间序列。
- 陕西电力交易中心微信公众号日报只补充风电、光伏分项，并用于交叉核验。
- 双源差异只记录，不覆盖交易中心主序列；未披露字段保持为空，不自动填 0。
- 数据表格同时提供交易中心公开页面和公众号日报原文链接，便于逐日追溯。

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

## 自动更新

`publish_verified_update.sh` 会先运行质量门禁和网站测试。只有数据或工作簿确有变化且全部检查通过时，才重新构建静态站、提交并推送 Git；GitHub Pages 监听 `main` 分支后自动重新部署（约 30-60 秒生效）。

更新流程：

```
数据更新 → publish_verified_update.sh 跑质量门禁 → 重建 index.html → git push origin main → GitHub Pages 自动部署
```

## 备选方案

如需中国境内加速或自定义域名，可改用腾讯云 EdgeOne Pages（监听同一仓库 `main` 分支），配置说明见 `EdgeOne_Pages_部署指引.md`。EdgeOne 与 GitHub Pages 可并存。
