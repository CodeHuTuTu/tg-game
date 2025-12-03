# PostgreSQL 连接问题修复 ✅

## 问题诊断

错误信息：
```
connection to server at "localhost" (::1), port 5432 failed: Connection refused
```

**原因**：Bot 容器在尝试连接到 `localhost:5432`，但：
1. PostgreSQL 服务名在 Docker 中是 `postgres`，不是 `localhost`
2. Bot 容器在 Docker 启动时还未等到数据库完全初始化

---

## 修复内容

### ✅ 已修改的文件（共 3 个）

1. ✅ `src/utils/config.py` - 修改默认数据库主机从 `localhost` 改为 `postgres`
2. ✅ `config/config.example.yaml` - 更新示例配置的数据库连接字符串
3. ✅ `docker-compose.yml` - 移除过时的 `version` 字段
4. ✅ `src/bot.py` - 添加数据库连接重试机制（30 次重试，每次延迟 2 秒）

### 具体修复

#### 1. Docker 主机名配置
```python
# 之前
host = os.getenv("DB_HOST", "localhost")

# 之后
host = os.getenv("DB_HOST", "postgres")  # Docker 中使用服务名
```

#### 2. 重试机制
```python
# 新增重试逻辑，确保等待数据库就绪
db = self._init_database(max_retries=30, retry_delay=2)
# 会尝试 30 次连接，每次间隔 2 秒，共等待最长 60 秒
```

---

## 快速修复步骤

### 在服务器上执行

```bash
# 1. 进入项目目录
cd /home/lil/containers/tg-game/xianxia-bot

# 2. 获取最新代码
git pull origin main

# 3. 完全清理（谨慎操作）
docker-compose down
docker system prune -a --volumes --force

# 4. 重新构建
docker-compose build --no-cache

# 5. 启动
docker-compose up -d

# 6. 查看日志（等待 30-60 秒让数据库初始化）
docker-compose logs -f bot

# 应该看到：
# xianxia_bot  | 尝试连接数据库... (1/30)
# xianxia_bot  | 尝试连接数据库... (2/30)
# ... 几秒后 ...
# xianxia_bot  | ✅ 数据库初始化成功
# xianxia_bot  | Bot 初始化完成
```

---

## ✅ 成功标志

应该看到这样的日志序列：

```
xianxia_bot  | 尝试连接数据库... (1/30)
xianxia_bot  | 尝试连接数据库... (2/30)
xianxia_bot  | 尝试连接数据库... (3/30)
xianxia_bot  | ✅ 数据库初始化成功
xianxia_bot  | Bot 初始化完成
xianxia_bot  | 正在启动 Bot...
```

**没有** `connection refused` 错误就表示修复成功了！✅

---

## 验证修复

修复后可以验证数据库连接是否正常：

```bash
# 检查数据库容器是否运行
docker-compose ps
# 应该看到 xianxia_db 和 xianxia_bot 都是 Up

# 检查数据库日志
docker-compose logs postgres

# 进入数据库容器测试连接
docker-compose exec postgres psql -U xianxia_user -d xianxia_db -c "\dt"
# 应该看到几个表
```

---

## 关键改变

| 项目 | 旧值 | 新值 | 说明 |
|------|------|------|------|
| DB_HOST | localhost | postgres | Docker 网络中的服务名 |
| 连接重试 | 无 | 30 次 | 等待数据库启动 |
| 重试延迟 | N/A | 2 秒 | 每次重试间隔 |

---

## 原理解释

### 为什么要改 `localhost` 为 `postgres`？

在 Docker Compose 中：
- 每个服务有一个网络别名，就是 `service_name`
- `postgres` 容器在 Docker 网络中的域名是 `postgres`
- Bot 容器可以通过 `postgres:5432` 访问数据库

```
Docker 网络中的访问方式：
- Bot 容器 → postgres 容器 (通过 postgres:5432)
- 不能用 localhost (那是指 Bot 容器本身)
```

### 为什么需要重试机制？

```
启动顺序：
1. 14:21:18 - docker-compose 启动
2. 14:21:18 - postgres 容器开始启动
3. 14:21:19 - bot 容器启动并尝试连接
   ❌ 此时 postgres 还在初始化中
   ✅ 重试机制会等待 postgres 就绪
4. 14:21:20-25 - postgres 完全就绪
5. 14:21:25 - bot 连接成功
```

---

## 如果还有问题

### 问题：`connection refused` 仍然出现

**检查**：
```bash
# 检查数据库是否真的运行
docker-compose ps

# 如果 postgres 没有 Up，查看为什么启动失败
docker-compose logs postgres

# 检查网络
docker network ls
docker network inspect tg-game_xianxia_network
```

### 问题：数据库启动很慢

**这是正常的**，PostgreSQL 第一次初始化需要 10-30 秒。重试机制会自动等待。

### 问题：其他数据库错误

```bash
# 完全重置（删除所有数据，谨慎！）
docker-compose down -v
docker system prune -a --volumes --force

# 重新启动
docker-compose up -d
```

---

## 下一步

1. ✅ 应用修复（重新部署）
2. ✅ 验证 Bot 启动成功
3. ✅ 在 Telegram 中测试 `/start`
4. ✅ 查看 `QUICKSTART.md` 了解使用方法

---

## 总结

修复的核心是：
1. 修改数据库主机从 `localhost` → `postgres`
2. 添加重试机制等待数据库启动
3. 删除过时的 docker-compose 版本号

这样 Bot 就能正确连接到数据库了！🎉

现在重新部署应该能解决问题！
