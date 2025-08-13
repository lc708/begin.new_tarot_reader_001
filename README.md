# 🔮 神秘塔罗牌占卜师

一个基于[begin.new，5分钟，把想法变成可收钱的AI应用](https://www.begin.new)开发的全栈塔罗牌占卜应用，结合传统塔罗智慧与现代AI技术，为用户提供个性化的占卜体验。

## ✨ 特性

### 🎴 完整塔罗体验
- **78张完整塔罗牌**：包含22张大阿卡纳和56张小阿卡纳
- **6种牌阵选择**：从简单的单张牌到复杂的凯尔特十字
- **智能牌阵推荐**：AI根据问题类型自动推荐最适合的牌阵

### 🤖 AI智能解读
- **问题分析**：AI自动分析问题类型和复杂度
- **个性化解读**：结合牌意、位置和用户问题生成定制解读
- **综合指导**：整合多张牌的信息提供全面建议

### 💫 神秘用户界面
- **暗黑神秘主题**：深紫色调配合金色点缀
- **流畅动画效果**：卡牌翻转、洗牌、发光等视觉效果
- **响应式设计**：完美适配桌面和移动设备

### 📚 学习与历史
- **占卜历史记录**：保存所有占卜结果，支持回顾
- **塔罗牌学习**：完整的牌意解释和牌阵教学
- **统计分析**：问题类型分布和使用习惯统计

## 🏗️ 技术架构

### 后端 (MACore + Python)
- **MACore框架**：流程化处理占卜逻辑
- **节点化设计**：7个核心节点处理不同步骤
- **工具函数库**：塔罗牌数据库、抽牌逻辑、存储系统

### 前端 (Next.js + React)
- **Next.js 14**：现代化React框架
- **Tailwind CSS**：实用优先的CSS框架
- **Framer Motion**：流畅的动画效果
- **TypeScript**：类型安全的开发体验

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 18+
- OpenAI API Key（用于AI解读功能，可选）

## ☁️ 部署到Vercel

### 一键部署
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyour-username%2Fbgapp_001_tarot)

