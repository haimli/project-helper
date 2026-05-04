# Project Helper - 项目学习助手

> 输入一个 GitHub 仓库地址，自动生成通俗易懂的源码分析报告，还可以针对代码进行交互式问答。

## 功能特性

- **一键分析** — 输入 GitHub 仓库 URL，自动克隆并分析源码
- **完整报告** — 生成项目概述、技术栈、目录结构、核心模块、数据流、设计模式、阅读建议等 7 大模块的分析报告
- **实时进度** — 分析过程通过 SSE 实时推送进度，每个阶段清晰可见
- **智能缓存** — 已分析过的项目自动缓存，无需重复分析
- **交互问答** — AI Agent 拥有读取文件、搜索代码、列出目录等工具，自主查找代码来回答问题
- **流式输出** — 聊天回复逐字流式输出，工具调用过程实时可见
- **科技感 UI** — 暗色主题 + 发光特效 + 代码语法高亮

---

## 环境要求

| 依赖 | 最低版本 |
|------|---------|
| Python | 3.10+ |
| Node.js | 18+ |
| Git | 2.x (需在 PATH 中) |
| DeepSeek API Key | 需提前申请 |

> **注意**: Python 3.14 目前与 `langchain.agents` 存在兼容性问题，建议使用 Python 3.10 ~ 3.13。

---

## 快速开始

### 1. 获取代码

```bash
cd project-helper
```

### 2. 配置后端

```bash
cd backend

# 安装 Python 依赖
pip install -r requirements.txt

# 复制环境变量模板并填写 API Key
cp .env.example .env
```

编辑 `.env` 文件，填入你的 DeepSeek API Key：

```ini
DEEPSEEK_API_KEY=sk-your-actual-key-here
DEEPSEEK_API_BASE=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
DATABASE_URL=sqlite+aiosqlite:///data/projects.db
REPOS_DIR=data/repos
```

**必须配置的变量：**

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 (必填) | 空 |
| `DEEPSEEK_API_BASE` | DeepSeek API 地址 | `https://api.deepseek.com` |
| `DEEPSEEK_MODEL` | 使用的模型名称 | `deepseek-chat` |
| `DATABASE_URL` | SQLite 数据库路径 | `sqlite+aiosqlite:///data/projects.db` |
| `REPOS_DIR` | 克隆仓库的存储目录 | `data/repos` |
| `MAX_CLONE_SIZE_MB` | 仓库最大体积限制 (MB) | `500` |
| `CORS_ORIGINS` | 允许的前端跨域地址 | `["http://localhost:5173"]` |

### 3. 启动后端

```bash
cd backend

# 方式一：直接运行
python run.py

# 方式二：用 uvicorn 启动 (可自定义参数)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

后端启动后：
- API 地址: `http://localhost:8000`
- API 文档 (Swagger): `http://localhost:8000/docs`
- API 文档 (ReDoc): `http://localhost:8000/redoc`

### 4. 安装前端依赖

```bash
cd frontend
npm install
```

### 5. 启动前端

```bash
cd frontend
npm run dev
```

前端启动后访问: `http://localhost:5173`

> 前端开发服务器已配置代理，`/api` 路径的请求会自动转发到后端 `http://localhost:8000`，无需额外配置跨域。

---

## 使用指南

### 分析一个项目

1. 打开 `http://localhost:5173`，在首页输入框中输入 GitHub 仓库地址
   - 支持格式: `https://github.com/用户名/仓库名`
   - 例如: `https://github.com/fastapi/fastapi`

2. 点击 **Analyze** 按钮，页面自动跳转到分析进度页

3. 分析过程包含 8 个阶段，实时显示进度条：
   | 阶段 | 说明 | 进度 |
   |------|------|------|
   | Cloning | 克隆仓库到本地 | 5% |
   | Scanning | 扫描目录结构 | 15% |
   | Tech Stack | 分析技术栈 | 30% |
   | Core Modules | 识别核心模块 | 50% |
   | Data Flow | 分析数据流 | 65% |
   | Design Patterns | 检测设计模式 | 80% |
   | Reading Guide | 生成阅读建议 | 90% |
   | Saving | 保存报告 | 100% |

4. 分析完成后自动展示完整报告，包含以下板块：
   - **Project Overview** — 项目概述与用途
   - **Tech Stack** — 编程语言、框架、构建工具
   - **Directory Structure** — 目录树结构
   - **Core Modules** — 核心模块及其职责与依赖关系
   - **Data Flow** — 主要数据流路径
   - **Design Patterns** — 使用的设计模式
   - **Reading Guide** — 推荐的阅读顺序

