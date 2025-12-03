# Docker 问题修复指南

## 问题诊断

你遇到的错误：
```
ModuleNotFoundError: No module named 'src'
```

**原因**：Docker 容器内的 Python 找不到 `src` 模块的导入路径。

---

## 修复方案（已完成）

### ✅ 已修改的文件

我已经修改了以下文件，添加了正确的 sys.path 配置：

1. ✅ `src/main.py` - 修复主入口
2. ✅ `src/bot.py` - 修复 Bot 核心
3. ✅ `src/handlers/start_handler.py` - 修复启动处理器
4. ✅ `src/handlers/shop_handler.py` - 修复商店处理器
5. ✅ `src/handlers/command_handler.py` - 修复命令处理器
6. ✅ `src/services/db_service.py` - 修复数据库服务
7. ✅ `src/utils/config.py` - 修复配置管理
8. ✅ `src/utils/logger.py` - 修复日志系统

### 修复原理

在每个 Python 文件的顶部添加了：

```python
import os
import sys

# 确保 src 模块可以被导入
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
```

这样能确保无论从哪里运行，都能找到 `src` 模块。

---

## 部署步骤

### 1. 更新代码

确保本地的 xianxia-bot 目录中的所有文件都是最新的。

从本地上传到服务器：

```bash
# 本地打包最新代码
cd /Users/elliott/Code/Git/tg-game
tar -czf xianxia-bot-fixed.tar.gz xianxia-bot/

# 上传到服务器
scp xianxia-bot-fixed.tar.gz lil@your-server:/home/lil/containers/

# 在服务器上
ssh lil@your-server
cd /home/lil/containers/
tar -xzf xianxia-bot-fixed.tar.gz
cd xianxia-bot
```

或者直接 git pull（如果已 commit）：

```bash
cd /home/lil/containers/tg-game/xianxia-bot
git pull origin main
```

### 2. 重新构建 Docker

```bash
cd /home/lil/containers/tg-game

# 停止旧容器
docker-compose down

# 清理旧镜像（可选）
docker system prune -a --volumes

# 重新构建
docker-compose build --no-cache
```

### 3. 启动服务

```bash
docker-compose up -d
```

### 4. 验证

```bash
# 查看日志（应该看到初始化成功，不再有 ModuleNotFoundError）
docker-compose logs -f bot

# 正常日志应该显示：
# xianxia_bot  | ==================================================
# xianxia_bot  | 修仙游戏助手 Bot 启动中...
# xianxia_bot  | ==================================================
# xianxia_bot  | Bot 初始化完成
```

---

## 其他注意事项

### docker-compose.yml 版本警告

你看到的这个警告：
```
WARN[0000] /home/lil/containers/tg-game/docker-compose.yml: the attribute `version` is obsolete
```

这不是错误，只是警告。可以删除 docker-compose.yml 中的 `version:` 行（通常在第一行）：

```yaml
# 删除这一行（如果存在）
# version: '3.8'

services:
  postgres:
    ...
```

---

## 快速检查清单

部署前检查：
- [ ] 已从本地上传最新代码
- [ ] `config/config.yaml` 已正确配置
- [ ] `.env` 文件已创建（或使用示例）
- [ ] Docker 正在运行
- [ ] 磁盘空间足够（>500MB）

部署后验证：
- [ ] `docker-compose ps` 显示两个容器都 Up
- [ ] `docker-compose logs bot` 没有错误
- [ ] 在 Telegram 中发送 `/start` 收到菜单

---

## 如果还有问题

### 1. 检查日志详情

```bash
# 查看完整日志（最后 50 行）
docker-compose logs bot | tail -50

# 或查看所有日志
docker-compose logs bot

# 查看数据库日志
docker-compose logs postgres
```

### 2. 检查容器是否真的启动了

```bash
docker ps -a
# 应该看到 xianxia_bot 和 xianxia_db 两个容器
```

### 3. 重新启动

```bash
# 完全重启
docker-compose restart

# 如果还是有问题，完全清理
docker-compose down
docker system prune -a --volumes  # 小心！这会删除所有数据
docker-compose up -d
```

### 4. 查看特定错误

```bash
# 如果 Bot 容器一直在重启，查看完整错误
docker-compose logs --tail=100 bot

# 查看最近的错误（不需要 -f）
docker-compose logs bot 2>&1 | grep -i error
```

---

## 验证修复成功的标志

### ✅ 成功的日志输出应该包含：

```
xianxia_bot  | ==================================================
xianxia_bot  | 修仙游戏助手 Bot 启动中...
xianxia_bot  | ==================================================
xianxia_bot  | 2024-12-03 12:34:56 - src.utils.config - INFO - 成功加载配置文件: config/config.yaml
xianxia_bot  | 2024-12-03 12:34:56 - src.utils.logger - INFO - 日志系统已初始化，日志级别: INFO，日志文件: ./logs/bot.log
xianxia_bot  | 2024-12-03 12:34:57 - src.database.models - INFO - 数据库初始化成功
xianxia_bot  | 2024-12-03 12:34:57 - src.bot - INFO - Bot 初始化完成
xianxia_bot  | 2024-12-03 12:34:58 - src.bot - INFO - 正在启动 Bot...
```

### ❌ 错误的日志输出会包含：

```
ModuleNotFoundError: No module named 'src'
```

---

## 获取帮助

1. **查看文档** - `START_HERE.md` 和 `QUICKSTART.md`
2. **检查日志** - `docker-compose logs bot`
3. **验证配置** - 检查 `config/config.yaml`
4. **重启试试** - `docker-compose restart bot`

---

## 总结

主要修复包括：
✅ 修改了所有 Python 文件的导入路径
✅ 添加了 sys.path 动态配置
✅ 确保在 Docker 容器中能正确导入

现在按照上面的"部署步骤"重新部署就应该能解决问题了！