### 手动部署步骤
1. **Fork或克隆项目到你的GitHub**
2. **在Vercel中导入项目**
   - 登录 [Vercel](https://vercel.com)
   - 点击 "New Project"
   - 导入你的GitHub仓库
3. **配置环境变量**
   - 在Vercel项目设置中添加环境变量：
   ```
   OPENAI_API_KEY=your-openai-api-key-here
   LLM_PROVIDER=openai
   OPENAI_MODEL=gpt-5-mini
   ```
4. **部署**
   - Vercel会自动检测Next.js项目并部署
   - 后端API会作为Serverless Functions运行

### 环境变量说明
- `OPENAI_API_KEY`: OpenAI API密钥（必需）
- `LLM_PROVIDER`: LLM提供商，支持 `openai`、`gemini`、`deepseek`
- `OPENAI_MODEL`: OpenAI模型名称（默认：`gpt-5-mini`）

### 全栈模式运行（推荐）

#### 1. 启动后端API服务器
```bash
cd bgapp_001_tarot
pip install -r requirements.txt

# 可选：设置LLM API密钥以获得更好的占卜效果
cp .env.template  .env.local
修改 OPENAI_API_KEY=your-openai-api-key-here
如需使用其他模型，请阅读.env文件中的注释

# 启动API服务器
python3 api_server.py
```
API服务器将在 `http://localhost:8011` 启动

#### 2. 启动前端界面
```bash
cd frontend
npm install
npm run dev
```
前端界面将在 `http://localhost:3000` 启动

#### 3. 享受完整体验
- 🎨 **精美的用户界面**：神秘主题设计配合流畅动画
- 🔗 **前后端联动**：真正的API调用获得准确占卜
- 🤖 **AI智能解读**：个性化的塔罗牌解释
- 💾 **历史记录**：自动保存占卜结果

### 单独使用模式

#### 仅使用后端（命令行）
```bash
# 交互式模式
python3 main.py

# 演示模式
python3 main.py --demo

# 单次占卜
python3 main.py -q "我今天的运势如何？" -s single
```

#### 仅使用前端（本地模式）
```bash
cd frontend
npm run dev
```
前端会在无法连接后端时自动切换到本地模式

## 📱 使用指南

### 命令行模式

#### 交互式占卜
```bash
python3 main.py
```
选择"1. 进行塔罗牌占卜"，然后按提示操作：
1. 输入您的问题
2. 选择牌阵类型
3. 查看占卜结果

#### 快速占卜
```bash
python3 main.py -q "我的感情状况如何？" -s love_spread
```

#### 查看统计
```bash
python3 main.py --stats
```

### Web界面

1. **访问首页**：浏览应用介绍和特性
2. **开始占卜**：点击"开始占卜"进入占卜流程
3. **输入问题**：详细描述您想了解的问题
4. **选择牌阵**：根据问题类型选择合适的牌阵
5. **抽牌解读**：观看抽牌动画，获得AI解读

## 🎯 支持的牌阵

| 牌阵名称 | 牌数 | 适用场景 | 难度 |
|---------|------|----------|------|
| 单张牌占卜 | 1张 | 日常指导、简单问题 | 初级 |
| 三张牌占卜 | 3张 | 过去-现在-未来分析 | 初级 |
| 恋爱牌阵 | 5张 | 感情问题专用 | 中级 |
| 事业牌阵 | 6张 | 工作事业指导 | 中级 |
| 决策牌阵 | 7张 | 两难选择分析 | 中级 |
| 凯尔特十字 | 10张 | 复杂问题全面分析 | 高级 |

## 📂 项目结构

```
bgapp_001_tarot/
├── docs/                    # 设计文档
│   ├── design.md           # 完整设计文档
│   └── detail_note.md      # 开发详细记录
├── utils/                   # 工具函数库
│   ├── tarot_database.py   # 塔罗牌数据库
│   ├── card_drawer.py      # 随机抽牌逻辑
│   ├── spread_config.py    # 牌阵配置
│   ├── reading_storage.py  # 占卜记录存储
│   └── call_llm.py         # LLM调用封装
├── nodes.py                 # MACore节点定义
├── flow.py                  # 流程管理
├── main.py                  # 主程序入口
├── macore.py               # MACore框架
├── requirements.txt        # Python依赖
└── frontend/               # 前端应用
    ├── src/
    │   ├── pages/          # 页面组件
    │   ├── components/     # 通用组件
    │   ├── styles/         # 样式文件
    │   └── lib/           # 工具库
    ├── package.json        # Node.js依赖
    └── next.config.js      # Next.js配置
```

## 🎨 设计理念

### 视觉设计
- **神秘主题**：深色背景配合紫金色调
- **星空元素**：动态星空背景增加神秘感
- **发光效果**：关键元素的微妙发光效果
- **流畅动画**：卡牌翻转、洗牌等自然动画

### 用户体验
- **引导式流程**：清晰的步骤指示和引导
- **即时反馈**：每个操作都有相应的视觉反馈
- **渐进式复杂度**：从简单到复杂的牌阵选择
- **历史追踪**：完整的占卜历史和统计

## 🔧 自定义配置

### 添加新牌阵
在 `utils/spread_config.py` 中添加新的牌阵配置：

```python
"new_spread": {
    "name": "新牌阵",
    "description": "牌阵描述",
    "card_count": 5,
    "positions": {
        1: {"name": "位置1", "description": "位置含义"},
        # ...
    }
}
```

### 自定义塔罗牌
在 `utils/tarot_database.py` 中修改或添加塔罗牌信息。

### LLM提供商配置
在 `utils/call_llm.py` 中配置不同的LLM提供商。

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- **MACore框架**：提供强大的流程化处理能力
- **塔罗牌智慧**：传承千年的占卜艺术
- **开源社区**：各种优秀的开源工具和库

---

🔮 *愿塔罗牌的智慧为您的人生之路带来光明与指引* ✨