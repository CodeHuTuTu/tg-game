# 快速开始指南

## 5 分钟快速部署

### 第一步：准备信息

你需要以下信息：

1. **Telegram Bot Token**
   - 找到 @BotFather
   - `/start` → `/newbot` → 按提示创建
   - 获得类似：`123456789:ABCDefghIjklmnoPqrsTuvWXYZ`

2. **你的 Telegram User ID**
   - 找到 @userinfobot
   - 发送任何信息
   - 获得你的 User ID，类似：`987654321`

3. **游戏机器人的用户名**
   - 一般是 `@mei_nai_bot` 或类似

### 第二步：配置文件

进入项目目录：

```bash
cd xianxia-bot
```

**第一次使用，创建配置：**

```bash
# 复制示例文件
cp config/config.example.yaml config/config.yaml
cp .env.example .env
```

**编辑 config/config.yaml**（用你喜欢的编辑器）：

```yaml
telegram:
  bot_token: "粘贴你的Bot Token"          # 例：123456789:ABCDefghIjklmnoPqrsTuvWXYZ
  user_id: 粘贴你的User ID              # 例：987654321
  game_bot_username: "mei_nai_bot"      # 保持不变或改为实际的游戏机器人
```

**编辑 .env**（可选，数据库密码）：

```
DB_PASSWORD=改成一个你想要的密码
```

### 第三步：启动服务

一键启动！

```bash
docker-compose up -d
```

等待 10-15 秒让数据库初始化...

### 第四步：验证

1. 打开 Telegram
2. 找到你的机器人（通过 BotFather 给你的链接）
3. 发送 `/start` 命令
4. **应该看到菜单界面！** ✓

如果看不到菜单，检查日志：

```bash
docker-compose logs bot
```

## 常用命令

```bash
# 启动
docker-compose up -d

# 停止
docker-compose down

# 查看日志
docker-compose logs -f bot

# 重启
docker-compose restart bot

# 查看运行状态
docker-compose ps
```

## 使用说明

### 菜单操作

1. `/start` - 显示主菜单
2. 点击按钮选择功能
3. 按照提示操作

### 核心功能

#### 🏪 商店助手

1. 点击 **🏪 商店助手**
2. 选择 **📥 输入商店内容**
3. 从 @美奈 机器人复制商店信息，粘贴到本 Bot
4. Bot 自动解析并显示购买按钮
5. 点击按钮获取购买指令

#### 📋 快捷指令

1. 点击 **📋 指令菜单**
2. 选择任何指令（如 **【我的信息】**）
3. Bot 会显示生成的指令
4. 复制指令，发送给 @美奈 机器人

## 故障排查

### "无法连接数据库"

```bash
# 检查数据库是否在运行
docker-compose ps

# 应该看到两个容器都是 Up 状态
```

### "Bot Token 无效"

- 检查 `config/config.yaml` 中的 `bot_token` 是否正确
- 从 @BotFather 重新获取确保无误

### "收不到 Bot 的回复"

```bash
# 查看完整日志
docker-compose logs bot | tail -50

# 查找 ERROR 或 WARNING
```

### "想要重新配置"

```bash
# 停止并删除（不影响数据库数据）
docker-compose down

# 编辑配置
nano config/config.yaml

# 重新启动
docker-compose up -d
```

## 常见问题

**Q: 输入商店内容时怎样复制？**
A: 在 Telegram 中：
1. 找到 @美奈 的商店消息
2. 长按消息，选择 "复制"
3. 切换到本 Bot
4. 长按输入框，选择 "粘贴"
5. 发送

**Q: 为什么点击按钮没反应？**
A: 等待 1-2 秒，或检查网络连接

**Q: 能否自动发送指令给游戏 Bot？**
A: 目前版本需要手动复制。这需要特殊权限，后续版本可能支持

**Q: 数据会被保存吗？**
A: 是的，所有数据保存在 PostgreSQL 数据库中。

**Q: 如何备份数据？**
A: 
```bash
docker-compose exec postgres pg_dump -U xianxia_user xianxia_db > backup.sql
```

**Q: 可以在多个设备上使用吗？**
A: 当前配置只支持一个 User ID。要支持多个用户需要修改代码。

## 下一步

- 详见 [README.md](README.md) 了解完整功能
- 详见 [DEPLOYMENT.md](DEPLOYMENT.md) 了解高级配置

## 需要帮助？

- 检查日志：`docker-compose logs bot`
- 确保 Docker 和 Docker Compose 已安装
- 确保 `config/config.yaml` 格式正确（YAML 对缩进敏感）
