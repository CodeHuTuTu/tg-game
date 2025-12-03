import os
import sys
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List, Dict, Any
import logging

# 确保 src 模块可以被导入
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.database.models import User, ShopItem, ShopSnapshot, OperationLog

logger = logging.getLogger(__name__)


class UserService:
    """用户服务"""

    @staticmethod
    def get_or_create_user(session: Session, user_id: int) -> User:
        """获取或创建用户"""
        user = session.query(User).filter(User.user_id == user_id).first()
        if not user:
            user = User(user_id=user_id)
            session.add(user)
            session.commit()
            logger.info(f"创建新用户: {user_id}")
        return user

    @staticmethod
    def update_user_info(session: Session, user_id: int, data: Dict[str, Any]):
        """更新用户信息"""
        user = UserService.get_or_create_user(session, user_id)
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        session.commit()
        return user

    @staticmethod
    def get_user_info(session: Session, user_id: int) -> Optional[User]:
        """获取用户信息"""
        return session.query(User).filter(User.user_id == user_id).first()


class ShopService:
    """商店服务"""

    @staticmethod
    def save_shop_snapshot(session: Session, user_id: int, shop_data: Dict[str, Any], refresh_time: Optional[str] = None) -> ShopSnapshot:
        """保存商店快照"""
        snapshot = ShopSnapshot(
            user_id=user_id,
            snapshot_data=shop_data,
            refresh_time=refresh_time
        )
        session.add(snapshot)
        session.commit()
        logger.info(f"保存用户 {user_id} 的商店快照")
        return snapshot

    @staticmethod
    def get_latest_shop_snapshot(session: Session, user_id: int) -> Optional[ShopSnapshot]:
        """获取用户最新的商店快照"""
        return session.query(ShopSnapshot).filter(
            ShopSnapshot.user_id == user_id
        ).order_by(ShopSnapshot.created_at.desc()).first()

    @staticmethod
    def parse_and_save_shop(session: Session, user_id: int, shop_text: str):
        """解析并保存商店内容"""
        from src.utils.shop_parser import ShopParser
        parser = ShopParser()
        shop_data = parser.parse_shop_text(shop_text)
        
        return ShopService.save_shop_snapshot(
            session, 
            user_id, 
            shop_data,
            refresh_time=parser.extract_refresh_time(shop_text)
        )


class OperationService:
    """操作日志服务"""

    @staticmethod
    def log_operation(
        session: Session,
        user_id: int,
        operation_type: str,
        operation_content: str = None,
        success: bool = True,
        response: str = None
    ):
        """记录操作"""
        log = OperationLog(
            user_id=user_id,
            operation_type=operation_type,
            operation_content=operation_content,
            success=success,
            response=response
        )
        session.add(log)
        session.commit()
        return log

    @staticmethod
    def get_user_operations(session: Session, user_id: int, limit: int = 50) -> List[OperationLog]:
        """获取用户的操作日志"""
        return session.query(OperationLog).filter(
            OperationLog.user_id == user_id
        ).order_by(OperationLog.created_at.desc()).limit(limit).all()
