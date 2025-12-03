#!/usr/bin/env python3
"""修仙游戏助手 - 主入口"""

import os
import sys
import logging

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils.logger import setup_logging
from src.bot import XianxiaBot

logger = logging.getLogger(__name__)


def main():
    """主函数"""
    try:
        setup_logging()
        logger.info("=" * 50)
        logger.info("修仙游戏助手 Bot 启动中...")
        logger.info("=" * 50)
        
        bot = XianxiaBot()
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("\n收到中断信号，正在关闭...")
    except Exception as e:
        logger.error(f"发生错误: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
