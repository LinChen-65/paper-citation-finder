# 论文引用检索系统

一个Web应用程序，用于搜索和整理学术论文的正面引用。

## 功能特性
- 📚 学术论文引用检索（Semantic Scholar API）
- 🎓 国际课件检索（Google Programmable Search）
- 🇨🇳 中文资源检索（百度学术、豆丁网等）
- 😊 正面引用情感分析
- 🌐 响应式Web界面

## 部署指南

### 1. 后端部署 (Render)

**步骤:**
1. 注册 [Render](https://render.com) 账号
2. 创建新的 Web Service
3. 连接你的 GitHub 仓库（包含此代码）
4. 设置环境变量：
   - `GOOGLE_API_KEY` = 你的 Google Cloud API Key
   - `GOOGLE_CSE_ID` = 你的 Custom Search Engine ID
5. 构建命令: `pip install -r requirements.txt`
6. 启动命令: `python app.py`
7. 等待部署完成，记录你的 Render URL

### 2. 前端部署 (Vercel)

**步骤:**
1. 注册 [Vercel](https://vercel.com) 账号
2. 导入你的 GitHub 仓库
3. 在项目根目录创建 `vercel.json` 文件，配置 API 代理：
```json
{
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://your-render-app-url.onrender.com/api/$1"
    }
  ]
}
```
4. 替换 `your-render-app-url` 为你的实际 Render URL
5. 部署完成！

### 3. Google API 配置

**获取 Google API Key:**
1. 访问 [Google Cloud Console](https://console.cloud.google.com)
2. 创建新项目或选择现有项目
3. 启用 "Custom Search API"
4. 创建 API Key

**创建 Custom Search Engine:**
1. 访问 [Google Programmable Search](https://programmablesearchengine.google.com)
2. 创建新的搜索引擎
3. 搜索范围设置为教育相关网站：
   - `*.edu`
   - `slideshare.net`
   - `docer.com`
   - `baidu.com/scholar`
   - `douding.cn`
   - `doc88.com`
4. 获取 CSE ID

### 4. 成本说明
- **Render**: 免费层足够个人使用
- **Vercel**: 免费层足够
- **Google API**: 前100次搜索/天免费，之后 $5/1000次
- **总成本**: $0-5/月

## 使用方法
1. 访问部署后的网站URL
2. 输入论文DOI、标题或相关信息
3. 系统自动搜索并展示正面引用结果
4. 结果按来源分类：学术论文、国际课件、中文资源

## 技术栈
- **前端**: React + Ant Design + Vite
- **后端**: Python Flask + BeautifulSoup
- **API**: Semantic Scholar (免费) + Google Custom Search
- **部署**: Vercel (前端) + Render (后端)

## 注意事项
- 中文网站爬虫可能需要调整反爬策略
- Google API 有调用限制，请合理使用
- 如需更多功能，可扩展后端爬虫模块