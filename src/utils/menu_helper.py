from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class MenuHelper:
    """菜单帮助类"""

    # 菜单数据
    MAIN_MENU = [
        ("📋 指令菜单", "menu_commands"),
        ("🏪 商店助手", "menu_shop"),
        ("⚔️ 装备系统", "menu_equipment"),
        ("⚡ 突破系统", "menu_breakthrough"),
        ("💊 丹药系统", "menu_potion"),
        ("ℹ️ 我的信息", "my_info"),
    ]

    COMMANDS_MENU = [
        ("【我要修仙】", "cmd_start"),
        ("【我的信息】", "cmd_my_info"),
        ("【闭关】", "cmd_closed_cultivation"),
        ("【出关】", "cmd_exit_cultivation"),
        ("【签到】", "cmd_check_in"),
        ("【丹药背包】", "cmd_potion_bag"),
        ("🔙 返回主菜单", "back_main"),
    ]

    EQUIPMENT_MENU = [
        ("【我的装备】", "cmd_my_equipment"),
        ("【装备 物品名】", "cmd_equip_item"),
        ("【卸下 装备名】", "cmd_unequip_item"),
        ("🔙 返回主菜单", "back_main"),
    ]

    BREAKTHROUGH_MENU = [
        ("【突破信息】", "cmd_breakthrough_info"),
        ("【突破】", "cmd_breakthrough"),
        ("【突破 丹药名】", "cmd_breakthrough_with_potion"),
        ("🔙 返回主菜单", "back_main"),
    ]

    POTION_MENU = [
        ("【丹药背包】", "cmd_potion_bag"),
        ("【服用丹药 丹药名】", "cmd_use_potion"),
        ("【丹药信息 丹药名】", "cmd_potion_info"),
        ("🔙 返回主菜单", "back_main"),
    ]

    SHOP_MENU = [
        ("📥 输入商店内容", "shop_input"),
        ("📊 查看当前商店", "shop_view"),
        ("💳 快速购买", "shop_buy"),
        ("🔄 手动刷新商店", "cmd_refresh_shop"),
        ("🔙 返回主菜单", "back_main"),
    ]

    @staticmethod
    def create_main_menu_keyboard() -> InlineKeyboardMarkup:
        """创建主菜单键盘"""
        buttons = []
        for text, callback in MenuHelper.MAIN_MENU:
            buttons.append([InlineKeyboardButton(text, callback_data=callback)])
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def create_menu_keyboard(menu_items: List[Tuple[str, str]]) -> InlineKeyboardMarkup:
        """创建菜单键盘"""
        buttons = []
        for text, callback in menu_items:
            buttons.append([InlineKeyboardButton(text, callback_data=callback)])
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def create_shop_items_keyboard(items: List[dict]) -> InlineKeyboardMarkup:
        """为商店物品创建购买按钮"""
        buttons = []
        
        for item in items:
            name = item.get("name", "")
            position = item.get("position", 0)
            price = item.get("price", 0)
            
            text = f"购买 {name} ({price}灵石)"
            callback_data = f"buy_{position}_{name}"
            
            buttons.append([InlineKeyboardButton(text, callback_data=callback_data)])
        
        # 添加返回按钮
        buttons.append([InlineKeyboardButton("🔙 返回商店菜单", callback_data="back_shop")])
        
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """发送主菜单"""
        message = "🎮 修仙游戏助手\n选择功能:"
        await update.callback_query.edit_message_text(
            text=message,
            reply_markup=MenuHelper.create_main_menu_keyboard()
        )

    @staticmethod
    async def send_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, menu_type: str):
        """发送指定菜单"""
        menus = {
            "commands": ("📋 常用指令\n", MenuHelper.COMMANDS_MENU),
            "equipment": ("⚔️ 装备系统\n", MenuHelper.EQUIPMENT_MENU),
            "breakthrough": ("⚡ 突破系统\n", MenuHelper.BREAKTHROUGH_MENU),
            "potion": ("💊 丹药系统\n", MenuHelper.POTION_MENU),
            "shop": ("🏪 商店助手\n", MenuHelper.SHOP_MENU),
        }
        
        if menu_type not in menus:
            menu_type = "commands"
        
        title, menu_items = menus[menu_type]
        await update.callback_query.edit_message_text(
            text=title,
            reply_markup=MenuHelper.create_menu_keyboard(menu_items)
        )