5. 已分析过的项目会被缓存，再次输入相同地址会直接返回报告

### 交互式问答

1. 在项目分析报告页，点击右上角 **Chat with Code** 按钮进入聊天页

2. 输入问题，AI Agent 会自动调用工具查看代码后回答，例如：
   - "这个项目的入口文件在哪？"
   - "解释一下 `src/main.py` 的逻辑"
   - "这个项目用到了哪些设计模式？"
   - "数据库连接是如何建立的？"

3. Agent 拥有 3 个工具：
   | 工具 | 说明 |
   |------|------|
   | `read_file` | 读取项目中的源代码文件 |
   | `search_code` | 按关键词/正则搜索代码 |
   | `list_files` | 列出目录下的文件和子目录 |

4. 工具调用过程会实时显示在聊天界面中（可折叠查看详情），回复内容逐字流式输出

5. 点击 **+ New Chat** 可以开始新的对话会话

### 管理项目

- 首页底部展示所有已分析过的项目列表
- 点击项目卡片可重新查看分析报告或进入聊天
- 项目状态分为 4 种：`pending`（等待中）、`analyzing`（分析中）、`completed`（已完成）、`failed`（失败）

---

## API 文档

后端启动后可访问 Swagger UI (`/docs`) 查看交互式 API 文档，以下是接口概览：

### 项目管理

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| `POST` | `/api/projects/analyze` | 提交分析 | `{"repo_url": "https://github.com/..."}` | `{"id": 1, "status": "pending", ...}` |
| `GET` | `/api/projects` | 项目列表 | Query: `?skip=0&limit=20` | `{"items": [...], "total": 42}` |
| `GET` | `/api/projects/{id}` | 项目详情 | — | `{"id": 1, "repo_url": "...", "status": "completed", ...}` |
| `GET` | `/api/projects/{id}/report` | 分析报告 | — | 完整报告 JSON |
| `GET` | `/api/projects/{id}/progress` | SSE 进度流 | — | SSE 事件流 |
| `DELETE` | `/api/projects/{id}` | 删除项目 | — | `{"ok": true}` |

**SSE 进度事件格式：**

```
event: progress
data: {"stage": "analyzing_tech_stack", "progress": 30, "detail": "Analyzing tech stack..."}
```

### 聊天问答

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| `POST` | `/api/chat/sessions` | 创建会话 | `{"project_id": 1}` | `{"id": 1, "project_id": 1, ...}` |
| `GET` | `/api/chat/sessions` | 会话列表 | Query: `?project_id=1` | `{"items": [...]}` |
| `GET` | `/api/chat/{sid}/messages` | 消息历史 | — | `{"items": [...]}` |
| `POST` | `/api/chat/{sid}/messages` | 发送消息 (SSE) | `{"content": "问题"}` | SSE 事件流 |

**SSE 聊天事件格式：**

```
event: token
data: {"content": "这个项目的"}

event: tool_call
data: {"tool": "read_file", "input": {"file_path": "src/main.py"}}

event: tool_result
data: {"tool": "read_file", "output": "import sys\n..."}

event: done
data: {}
```

---

## 项目结构

