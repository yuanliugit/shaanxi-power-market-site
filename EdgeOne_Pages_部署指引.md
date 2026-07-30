# EdgeOne Pages 部署指引（陕电现货观察）

> 目标：把 GitHub 仓库 `yuanliugit/shaanxi-power-market-site` 部署到腾讯云 EdgeOne Pages，获得一个**长期稳定、公网可访问**的网址。

---

## 一、前置确认（已完成 ✅）

| 项目 | 状态 | 说明 |
|---|---|---|
| GitHub 仓库 | ✅ 已存在 | `yuanliugit/shaanxi-power-market-site`（私有仓库） |
| main 分支 | ✅ 已推送 | 最新 commit `a73e6a9 Deploy Shaanxi power market dashboard` |
| index.html | ✅ 在仓库根目录 | 44K，自包含网页（CSS+JS+数据全内联） |
| Excel 下载文件 | ✅ 在仓库根目录 | `陕西现货市场每日出清价格跟踪_2025至今_含风光分项.xlsx`（164K） |
| 构建步骤 | ✅ 无需构建 | index.html 已是最终产物，构建命令留空 |
| 输出目录 | ✅ 仓库根 | 配置填 `.` |

---

## 二、5 步部署流程

### 第 1 步：登录 EdgeOne 控制台

打开 **https://console.cloud.tencent.com/edgeone**

- 首次使用点"立即开通"（免费）
- 已开通直接进入控制台
- 进入后切换到顶部 **Pages** Tab

### 第 2 步：创建项目 → 导入 Git 仓库

在 Pages Tab 下：

1. 鼠标移到"创建项目"，选 **"导入 Git 仓库"**
2. 在 Git 提供商里点 **GitHub**

### 第 3 步：授权 GitHub 访问（关键步骤）

因为是**私有仓库**，需要给 EdgeOne 授权：

1. 跳转到 GitHub 授权页，点 **Authorize EO Pages**
2. 在仓库选择页，选 **Only select repositories**
3. 勾选 `yuanliugit/shaanxi-power-market-site`
4. 点 **Install**

> ⚠️ 如果之前授权过但看不到这个仓库，回到 GitHub → Settings → Applications → EO Pages → Configure → 增加这个仓库的访问权限。

### 第 4 步：填写构建配置

按下表填写（**针对你的仓库已优化**）：

| 配置项 | 填写值 | 说明 |
|---|---|---|
| 仓库 | `yuanliugit/shaanxi-power-market-site` | 第 3 步授权后可选到 |
| 分支 | `main` | 默认主分支 |
| 项目名称 | `shaanxi-power-market` | 自定义，会成为域名一部分 |
| 框架预设 | 无 / Other | 纯静态 HTML，无需预设 |
| 构建命令 | **（留空）** | index.html 已是构建产物 |
| 输出目录 | `.` | 仓库根目录 |
| 根目录 | 留空 | 默认仓库根 |
| 加速区域 | **全球（不含中国境内）** ⭐ | 无需备案，预览域名立即可用 |

> **加速区域选择说明：**
> - **全球（不含中国境内）** ⭐ 推荐：用 EdgeOne 提供的预览域名，**无需备案**，立即可访问，中国境内也能访问（走海外节点，速度可接受）
> - 全球（含中国境内）：用预览域名也可以，但**绑定自定义域名时需备案**
> - 仅中国境外：无需备案，但中国境内访问体验差
>
> 你的场景是数据看板分享，先用"全球（不含中国境内）"+ 预览域名最快上线。后续要境内加速+自定义域名再备案。

### 第 5 步：开始部署 → 拿到域名

1. 检查配置无误，点 **"开始部署"**
2. 等待 30 秒～2 分钟（纯静态，很快）
3. 部署成功后，在"部署详情页"或"项目概览"右上角点 **Preview**，会显示一个形如 `https://xxx.edgeone.app` 或 `https://shaanxi-power-market.edgeone.app` 的预览域名
4. **这个域名就是长期稳定的公网访问地址** —— 复制下来

---

## 三、部署成功后

### 自动部署机制（已自动生效）

EdgeOne Pages 会监听 `main` 分支，**每次 push 自动重新部署**。你本地已有 `publish_verified_update.sh` 脚本，数据更新流程不变：

```
数据更新 → publish_verified_update.sh 跑质量门禁 → 重建 HTML → git push → EdgeOne 自动部署
```

### 拿到域名后告诉我

把 EdgeOne 给你的预览域名发给我，我会：

1. 验证网页可访问（HTTP 200、内容正确）
2. 验证 Excel 下载链接可用
3. 把域名更新到 `README.md` 和 `源码与发布入口说明.md`
4. 提交一次 commit 推到 GitHub（这次 push 也会触发 EdgeOne 自动部署，验证链路闭环）

---

## 四、常见问题

### Q1：授权时看不到 `shaanxi-power-market-site` 仓库？

因为仓库是私有的。在 GitHub 授权页务必选 "Only select repositories" 并勾选该仓库，或选 "All repositories"。

### Q2：部署失败，提示找不到 index.html？

检查"输出目录"是否填了 `.`（仓库根）。不要填 `dist/` 或 `output/`。

### Q3：部署成功但访问 404？

确认仓库根目录确实有 `index.html`（已确认 ✅）。如果用了子目录部署，检查路径配置。

### Q4：中国境内访问慢？

当前选的"全球（不含中国境内）"走海外节点，境内访问稍慢但可用。如需境内加速：
- 升级加速区域到"全球（含中国境内）"
- 绑定自定义域名（需 ICP 备案）

### Q5：要不要改成公开仓库？

不需要。私有仓库 + EdgeOne 授权访问完全支持，且更安全（源码不暴露）。

### Q6：EdgeOne Pages 收费吗？

个人用量范围内免费。具体额度见 https://cloud.tencent.com/document/product/1552 。你这个站点流量很小，免费额度完全够用。

---

## 五、备选方案（如果 EdgeOne 配置遇阻）

| 方案 | 优点 | 缺点 |
|---|---|---|
| **CloudStudio 重新部署** | 立即可用，我可直接操作 | 沙箱预览性质，不保证永久 |
| **GitHub Pages** | 完全免费、永久 | 需把仓库改公开；境内访问不稳定 |
| **Vercel / Netlify** | 免费额度大、自动部署 | 需注册账号；境内访问一般 |

如需切换备选方案，告诉我即可。
