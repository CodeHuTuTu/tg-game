import os
import sys
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
import logging

# 确保 src 模块可以被导入
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

logger = logging.getLogger(__name__)


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        """加载配置文件"""
        if not self.config_path.exists():
            logger.warning(f"配置文件不存在: {self.config_path}")
            logger.info(f"请复制 config/config.example.yaml 到 config/config.yaml 并填写配置")
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f) or {}
            logger.info(f"成功加载配置文件: {self.config_path}")
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值，支持点记法（如 telegram.bot_token）"""
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value if value is not None else default

    def get_telegram_config(self) -> Dict[str, Any]:
        """获取 Telegram 配置"""
        return self.get("telegram", {})

    def get_database_config(self) -> Dict[str, Any]:
        """获取数据库配置"""
        return self.get("database", {})

    def get_app_config(self) -> Dict[str, Any]:
        """获取应用配置"""
        return self.get("app", {})

    def get_scheduler_config(self) -> Dict[str, Any]:
        """获取定时任务配置"""
        return self.get("scheduler", {})

    @property
    def bot_token(self) -> str:
        """获取 Bot Token"""
        token = self.get("telegram.bot_token")
        if not token or token == "YOUR_BOT_TOKEN_HERE":
            raise ValueError("未配置有效的 BOT_TOKEN")
        return token

    @property
    def user_id(self) -> int:
        """获取用户 ID"""
        user_id = self.get("telegram.user_id")
        if not user_id:
            raise ValueError("未配置 user_id")
        return int(user_id)

    @property
    def db_url(self) -> str:
        """获取数据库 URL"""
        db_config = self.get_database_config()
        url = db_config.get("url")
        if not url:
            # 从环境变量构建
            user = os.getenv("DB_USER", "xianxia_user")
            password = os.getenv("DB_PASSWORD", "xianxia_password")
            host = os.getenv("DB_HOST", "localhost")
            port = os.getenv("DB_PORT", "5432")
            dbname = os.getenv("DB_NAME", "xianxia_db")
            url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        return url

    @property
    def log_level(self) -> str:
        """获取日志级别"""
        return self.get("app.log_level", "INFO")

    @property
    def log_file(self) -> str:
        """获取日志文件路径"""
        return self.get("app.log_file", "./logs/bot.log")

    @property
    def sync_interval(self) -> int:
        """获取数据同步间隔（分钟）"""
        return self.get("scheduler.sync_interval", 60)

    @property
    def game_bot_id(self) -> Optional[int]:
        """获取游戏机器人 ID"""
        bot_id = self.get("telegram.game_bot_id")
        return int(bot_id) if bot_id else None

    @property
    def game_bot_username(self) -> Optional[str]:
        """获取游戏机器人用户名"""
        return self.get("telegram.game_bot_username")


# 全局配置实例
config = ConfigManager()
