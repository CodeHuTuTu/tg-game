import logging
import os
import sys
from telegram import Update
from telegram.ext import ContextTypes

# 确保 src 模块可以被导入
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

logger = logging.getLogger(__name__)


async def send_command_to_game_bot(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str):
    """发送指令给游戏 Bot
    
    这个函数暂时只是显示指令，实际的转发可能需要通过其他方式实现
    """
    message = f"📤 指令已准备:\n【{command}】\n\n请复制上述指令并发送给游戏 Bot"
    await update.message.reply_text(message)
    logger.info(f"用户 {update.effective_user.id} 执行命令: {command}")
