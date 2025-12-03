# 修仙游戏助手 Bot

一个 Telegram 机器人，帮助你更高效地进行修仙游戏。

## 功能特性

- 📋 **快捷指令菜单** - 一键发送常用指令
- 🏪 **智能商店助手** - 自动解析商店物品，生成购买指令
- ⚔️ **装备管理** - 快速查看和管理装备
- ⚡ **突破系统** - 突破助手和成功率计算
- 💊 **丹药系统** - 丹药管理和使用
- 📊 **数据持久化** - PostgreSQL 数据库存储

## 技术栈

- **Python 3.11**
- **python-telegram-bot** - Telegram Bot Framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - 数据库
- **Docker & Docker Compose** - 容器化部署

## 快速开始

### 前置条件

- Docker & Docker Compose
- Telegram Bot Token（从 BotFather 获取）
- 你的 Telegram User ID

### 部署步骤

1. **克隆或复制项目**
   ```bash
   cd xianxia-bot
   ```

2. **配置文件**
   - 复制配置文件示例：
     ```bash
     cp config/config.example.yaml config/config.yaml
     cp .env.example .env
     ```
   
   - 编辑 `config/config.yaml` 填写你的信息：
     ```yaml
     telegram:
       bot_token: "YOUR_BOT_TOKEN_HERE"  # 从 BotFather 获取
       user_id: 123456789                 # 你的 Telegram User ID
       game_bot_username: "mei_nai_bot"  # 游戏机器人用户名
     
     database:
       url: "postgresql://xianxia_user:xianxia_password@postgres:5432/xianxia_db"
     ```
   
   - 编辑 `.env` 文件（可选，用于 Docker）：
     ```
     DB_USER=xianxia_user
     DB_PASSWORD=your_secure_password
     DB_NAME=xianxia_db
     BOT_TOKEN=your_bot_token
     ```

3. **启动服务**
   ```bash
   docker-compose up -d
   ```
   
   查看日志：
   ```bash
   docker-compose logs -f bot
   ```

4. **停止服务**
   ```bash
   docker-compose down
   ```

## 配置说明

### config/config.yaml

```yaml
# Telegram Bot 配置
telegram:
  bot_token: "YOUR_BOT_TOKEN_HERE"    # 机器人 Token
  user_id: 123456789                   # 你的用户 ID
  game_bot_id: 987654321              # 游戏机器人的 ID（可选）
  game_bot_username: "mei_nai_bot"    # 游戏机器人的用户名

# 数据库配置
database:
  url: "postgresql://user:password@host:port/dbname"
  pool_size: 10
  max_overflow: 20
  pool_recycle: 3600

# 应用配置
app:
  log_level: "INFO"                    # 日志级别
  log_file: "./logs/bot.log"           # 日志文件
  debug: false                         # 调试模式

# 定时任务配置
scheduler:
  sync_interval: 60                    # 自动同步间隔（分钟）
  sync_on_startup: true                # 启动时同步

# 商店配置
shop:
  history_days: 30                     # 保留历史记录天数
  max_snapshots: 100                   # 最多保存快照数

# 功能开关
features:
  auto_sync: true                      # 启用自动同步
  enable_web: true                     # 启用 Web 界面
  web_port: 8080                       # Web 端口
```

## 使用指南

### 菜单操作

1. 发送 `/start` 启动 Bot
2. 点击相应菜单按钮选择功能
3. 按照提示操作

### 商店助手

1. 选择 🏪 **商店助手**
2. 点击 **📥 输入商店内容**
3. 从游戏 Bot 复制商店信息，粘贴到 Bot
4. Bot 自动解析并生成购买按钮
5. 点击物品购买按钮自动生成指令

### 快捷指令

- 点击任何指令按钮，Bot 会生成相应的指令
- 复制指令内容
- 发送给游戏 Bot

## 数据库

### 表结构

- **users** - 用户信息（等级、灵石、装备等）
- **shop_items** - 商店物品
- **shop_snapshots** - 商店快照（历史记录）
- **operation_logs** - 操作日志

### 初始化

首次启动时自动创建所有表。

## 常见问题

### Q: 怎样获取 Bot Token？
**A:** 在 Telegram 中找到 @BotFather，按照提示创建机器人即可获取 Token。

### Q: 怎样获取我的 User ID？
**A:** 在 Telegram 中找到 @userinfobot，它会显示你的 User ID。

### Q: 能否转发指令给游戏 Bot？
**A:** 目前版本需要手动复制指令并发送。后续版本可能增加自动转发功能（需要特殊权限）。

### Q: 如何查看日志？
**A:** 
- Docker 环境：`docker-compose logs -f bot`
- 日志文件：`logs/bot.log`

### Q: 数据库连接失败？
**A:** 
- 检查 PostgreSQL 是否正在运行
- 检查 `config/config.yaml` 中的数据库配置
- 确认数据库用户名和密码正确

## 开发

### 项目结构

```
xianxia-bot/
├── src/
│   ├── main.py                 # 入口文件
│   ├── bot.py                  # Bot 核心
│   ├── handlers/               # 事件处理器
│   │   ├── start_handler.py    # 启动和菜单
│   │   ├── shop_handler.py     # 商店处理
│   │   └── command_handler.py  # 命令处理
│   ├── services/               # 业务逻辑层
│   │   └── db_service.py       # 数据库操作
│   ├── database/               # 数据库模块
│   │   └── models.py           # 数据模型
│   └── utils/                  # 工具函数
│       ├── config.py           # 配置管理
│       ├── logger.py           # 日志配置
│       ├── shop_parser.py      # 商店解析
│       └── menu_helper.py      # 菜单帮助
├── config/
│   ├── config.yaml             # 配置文件
│   └── config.example.yaml     # 配置示例
├── web/                        # Web 界面（可选）
├── Dockerfile                  # Docker 配置
├── docker-compose.yml          # Docker Compose 配置
├── requirements.txt            # Python 依赖
└── README.md                   # 本文件
```

### 添加新功能

1. 在 `src/handlers/` 中创建新的处理器
2. 在 `src/bot.py` 中注册处理器
3. 在菜单中添加相应按钮

## 许可证

MIT

## 支持

如有问题或建议，请提交 Issue 或 Pull Request。
