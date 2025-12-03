from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, JSON, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class User(Base):
    """用户数据模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255))
    
    # 修仙等级信息
    level = Column(String(50), default="初入凡间")  # 当前境界
    exp = Column(Float, default=0)  # 修为
    spiritual_stones = Column(Integer, default=0)  # 灵石
    
    # 装备信息（JSON 存储）
    equipment = Column(JSON, default={})
    
    # 丹药背包（JSON 存储）
    potions = Column(JSON, default={})
    
    # 状态信息
    is_closed_cultivation = Column(Boolean, default=False)  # 是否在闭关
    closed_cultivation_start = Column(DateTime, nullable=True)  # 闭关开始时间
    
    # 记录更新时间
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_user_id_updated', 'user_id', 'updated_at'),
    )


class ShopItem(Base):
    """商店物品"""
    __tablename__ = "shop_items"

    id = Column(Integer, primary_key=True)
    
    # 物品基本信息
    name = Column(String(255), nullable=False)
    item_type = Column(String(50))  # 武器/防具/丹药/物品/功能丹 等
    rarity = Column(String(50))  # 凡品/灵品/天品/帝品
    
    # 价格信息
    original_price = Column(Integer)
    current_price = Column(Integer)
    discount_percent = Column(Float, default=0)  # 折扣百分比
    
    # 快照信息
    snapshot_id = Column(Integer, nullable=False, index=True)  # 属于哪个商店快照
    position = Column(Integer)  # 商店中的位置
    
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_snapshot_position', 'snapshot_id', 'position'),
    )


class ShopSnapshot(Base):
    """商店快照（记录某个时刻的完整商店）"""
    __tablename__ = "shop_snapshots"

    id = Column(Integer, primary_key=True)
    
    # 快照信息
    user_id = Column(Integer, nullable=False, index=True)
    snapshot_data = Column(JSON, nullable=False)  # 完整的商店数据
    
    # 刷新信息
    refresh_time = Column(DateTime)  # 下次刷新时间
    
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_user_snapshot', 'user_id', 'created_at'),
    )


class OperationLog(Base):
    """操作日志"""
    __tablename__ = "operation_logs"

    id = Column(Integer, primary_key=True)
    
    # 用户信息
    user_id = Column(Integer, nullable=False, index=True)
    
    # 操作信息
    operation_type = Column(String(50), nullable=False)  # buy/equip/use_potion/breakthrough 等
    operation_content = Column(Text)  # 操作详情
    
    # 结果
    success = Column(Boolean, default=True)
    response = Column(Text)  # 游戏机器人的响应
    
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_user_operation', 'user_id', 'created_at'),
    )


class Database:
    """数据库管理"""

    def __init__(self, db_url: str):
        self.engine = create_engine(
            db_url,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600,
            echo=False
        )
        self.SessionLocal = sessionmaker(bind=self.engine)

    def init_db(self):
        """初始化数据库"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("数据库初始化成功")
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise

    def get_session(self) -> Session:
        """获取数据库会话"""
        return self.SessionLocal()

    def close(self):
        """关闭数据库连接"""
        self.engine.dispose()
