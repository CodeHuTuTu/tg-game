import logging
import os
import sys
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# 确保 src 模块可以被导入
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils.config import config
from src.utils.logger import setup_logging
from src.database.models import Database
from src.handlers.start_handler import start_command, button_callback
from src.handlers.shop_handler import shop_input, shop_view, shop_buy, parse_shop_input
from src.handlers.command_handler import send_command_to_game_bot

logger = logging.getLogger(__name__)


class XianxiaBot:
    """修仙游戏助手 Bot"""

    def __init__(self):
        setup_logging()
        
        self.bot_token = config.bot_token
        self.user_id = config.user_id
        self.db = Database(config.db_url)
        self.db.init_db()
        
        logger.info("Bot 初始化完成")

    def run(self):
        """运行 Bot"""
        logger.info("正在启动 Bot...")
        
        # 创建应用
        app = Application.builder().token(self.bot_token).build()
        
        # 添加命令处理器
        app.add_handler(CommandHandler("start", start_command))
        
        # 添加回调查询处理器（菜单按钮）
        app.add_handler(CallbackQueryHandler(button_callback))
        
        # 添加消息处理器（用于处理普通消息）
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # 启动 Bot
        app.run_polling()

    def shutdown(self):
        """关闭 Bot"""
        self.db.close()
        logger.info("Bot 已关闭")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理普通消息"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    logger.info(f"收到来自 {user_id} 的消息: {message_text}")
    
    # 这里可以添加更多的消息处理逻辑
    # 例如：处理用户的手动输入，自动转发给游戏 Bot 等


if __name__ == "__main__":
    bot = XianxiaBot()
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在关闭...")
        bot.shutdown()
    except Exception as e:
        logger.error(f"Bot 运行出错: {e}", exc_info=True)
        bot.shutdown()
