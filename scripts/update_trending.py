#!/usr/bin/env python3
"""
GitHubBook 每日自动更新脚本
功能：抓取 GitHub Trending 前10项目，生成博文 HTML，更新首页和热点页面
"""

import requests
import re
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup

# ---- 配置 ----
TIMEZONE = timezone(timedelta(hours=8))
TODAY = datetime.now(TIMEZONE).strftime('%Y-%m-%d')
TODAY_CN = datetime.now(TIMEZONE).strftime('%Y年%m月%d日')
POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')

# 编程语言颜色（和 JS 保持一致）
LANG_COLORS = {
    'TypeScript': '#3178c6',
    'JavaScript': '#f1e05a',
    'Python': '#3572A5',
    'Rust': '#dea584',
    'Go': '#00ADD8',
    'Java': '#b07219',
    'Ruby': '#701516',
    'Shell': '#89e051',
    'C': '#555555',
    'C++': '#f34b7d',
    'HTML': '#e34c26',
    'CSS': '#563d7c',
    'Swift': '#F05138',
    'Kotlin': '#A97BFF',
}

RANK_EMOJIS = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
RANK_CLASSES = ['rank-1', 'rank-2', 'rank-3'] + ['rank-other'] * 7


def fetch_trending(limit=10):
    """抓取 GitHub Trending 页面，解析项目数据"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    try:
        resp = requests.get('https://github.com/trending', headers=headers, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f'[ERROR] 抓取失败: {e}')
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')
    articles = soup.select('article.Box-row')[:limit]

    projects = []
    for art in articles:
        # 仓库名
        h2 = art.select_one('h2 a')
        if not h2:
            continue
        parts = h2.get_text(separator='/', strip=True).split('/')
        if len(parts) < 2:
            continue
        owner = parts[0].strip()
        repo = parts[1].strip()
        url = f'https://github.com/{owner}/{repo}'

        # 描述
        p = art.select_one('p')
        desc = p.get_text(strip=True) if p else ''

        # 语言
        lang_el = art.select_one('[itemprop="programmingLanguage"]')
        lang = lang_el.get_text(strip=True) if lang_el else ''

        # 总 Stars
        stars_el = art.select_one('a[href$="/stargazers"]')
        stars_raw = stars_el.get_text(strip=True) if stars_el else '0'
        stars_raw = stars_raw.replace(',', '').strip()
        try:
            stars = int(stars_raw)
        except:
            stars = 0

        # 今日新增 Stars
        today_el = art.select_one('.float-sm-right')
        today_raw = today_el.get_text(strip=True) if today_el else '0'
        today_num = re.sub(r'[^\d,]', '', today_raw).replace(',', '')
        try:
            today_stars = int(today_num)
        except:
            today_stars = 0

        projects.append({
            'owner': owner,
            'repo': repo,
            'url': url,
            'desc': desc,
            'lang': lang,
            'stars': stars,
            'today_stars': today_stars,
        })

    return projects


def lang_dot_html(lang):
    color = LANG_COLORS.get(lang, '#8b949e')
    return f'<span class="lang-dot" style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{color};"></span>'


def generate_post_html(projects, date_str, date_cn):
    """生成日报博文 HTML"""
    total_stars = sum(p['today_stars'] for p in projects)
    ai_count = sum(1 for p in projects if any(kw in (p['desc'] + p['repo']).lower()
                                               for kw in ['agent', 'llm', 'ai', 'gpt', 'model', 'deep']))

    # 构建项目卡片 HTML
    cards_html = ''
    for i, p in enumerate(projects):
        rank_class = RANK_CLASSES[i]
        rank_num = i + 1
        lang_html = f'{lang_dot_html(p["lang"])} {p["lang"]}' if p['lang'] else ''
        stars_fmt = f'{p["stars"]:,}'
        today_fmt = f'{p["today_stars"]:,}'

        cards_html += f'''
    <div class="project-card">
      <span class="rank-badge {rank_class}">{rank_num}</span>
      <a href="{p['url']}" target="_blank" class="project-name">
        {RANK_EMOJIS[i]} {p['owner']} / {p['repo']}
      </a>
      <p class="project-desc">{p['desc'] or '暂无描述'}</p>
      <div class="project-stats">
        <span class="project-stat">{lang_html}</span>
        <span class="project-stat">⭐ {stars_fmt} 总 Stars</span>
        <span class="stars-today" style="font-size:0.82rem;">↑ +{today_fmt} 今日</span>
      </div>
    </div>'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{date_str} GitHub热点：今日热榜深度解析 - GitHubBook</title>
  <meta name="description" content="{date_cn} GitHub Trending热榜深度解析，今日{len(projects)}大热门开源项目，合计新增{total_stars:,}颗Stars。">
  <meta name="keywords" content="GitHub Trending,{date_str},热点,开源项目,{','.join(p['repo'] for p in projects[:3])}">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📚</text></svg>">
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>

<header class="site-header">
  <div class="header-inner">
    <a href="../index.html" class="logo">
      <div class="logo-icon">📚</div>
      <span class="logo-text">GitHub<span>Book</span></span>
    </a>
    <nav class="main-nav">
      <a href="../index.html" class="nav-link">🏠 首页</a>
      <a href="../trending.html" class="nav-link active">🔥 GitHub热点 <span class="nav-badge">HOT</span></a>
      <a href="../ai-academy.html" class="nav-link">🤖 AI学堂</a>
      <a href="../weekly.html" class="nav-link">📰 周报</a>
      <a href="../tools.html" class="nav-link">🛠️ 工具箱</a>
    </nav>
    <div class="header-cta">
      <a href="https://github.com/cowbook/githubbook" target="_blank" class="btn-github">⭐ Star</a>
    </div>
  </div>
</header>

<div class="post-container">
  <div class="post-hero">
    <div style="margin-bottom:12px;">
      <span class="post-tag tag-hot">🔥 今日热榜</span>
    </div>
    <h1>{date_cn} GitHub 热点：今日热榜深度解析</h1>
    <div class="post-meta-bar">
      <span>📅 {date_str}</span>
      <span>🤖 GitHubBook Bot 自动生成</span>
      <span>⭐ 今日合计 +{total_stars:,} Stars</span>
    </div>
  </div>

  <div class="post-content">

    <p>今天是 <strong>{date_cn}</strong>，GitHub Trending 今日热榜出炉。
    今日共上榜 <strong>{len(projects)}</strong> 个项目，合计新增
    <strong style="color:var(--accent-green);">{total_stars:,} Stars</strong>。
    其中 AI/LLM 相关项目 <strong>{ai_count}</strong> 个。</p>

    <div class="insight-box">
      <h3>📊 今日数据速览</h3>
      <ul>
        <li>上榜项目：{len(projects)} 个</li>
        <li>今日累计新增 Stars：{total_stars:,} ⭐</li>
        <li>AI/LLM 相关项目：{ai_count} 个</li>
        <li>最热项目：{projects[0]['owner']}/{projects[0]['repo']} (+{projects[0]['today_stars']:,})</li>
      </ul>
    </div>

    <h2>🏆 完整榜单</h2>
    {cards_html}

    <div style="margin-top:32px;text-align:center;">
      <a href="../trending.html" class="btn-secondary" style="font-size:0.85rem;padding:8px 16px;">← 返回热点列表</a>
      <a href="https://github.com/trending" target="_blank" class="btn-primary" style="font-size:0.85rem;padding:8px 16px;margin-left:12px;">查看 GitHub Trending →</a>
    </div>

    <div style="margin-top:24px;text-align:center;color:var(--text-muted);font-size:0.8rem;">
      🤖 本文由 GitHubBook GitHub Actions 自动生成 · 数据来源 <a href="https://github.com/trending" target="_blank">GitHub Trending</a>
    </div>

  </div>
</div>

<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-bottom">
      <span>© 2026 GitHubBook · 每日自动更新</span>
      <div class="footer-links">
        <a href="https://github.com/cowbook/githubbook" target="_blank">GitHub</a>
        <a href="../index.html">首页</a>
      </div>
    </div>
  </div>
</footer>

<button class="back-to-top">↑</button>
<script src="../js/main.js"></script>
</body>
</html>'''
    return html


def update_trending_index(projects, date_str, date_cn):
    """更新 trending.html，在顶部插入最新日报链接"""
    trending_path = os.path.join(os.path.dirname(__file__), 'trending.html')
    if not os.path.exists(trending_path):
        return

    with open(trending_path, 'r', encoding='utf-8') as f:
        content = f.read()

    top3 = ', '.join(f'{p["owner"]}/{p["repo"]}' for p in projects[:3])
    total = sum(p['today_stars'] for p in projects)
    new_card = f'''
        <div class="trend-card" style="cursor:default;">
          <div class="card-header">
            <div>
              <div style="font-size:0.78rem;color:var(--text-muted);margin-bottom:6px;">📅 {date_str} · 最新</div>
              <a href="posts/{date_str}-github-trending.html" class="card-title" style="font-size:1.05rem;">
                🔥 {date_cn} GitHub 热榜：{top3} 等上榜
              </a>
            </div>
            <span class="nav-badge" style="flex-shrink:0;">NEW</span>
          </div>
          <p class="card-desc">今日共 {len(projects)} 个项目上榜，合计新增 {total:,} Stars。{top3} 领跑今日热榜。</p>
          <div class="card-meta">
            <a href="posts/{date_str}-github-trending.html" class="section-link" style="margin-left:auto;">阅读全文 →</a>
          </div>
        </div>
'''
    # 插入到热点归档列表第一个位置
    marker = '<!-- AUTO_INSERT_HERE -->'
    if marker in content:
        content = content.replace(marker, marker + new_card)
    else:
        # 找到 trend-list div 后插入
        content = content.replace(
            '<div class="trend-list">',
            f'<div class="trend-list">{new_card}',
            1
        )

    with open(trending_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'[OK] trending.html 已更新')


def main():
    print(f'[INFO] 开始抓取 GitHub Trending，日期：{TODAY}')

    projects = fetch_trending(10)
    if not projects:
        print('[WARN] 未获取到项目数据，退出')
        sys.exit(1)

    print(f'[INFO] 获取到 {len(projects)} 个项目：')
    for i, p in enumerate(projects, 1):
        print(f'  #{i} {p["owner"]}/{p["repo"]} (+{p["today_stars"]:,} 今日)')

    # 生成博文
    post_html = generate_post_html(projects, TODAY, TODAY_CN)
    post_path = os.path.join(POSTS_DIR, f'{TODAY}-github-trending.html')
    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(post_html)
    print(f'[OK] 博文已生成：{post_path}')

    # 更新热点列表页
    update_trending_index(projects, TODAY, TODAY_CN)

    print('[DONE] 更新完成！')


if __name__ == '__main__':
    main()
