import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ShopItemData:
    """商店物品数据"""
    position: int
    name: str
    item_type: str  # 武器/防具/丹药/物品/功能丹
    rarity: str  # 凡品/灵品/天品/帝品
    price: int
    original_price: int
    discount_percent: float


class ShopParser:
    """商店文本解析器"""

    # 品级映射
    RARITY_MAP = {
        "凡品": "common",
        "灵品": "spiritual",
        "天品": "heavenly",
        "帝品": "imperial",
    }

    # 物品类型
    ITEM_TYPES = {
        "武器": "weapon",
        "防具": "armor",
        "丹药": "potion",
        "功能丹": "functional_potion",
        "物品": "item",
    }

    def parse_shop_text(self, shop_text: str) -> Dict[str, Any]:
        """解析商店文本
        
        格式示例:
        === 修仙商店 ===
        1. [凡品] 流云琴 (武器) [7%折]
           价格: 342 灵石 (原价: 369)
        """
        items = []
        
        # 分行处理
        lines = shop_text.strip().split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # 跳过标题和空行
            if not line or '===' in line or '提示:' in line or '下次' in line:
                i += 1
                continue
            
            # 匹配物品行：数字. [品级] 物品名 (类型) [折扣]
            match = re.match(r'(\d+)\.\s*\[([^\]]+)\]\s+(.+?)\s+\(([^)]+)\)\s*\[([^\]]+)\]', line)
            
            if match:
                position = int(match.group(1))
                rarity = match.group(2)
                name = match.group(3).strip()
                item_type = match.group(4).strip()
                discount_str = match.group(5).strip()
                
                # 查找下一行的价格信息
                if i + 1 < len(lines):
                    price_line = lines[i + 1].strip()
                    price_match = re.search(r'价格:\s*(\d+)\s*灵石\s*\(原价:\s*(\d+)\)', price_line)
                    
                    if price_match:
                        current_price = int(price_match.group(1))
                        original_price = int(price_match.group(2))
                        
                        # 解析折扣
                        discount_percent = self._parse_discount(discount_str, current_price, original_price)
                        
                        item_data = ShopItemData(
                            position=position,
                            name=name,
                            item_type=self.ITEM_TYPES.get(item_type, item_type),
                            rarity=self.RARITY_MAP.get(rarity, rarity),
                            price=current_price,
                            original_price=original_price,
                            discount_percent=discount_percent
                        )
                        items.append(item_data)
                        i += 2
                        continue
            
            i += 1
        
        return {
            "items": [self._item_to_dict(item) for item in items],
            "count": len(items),
            "raw_text": shop_text
        }

    @staticmethod
    def _parse_discount(discount_str: str, current_price: int, original_price: int) -> float:
        """解析折扣"""
        # 处理 "7%折" 或 "+10%" 的格式
        match = re.search(r'([+-]?)(\d+(?:\.\d+)?)', discount_str)
        if match:
            sign = match.group(1)
            value = float(match.group(2))
            
            if sign == '-' or '折' in discount_str:
                # 折扣格式
                return -value
            else:
                # 上浮格式
                return value
        
        # 计算实际折扣
        if original_price > 0:
            discount = ((current_price - original_price) / original_price) * 100
            return round(discount, 2)
        
        return 0

    @staticmethod
    def _item_to_dict(item: ShopItemData) -> Dict[str, Any]:
        """将物品数据转换为字典"""
        return {
            "position": item.position,
            "name": item.name,
            "type": item.item_type,
            "rarity": item.rarity,
            "price": item.price,
            "original_price": item.original_price,
            "discount_percent": item.discount_percent,
        }

    @staticmethod
    def extract_refresh_time(shop_text: str) -> Optional[str]:
        """提取下次刷新时间"""
        match = re.search(r'下次刷新时间:\s*([^\n]+)', shop_text)
        if match:
            return match.group(1).strip()
        return None

    @staticmethod
    def format_items_for_display(items: List[Dict[str, Any]]) -> str:
        """格式化物品列表用于展示"""
        if not items:
            return "商店暂无物品"
        
        lines = ["📦 修仙商店物品列表\n"]
        
        for item in items:
            rarity_emoji = {
                "common": "🟩",
                "spiritual": "🟦", 
                "heavenly": "🟨",
                "imperial": "🟥",
            }.get(item.get("rarity", ""), "⬜")
            
            discount = item.get("discount_percent", 0)
            discount_str = f"[{discount:+.0f}%]" if discount else ""
            
            line = f"{rarity_emoji} {item['position']}. {item['name']} ({item['type']})\n"
            line += f"   💰 {item['price']} 灵石 (原价: {item['original_price']}) {discount_str}"
            lines.append(line)
        
        return "\n".join(lines)
