import logging
from telegram import Update
from telegram.ext import ContextTypes
from src.utils.shop_parser import ShopParser
from src.utils.menu_helper import MenuHelper
from src.services.db_service import ShopService, OperationService
from src.database.models import Database
from src.utils.config import config

logger = logging.getLogger(__name__)


async def parse_shop_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """解析用户输入的商店内容"""
    user_id = update.effective_user.id
    shop_text = update.message.text
    
    if not context.user_data.get('awaiting_shop_input'):
        return
    
    context.user_data['awaiting_shop_input'] = False
    
    try:
        # 解析商店
        parser = ShopParser()
        shop_data = parser.parse_shop_text(shop_text)
        items = shop_data.get('items', [])
        
        if not items:
            await update.message.reply_text("❌ 无法解析商店内容，请检查格式是否正确")
            return
        
        # 保存到数据库
        db = Database(config.db_url)
        session = db.get_session()
        
        try:
            ShopService.save_shop_snapshot(session, user_id, shop_data, parser.extract_refresh_time(shop_text))
            
            # 生成展示内容
            display_text = ShopParser.format_items_for_display(items)
            display_text += f"\n\n⏱️ 下次刷新时间: {parser.extract_refresh_time(shop_text) or '未知'}"
            
            # 创建购买按钮
            keyboard = MenuHelper.create_shop_items_keyboard(items)
            
            await update.message.reply_text(
                text=display_text,
                reply_markup=keyboard
            )
            
            logger.info(f"用户 {user_id} 的商店数据已保存，共 {len(items)} 件物品")
            
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"解析商店内容出错: {e}")
        await update.message.reply_text(f"❌ 解析出错: {str(e)}")


async def shop_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """商店输入处理"""
    await update.message.reply_text("请发送商店内容...")


async def shop_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """商店查看处理"""
    user_id = update.effective_user.id
    
    try:
        db = Database(config.db_url)
        session = db.get_session()
        
        try:
            snapshot = ShopService.get_latest_shop_snapshot(session, user_id)
            
            if not snapshot:
                await update.message.reply_text("❌ 未找到商店数据，请先输入商店内容")
                return
            
            shop_data = snapshot.snapshot_data
            items = shop_data.get('items', [])
            
            display_text = ShopParser.format_items_for_display(items)
            keyboard = MenuHelper.create_shop_items_keyboard(items)
            
            await update.message.reply_text(
                text=display_text,
                reply_markup=keyboard
            )
            
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"查看商店出错: {e}")
        await update.message.reply_text(f"❌ 查看商店出错: {str(e)}")


async def shop_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """商店购买处理"""
    await update.message.reply_text("请先输入商店内容来选择购买物品")
