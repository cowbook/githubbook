# GitHubBook

> 📚 每日追踪 GitHub 热门开源项目，洞察 AI 技术前沿

**[🌐 访问网站](https://cowbook.github.io/githubbook/)** | **[🔥 今日热榜](https://cowbook.github.io/githubbook/trending.html)**

---

## ✨ 功能特色

- 🔥 **每日热榜** - GitHub Actions 每天自动抓取 GitHub Trending 前10项目
- 📝 **深度博文** - 自动生成项目介绍、趋势分析、洞察观点
- 🤖 **AI学堂** - 即将开放，系统学习 AI 开发技术（规划中）
- 📰 **开源周报** - 每周汇总技术热点
- 🛠️ **工具箱** - 精选开发者必备工具
- 🎨 **黑暗主题** - 精美的 GitHub 风格深色设计

## 📁 项目结构

```
githubbook/
├── index.html          # 首页
├── trending.html       # GitHub 热点列表页
├── ai-academy.html     # AI 学堂（规划中）
├── weekly.html         # 周报
├── tools.html          # 工具箱
├── posts/              # 每日热点博文
│   └── YYYY-MM-DD-github-trending.html
├── css/
│   └── style.css       # 全站样式
├── js/
│   └── main.js         # 全站脚本
├── scripts/
│   └── update_trending.py  # 每日自动更新脚本
├── requirements.txt
└── .github/
    └── workflows/
        └── daily-update.yml  # GitHub Actions 配置
```

## 🚀 自动更新机制

每天北京时间 **08:00**，GitHub Actions 自动：

1. 抓取 GitHub Trending 前10个热门项目
2. 生成当日热点博文（`posts/YYYY-MM-DD-github-trending.html`）
3. 更新热点列表页
4. 提交并推送到 `main` 分支
5. GitHub Pages 自动部署

## 🛠️ 本地开发

```bash
# 克隆仓库
git clone https://github.com/cowbook/githubbook.git
cd githubbook

# 安装 Python 依赖（用于运行更新脚本）
pip install -r requirements.txt

# 手动触发更新
python scripts/update_trending.py

# 本地预览（直接打开 HTML 文件即可）
open index.html
```

## 📜 许可证

MIT License - 随便用，欢迎 Star ⭐

---

*由 [GitHubBook Bot](https://github.com/cowbook/githubbook) 每日自动维护*