```
project-helper/
├── PRD.md
├── README.md
│
├── backend/                         # 后端 (Python FastAPI)
│   ├── requirements.txt             # Python 依赖
│   ├── .env.example                 # 环境变量模板
│   ├── run.py                       # 启动入口
│   └── app/
│       ├── main.py                  # FastAPI 应用 + CORS + 生命周期
│       ├── config.py                # Pydantic Settings 配置
│       ├── database.py              # SQLAlchemy 异步引擎 + 数据库初始化
│       ├── models/                  # ORM 模型
│       │   ├── project.py           #   项目表
│       │   ├── analysis_report.py   #   分析报告表 (与项目 1:1)
│       │   ├── chat_session.py      #   聊天会话表
│       │   └── chat_message.py      #   聊天消息表
│       ├── schemas/                 # Pydantic 请求/响应模型
│       ├── api/                     # API 路由层
│       │   ├── router.py            #   路由聚合
│       │   ├── projects.py          #   项目管理接口
│       │   └── chat.py              #   聊天问答接口
│       ├── services/                # 业务逻辑层
│       │   ├── git_service.py       #   Git 克隆与仓库管理
│       │   ├── analyzer.py          #   分析流水线编排 (8 阶段)
│       │   ├── llm_service.py       #   LLM 调用封装 (DeepSeek)
│       │   ├── chat_service.py      #   聊天会话与消息管理
│       │   └── cache_service.py     #   项目缓存查询
│       ├── agent/                   # LangChain Agent
│       │   ├── tools.py             #   3 个工具: read_file, search_code, list_files
│       │   ├── agent.py             #   Agent 工厂 (bind_tools + Runnable)
│       │   └── prompts.py           #   系统 Prompt + 6 个分析阶段 Prompt
│       ├── core/                    # 横切关注点
│       │   ├── progress.py          #   SSE 进度管理器 (asyncio pub/sub)
│       │   ├── exceptions.py        #   自定义异常
│       │   └── security.py          #   路径遍历防护
│       └── analysis/                # 6 个分析阶段实现
│           ├── scanner.py           #   目录扫描 + 文件统计
│           ├── tech_stack.py        #   技术栈检测
│           ├── core_modules.py      #   核心模块识别
│           ├── data_flow.py         #   数据流分析
│           ├── design_patterns.py   #   设计模式检测
│           └── reading_guide.py     #   阅读建议生成
│
├── frontend/                        # 前端 (Vue 3 + TypeScript)
│   ├── package.json
│   ├── vite.config.ts               # Vite 配置 (含 /api 代理)
│   ├── tsconfig.json
│   ├── index.html
│   └── src/
│       ├── main.ts                  # 应用入口
│       ├── App.vue                  # 根组件 (Header + RouterView)
│       ├── api/                     # HTTP 客户端层
│       │   ├── index.ts             #   Axios 实例
│       │   ├── projects.ts          #   项目 API
│       │   └── chat.ts              #   聊天 API
│       ├── views/                   # 页面组件
│       │   ├── HomeView.vue         #   首页: 输入仓库 + 历史项目
│       │   ├── ProjectView.vue      #   项目页: 进度条 + 分析报告
│       │   └── ChatView.vue         #   聊天页: 交互式问答
│       ├── components/              # 可复用组件
│       │   ├── RepoInput.vue        #   GitHub URL 输入框
│       │   ├── AnalysisProgress.vue #   分析进度展示
│       │   ├── ReportView.vue       #   完整报告渲染 (7 板块)
│       │   ├── DirectoryTree.vue    #   目录树展示
│       │   ├── ChatMessage.vue      #   聊天消息气泡
│       │   ├── ChatInput.vue        #   消息输入框
│       │   ├── ToolCallBlock.vue    #   工具调用折叠展示
│       │   └── CodeBlock.vue        #   代码语法高亮
│       ├── stores/                  # Pinia 状态管理
│       │   ├── project.ts           #   项目状态
│       │   └── chat.ts              #   聊天状态
│       ├── router/index.ts          # Vue Router 路由配置
│       ├── styles/                  # 样式
│       │   ├── variables.scss       #   CSS 变量 (科技感暗色主题)
│       │   ├── global.scss          #   全局样式重置
│       │   ├── markdown.scss        #   Markdown 渲染样式
│       │   └── animations.scss      #   发光/脉冲/扫描线动效
│       └── utils/
│           ├── sse.ts               # POST SSE 客户端 + 进度 SSE
│           └── markdown.ts          # Marked + highlight.js 配置
│
└── data/                            # 运行时数据 (自动生成, git-ignored)
    ├── projects.db                  # SQLite 数据库
    └── repos/                       # 克隆的仓库文件
```

---

## 数据库设计

应用使用 SQLite 存储，启动时自动创建表，无需手动建库。

```sql
-- 项目表
projects (
    id            INTEGER PRIMARY KEY,
    repo_url      TEXT UNIQUE NOT NULL,       -- GitHub 仓库地址
    repo_name     TEXT NOT NULL,              -- user/repo 格式
    status        TEXT DEFAULT 'pending',     -- pending | analyzing | completed | failed
    error_message TEXT,                       -- 失败时的错误信息
    created_at    DATETIME,
    updated_at    DATETIME
)

-- 分析报告表 (与项目 1:1)
analysis_reports (
    id                  INTEGER PRIMARY KEY,
    project_id          INTEGER UNIQUE REFERENCES projects(id) ON DELETE CASCADE,
    overview            TEXT,                 -- 项目概述 (Markdown)
    tech_stack          TEXT,                 -- 技术栈 (JSON)
    directory_structure TEXT,                 -- 目录结构 (文本树)
    core_modules        TEXT,                 -- 核心模块 (JSON 数组)
    data_flow           TEXT,                 -- 数据流 (Markdown)
    design_patterns     TEXT,                 -- 设计模式 (JSON 数组)
    reading_suggestions TEXT,                 -- 阅读建议 (JSON 数组)
    created_at          DATETIME
)

-- 聊天会话表
chat_sessions (
    id          INTEGER PRIMARY KEY,
    project_id  INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    title       TEXT DEFAULT 'New Chat',
    created_at  DATETIME
)

-- 聊天消息表
chat_messages (
    id          INTEGER PRIMARY KEY,
    session_id  INTEGER REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role        TEXT,                          -- user | assistant | tool
    content     TEXT,
    tool_name   TEXT,                          -- 工具消息: 工具名称
    tool_input  TEXT,                          -- 工具消息: 调用参数 (JSON)
    created_at  DATETIME
)
```

