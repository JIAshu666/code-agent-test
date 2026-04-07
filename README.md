# 最简编程 Agent

一个基于大模型的智能编程助手，能够帮助您创建Python项目、生成代码、搭建环境并安装依赖。

## 🚀 功能特点

- **智能代码生成**：根据用户需求生成Python代码
- **环境管理**：自动创建虚拟环境并安装依赖
- **文件操作**：支持读取和写入文件
- **错误处理**：分析错误信息并修复代码问题
- **多轮交互**：支持与大模型进行持续对话

## 🛠️ 技术栈

- **Python 3.10+**：主要开发语言
- **OpenAI SDK**：与大模型API通信
- **uv**：Python包管理工具
- **python-dotenv**：环境变量管理

## 📦 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/JIAshu666/code-agent-test.git
cd code-agent-test
```

### 2. 创建虚拟环境

```bash
# 使用uv创建虚拟环境
uv venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建 `.env` 文件并添加以下内容：

```env
# 大模型API配置
API_KEY=your_api_key
BASE_URL=your_api_base_url
MODEL_NAME=your_model_name
```

## 🚀 使用方法

### 启动Agent

```bash
python main.py
```

### 示例交互

```
====== 最简编程 Agent 已启动 ======
提示：你可以让它写代码，然后你自己去运行，把报错信息直接复制粘贴发给它。

你: 帮我写一个Python脚本，爬取网页内容并保存到文件
Agent: 好的，我来帮你实现这个功能。首先让我创建一个虚拟环境，然后编写爬虫脚本。

[Agent 行动] 正在调用: create_venv, 参数: E:\code\python\spider-project
[系统反馈] 虚拟环境已创建于: E:\code\python\spider-project/.venv

[Agent 行动] 正在调用: write_file, 参数: E:\code\python\spider-project\spider.py
[系统反馈] 成功写入: E:\code\python\spider-project\spider.py

[Agent 行动] 正在调用: install_deps, 参数: E:\code\python\spider-project
[系统反馈] 依赖安装成功:
Successfully installed requests-2.31.0

Agent: 已完成爬虫脚本的创建，使用了requests库来爬取网页内容。你可以运行 `python spider.py` 来执行脚本。
```

## 🔧 工作流程

1. **用户输入需求**：用户提出编程需求或报错信息
2. **大模型分析**：大模型分析需求并决定下一步行动
3. **工具调用**：
   - `create_venv`：创建虚拟环境
   - `write_file`：写入代码文件
   - `install_deps`：安装依赖
   - `read_file`：读取文件内容
4. **结果反馈**：工具执行结果反馈给大模型
5. **持续交互**：根据需要进行多轮交互，直到任务完成

## 📁 项目结构

```
├── main.py          # 主入口文件
├── llm_client.py    # 大模型客户端
├── file_tool.py     # 工具实现
├── system_prompt.md # 系统提示词
├── tools_schema.json # 工具描述
├── .env             # 环境变量配置
├── .gitignore       # Git忽略文件
└── README.md        # 项目说明
```

## ⚙️ 配置说明

### 环境变量

| 变量名 | 描述 | 示例 |
|-------|------|------|
| API_KEY | 大模型API密钥 | sk-xxxxxxxxxxxxxxxxxxxxxxxx |
| BASE_URL | 大模型API地址 | https://api.openai.com/v1 |
| MODEL_NAME | 使用的模型名称 | gpt-3.5-turbo |

### 工具描述

项目使用 `tools_schema.json` 文件定义可用工具：

- `create_venv`：创建虚拟环境
- `install_deps`：安装依赖
- `read_file`：读取文件
- `write_file`：写入文件

## 🎯 示例场景

### 场景1：创建新项目

```
你: 帮我创建一个Flask项目，实现一个简单的API
Agent: 好的，我来帮你创建Flask项目。首先创建虚拟环境，然后编写Flask应用。

[Agent 行动] 正在调用: create_venv, 参数: E:\code\python\flask-api
[系统反馈] 虚拟环境已创建于: E:\code\python\flask-api/.venv

[Agent 行动] 正在调用: write_file, 参数: E:\code\python\flask-api\app.py
[系统反馈] 成功写入: E:\code\python\flask-api\app.py

[Agent 行动] 正在调用: install_deps, 参数: E:\code\python\flask-api
[系统反馈] 依赖安装成功:
Successfully installed Flask-2.0.1

Agent: 已完成Flask项目的创建，你可以运行 `python app.py` 来启动API服务。
```

### 场景2：修复代码错误

```
你: 我运行脚本时遇到了错误：ModuleNotFoundError: No module named 'requests'
Agent: 这是因为缺少requests模块，我来帮你安装它。

[Agent 行动] 正在调用: install_deps, 参数: E:\code\python\project
[系统反馈] 依赖安装成功:
Successfully installed requests-2.31.0

Agent: 已安装requests模块，现在你可以重新运行脚本了。
```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 联系方式

- GitHub: [JIAshu666](https://github.com/JIAshu666)

---

**享受编程的乐趣！** 🎉