# 部署指南

## 前置条件

- Docker & Docker Compose
- Debian 12 x64 服务器
- Telegram Bot Token
- 你的 Telegram User ID

## 完整部署步骤

### 1. 准备配置

首先，在本地或服务器上创建配置文件。

**创建 config/config.yaml：**

```bash
mkdir -p config
cp config/config.example.yaml config/config.yaml
```

编辑 `config/config.yaml`：

```yaml
telegram:
  bot_token: "你的_BOT_TOKEN"              # 从 BotFather 获取
  user_id: 你的_USER_ID                    # 从 @userinfobot 获取
  game_bot_username: "mei_nai_bot"        # 游戏机器人用户名

database:
  url: "postgresql://xianxia_user:xianxia_password@postgres:5432/xianxia_db"

app:
  log_level: "INFO"
  log_file: "./logs/bot.log"
  debug: false

scheduler:
  sync_interval: 60
  sync_on_startup: true
```

**创建 .env 文件：**

```bash
cp .env.example .env
```

编辑 `.env` 设置强密码：

```
DB_USER=xianxia_user
DB_PASSWORD=你的_安全_密码
DB_NAME=xianxia_db
DB_PORT=5432

BOT_TOKEN=你的_BOT_TOKEN
GAME_BOT_USERNAME=mei_nai_bot
```

### 2. 上传到服务器

```bash
# 本地打包
tar -czf xianxia-bot.tar.gz xianxia-bot/

# 上传到服务器
scp xianxia-bot.tar.gz user@your-server:/home/user/

# 在服务器上解压
ssh user@your-server
cd /home/user/
tar -xzf xianxia-bot.tar.gz
cd xianxia-bot
```

### 3. 启动服务

**首次启动：**

```bash
docker-compose up -d
```

**查看日志确保启动成功：**

```bash
docker-compose logs -f bot
```

你应该看到类似的输出：
```
xianxia_bot    | 2024-01-01 12:00:00 - src.bot - INFO - ==================================================
xianxia_bot    | 2024-01-01 12:00:00 - src.bot - INFO - 修仙游戏助手 Bot 启动中...
xianxia_bot    | 2024-01-01 12:00:00 - src.bot - INFO - ==================================================
xianxia_bot    | 2024-01-01 12:00:01 - src.bot - INFO - Bot 初始化完成
```

### 4. 验证运行

1. 在 Telegram 中找到你的机器人
2. 发送 `/start` 命令
3. 应该看到主菜单

### 5. 日常管理

**查看运行状态：**
```bash
docker-compose ps
```

**查看日志：**
```bash
# 实时日志
docker-compose logs -f bot

# 查看最后100行
docker-compose logs --tail=100 bot

# 查看特定时间的日志
docker-compose logs --since 1h bot
```

**重启服务：**
```bash
docker-compose restart bot
```

**完全停止：**
```bash
docker-compose down
```

**更新代码：**
```bash
# 1. 获取最新代码
git pull origin main

# 2. 重建镜像
docker-compose build

# 3. 重启服务
docker-compose up -d
```

### 6. 故障排查

**Bot 无法启动：**

检查日志：
```bash
docker-compose logs bot
```

常见原因：
- Bot Token 无效
- 配置文件格式错误
- 数据库连接失败

**数据库连接错误：**

```bash
# 检查数据库是否运行
docker-compose ps

# 查看数据库日志
docker-compose logs postgres

# 重启数据库
docker-compose restart postgres
```

**内存不足：**

检查资源使用：
```bash
docker stats
```

### 7. 备份和恢复

**备份数据库：**

```bash
docker-compose exec postgres pg_dump -U xianxia_user xianxia_db > backup_$(date +%Y%m%d).sql
```

**恢复数据库：**

```bash
docker-compose exec -T postgres psql -U xianxia_user xianxia_db < backup_20240101.sql
```

**备份整个应用：**

```bash
tar -czf xianxia-bot-backup-$(date +%Y%m%d).tar.gz xianxia-bot/
```

### 8. 高级配置

**使用反向代理（可选）：**

如果需要 Web 界面支持，可以配置 Nginx：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/xianxia-bot/web;
        index index.html;
    }
}
```

**设置开机自启：**

创建 systemd 服务文件 `/etc/systemd/system/xianxia-bot.service`：

```ini
[Unit]
Description=Xianxia Game Bot
After=docker.service
Requires=docker.service

[Service]
Type=simple
WorkingDirectory=/home/user/xianxia-bot
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

然后：
```bash
sudo systemctl daemon-reload
sudo systemctl enable xianxia-bot
sudo systemctl start xianxia-bot
```

## 监控和维护

### 监控脚本

创建 `monitor.sh`：

```bash
#!/bin/bash

# 检查容器状态
docker-compose ps

# 检查磁盘空间
df -h

# 检查内存使用
free -h

# 检查 Bot 是否在运行
if ! docker-compose ps bot | grep -q "Up"; then
    echo "Alert: Bot is not running!"
    # 可以添加发送通知的代码
fi
```

运行监控：
```bash
chmod +x monitor.sh
./monitor.sh
```

### 定期清理

```bash
# 清理未使用的 Docker 资源
docker system prune -a --volumes

# 清理旧日志
docker-compose exec bot sh -c 'find /app/logs -name "*.log.*" -mtime +30 -delete'
```

## 更多帮助

- 查看日志文件：`logs/bot.log`
- 查看 README.md 了解功能
- 联系技术支持
