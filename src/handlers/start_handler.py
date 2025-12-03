import logging
from telegram import Update
from telegram.ext import ContextTypes
from src.utils.menu_helper import MenuHelper

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令"""
    user = update.effective_user
    logger.info(f"用户 {user.id} ({user.username}) 启动了 Bot")
    
    welcome_text = f"""
👋 欢迎, {user.first_name}!

这是一个 Telegram 修仙游戏助手，可以帮助你更高效地进行游戏。

🎮 主要功能:
• 📋 快捷指令菜单
• 🏪 智能商店助手
• ⚔️ 装备管理
• ⚡ 突破助手
• 💊 丹药管理
• 📊 数据查询

点击下方按钮开始:
    """
    
    await update.message.reply_text(
        text=welcome_text,
        reply_markup=MenuHelper.create_main_menu_keyboard()
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理按钮回调"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    logger.info(f"用户 {query.from_user.id} 点击了: {callback_data}")
    
    # 路由不同的回调
    if callback_data == "back_main":
        await MenuHelper.send_main_menu(update, context)
    
    elif callback_data == "menu_commands":
        await MenuHelper.send_menu(update, context, "commands")
    
    elif callback_data == "menu_equipment":
        await MenuHelper.send_menu(update, context, "equipment")
    
    elif callback_data == "menu_breakthrough":
        await MenuHelper.send_menu(update, context, "breakthrough")
    
    elif callback_data == "menu_potion":
        await MenuHelper.send_menu(update, context, "potion")
    
    elif callback_data == "menu_shop":
        await MenuHelper.send_menu(update, context, "shop")
    
    elif callback_data == "back_shop":
        await MenuHelper.send_menu(update, context, "shop")
    
    # 处理快速指令
    elif callback_data.startswith("cmd_"):
        await handle_command_button(update, context, callback_data)
    
    # 处理购买操作
    elif callback_data.startswith("buy_"):
        await handle_buy_button(update, context, callback_data)
    
    # 处理商店输入
    elif callback_data == "shop_input":
        await handle_shop_input(update, context)
    
    elif callback_data == "shop_view":
        await handle_shop_view(update, context)
    
    elif callback_data == "shop_buy":
        await handle_shop_buy(update, context)


async def handle_command_button(update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data: str):
    """处理快速指令按钮"""
    commands_map = {
        "cmd_start": "我要修仙",
        "cmd_my_info": "我的信息",
        "cmd_closed_cultivation": "闭关",
        "cmd_exit_cultivation": "出关",
        "cmd_check_in": "签到",
        "cmd_potion_bag": "丹药背包",
        "cmd_my_equipment": "我的装备",
        "cmd_breakthrough_info": "突破信息",
        "cmd_breakthrough": "突破",
        "cmd_refresh_shop": "刷新商店",
    }
    
    command = commands_map.get(callback_data)
    if command:
        message = f"📤 已生成指令: 【{command}】\n\n请复制上述指令并发送给 @美奈 机器人"
        await update.callback_query.edit_message_text(text=message)
    else:
        await update.callback_query.edit_message_text(text="❌ 未知的指令")


async def handle_shop_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理商店输入"""
    context.user_data['awaiting_shop_input'] = True
    await update.callback_query.edit_message_text(
        text="请发送商店内容（整个商店信息）:\n\n"
             "📝 提示: 你可以从 @美奈 机器人的【商店】命令中复制内容，然后粘贴到这里。"
    )


async def handle_shop_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理查看商店"""
    await update.callback_query.edit_message_text(
        text="📊 功能开发中...\n正在优化此功能"
    )


async def handle_shop_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理快速购买"""
    await update.callback_query.edit_message_text(
        text="💳 请先输入商店内容，以查看可购买的物品"
    )


async def handle_buy_button(update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data: str):
    """处理购买按钮"""
    # 格式: buy_位置_物品名
    parts = callback_data.split("_", 2)
    if len(parts) >= 3:
        item_name = parts[2]
        message = f"📤 购买指令: 【购买 {item_name}】\n\n请复制上述指令并发送给 @美奈 机器人"
        await update.callback_query.edit_message_text(text=message)
