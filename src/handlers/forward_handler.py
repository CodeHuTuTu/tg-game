import logging
import os
import sys
from telegram import Update, User, Chat
from telegram.ext import ContextTypes

# 确保 src 模块可以被导入
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils.config import ConfigManager

logger = logging.getLogger(__name__)


class ForwardHandler:
    """处理指令转发和结果收集"""
    
    # 存储待转发的指令和用户信息
    pending_commands = {}  # {user_id: {"command": "xxx", "timestamp": xxx}}
    
    @staticmethod
    async def send_command_and_wait(
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE, 
        command: str
    ) -> None:
        """
        发送指令给游戏Bot并等待结果
        
        Args:
            update: Telegram Update 对象
            context: 上下文
            command: 要发送的指令
        """
        try:
            config = ConfigManager()
            user_id = update.effective_user.id
            game_bot_username = config.get("game_bot_username", "美奈")
            game_bot_user_id = config.get("game_bot_user_id")
            
            # 显示加载状态
            loading_msg = await update.callback_query.edit_message_text(
                text=f"⏳ 正在执行指令: 【{command}】\n\n"
                     f"向 @{game_bot_username} 发送请求中...",
                parse_mode=None
            )
            
            # 保存用户信息和消息ID用于接收回复
            context.user_data['last_command'] = command
            context.user_data['last_message_id'] = loading_msg.message_id
            context.user_data['awaiting_game_response'] = True
            
            # 如果有游戏Bot的user_id，尝试直接发送
            if game_bot_user_id:
                try:
                    bot = context.bot
                    # 尝试向游戏Bot的私聊发送指令
                    await bot.send_message(
                        chat_id=game_bot_user_id,
                        text=command
                    )
                    logger.info(f"已向 {game_bot_username} (ID: {game_bot_user_id}) 发送指令: {command}")
                    
                    # 更新消息提示
                    await bot.edit_message_text(
                        chat_id=update.effective_chat.id,
                        message_id=loading_msg.message_id,
                        text=f"✅ 指令已发送\n\n"
                             f"📤 发送内容: 【{command}】\n\n"
                             f"正在等待 @{game_bot_username} 的回复...\n"
                             f"（通常需要 1-2 秒）"
                    )
                    
                    # 记录指令用于后续匹配回复
                    context.user_data['sent_command'] = command
                    context.user_data['awaiting_response_until'] = None  # 会在 handle_game_response 中设置
                    
                except Exception as e:
                    logger.error(f"无法直接发送给游戏Bot: {e}")
                    await _fallback_to_manual(update, context, command, game_bot_username)
            else:
                # 没有游戏Bot ID，使用备选方案
                await _fallback_to_manual(update, context, command, game_bot_username)
                
        except Exception as e:
            logger.error(f"发送指令时出错: {e}")
            await update.callback_query.edit_message_text(
                text=f"❌ 执行失败: {str(e)}\n\n"
                     f"请重试或手动发送指令"
            )


async def _fallback_to_manual(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE, 
    command: str, 
    game_bot_username: str
) -> None:
    """备选方案：显示指令供用户手动复制"""
    message = (
        f"📤 已生成指令\n\n"
        f"指令内容:\n"
        f"`{command}`\n\n"
        f"📋 使用步骤:\n"
        f"1. 点击下方链接打开 @{game_bot_username}\n"
        f"2. 复制上面的指令\n"
        f"3. 粘贴到聊天框并发送\n\n"
        f"🔗 <a href='https://t.me/{game_bot_username}'>打开 @{game_bot_username}</a>"
    )
    
    await update.callback_query.edit_message_text(
        text=message,
        parse_mode="HTML"
    )


async def handle_game_bot_response(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    处理来自游戏Bot的回复消息
    
    这个函数应该在处理来自 game_bot_user_id 的消息时调用
    """
    # 这里的逻辑会在主handler中调用
    # 当收到来自游戏Bot的消息时，转发给用户
    pass