---

## 前端路由

| 路径 | 页面 | 说明 |
|------|------|------|
| `/` | HomeView | 首页，输入仓库地址，查看历史项目 |
| `/project/:id` | ProjectView | 项目详情页，展示分析进度或报告 |
| `/chat/:projectId` | ChatView | 聊天页，交互式源码问答 |

---

## 常用命令

### 后端

```bash
# 启动开发服务器 (带热重载)
cd backend && python run.py

# 手动启动 uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 安装依赖
pip install -r requirements.txt
```

### 前端

```bash
# 安装依赖
cd frontend && npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

---

## 生产部署

### 后端

```bash
# 不带热重载，使用多 worker
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

需修改 `.env` 中的 `CORS_ORIGINS` 为实际前端域名。

### 前端

```bash
# 构建
npm run build

# 产物在 dist/ 目录，用 Nginx 等 Web 服务器托管
```

Nginx 配置参考：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/project-helper/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API 反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # SSE 需要关闭缓冲
    location /api/projects/*/progress {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Connection '';
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_cache off;
    }

    # Chat SSE 同样需要关闭缓冲
    location /api/chat/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Connection '';
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_cache off;
    }
}
```

---

## 技术栈

### 后端

- **FastAPI** — 高性能异步 Web 框架
- **SQLAlchemy 2.0** — 异步 ORM (aiosqlite 驱动)
- **LangChain** — LLM 应用开发框架
- **langchain-openai** — DeepSeek 兼容 OpenAI 协议，直接使用 ChatOpenAI
- **sse-starlette** — FastAPI SSE 支持
- **Pydantic** — 数据校验与 Settings 管理

### 前端

- **Vue 3** — 渐进式前端框架 (Composition API + `<script setup>`)
- **TypeScript** — 类型安全
- **Vite** — 极速构建工具
- **Pinia** — 状态管理
- **Vue Router** — 路由管理
- **Axios** — HTTP 客户端
- **Marked** — Markdown 渲染
- **highlight.js** — 代码语法高亮
- **Sass** — CSS 预处理器

---

## 常见问题

### Q: 启动后端报 `unable to open database file`

确保 `data/` 目录有写入权限。应用启动时会自动创建 `data/` 目录和 SQLite 数据库文件。如果使用相对路径，确保工作目录正确：

```bash
cd backend && python run.py   # 正确，在 backend 目录下启动
```

### Q: 分析时报 `git is not installed`

系统依赖 Git 命令行工具来克隆仓库。请安装 Git 并确保在 PATH 中：

```bash
git --version   # 确认可用
```

### Q: 聊天问答没有响应

1. 检查 `.env` 中的 `DEEPSEEK_API_KEY` 是否正确
2. 确认 DeepSeek API 可正常访问
3. 查看后端终端的错误日志

### Q: Python 3.14 启动报 TypeError

Python 3.14 与 `langchain.agents` (AgentExecutor) 存在兼容性问题。本项目已改用 `langchain_core` 的低级 API (bind_tools + Runnable) 来规避此问题。如果仍有报错，建议降级到 Python 3.10 ~ 3.13。

### Q: 前端页面空白或 API 请求 404

确保后端已启动在 `localhost:8000`。前端 Vite 开发服务器已配置代理将 `/api` 请求转发到后端。如果修改了后端端口，需同步修改 `frontend/vite.config.ts` 中的 `proxy.target`。

### Q: 如何更换 LLM 模型

修改 `.env` 中的配置即可，DeepSeek 的 API 兼容 OpenAI 协议：

```ini
# 使用其他兼容 OpenAI 协议的模型
DEEPSEEK_API_BASE=https://api.openai.com/v1
DEEPSEEK_API_KEY=sk-your-openai-key
DEEPSEEK_MODEL=gpt-4o
```
