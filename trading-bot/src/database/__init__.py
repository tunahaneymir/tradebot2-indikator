"""
Trading Bot - Database Module
==============================

Database layer: PostgreSQL and Redis integration.

Modules:
    - postgres_manager: PostgreSQL connection and operations
    - redis_manager: Redis cache and pub/sub
    - trade_history_manager: Trade history storage and analysis

Author: Trading Bot Team
Version: 1.0 (Faz 3.2 - Trade History eklendi)
Python: 3.10+
"""

from src.database.postgres_manager import PostgresManager, PostgresError
from src.database.redis_manager import RedisManager, RedisError
from src.database.trade_history_manager import TradeHistoryManager, TradeHistoryError

__all__ = [
    # PostgreSQL
    'PostgresManager',
    'PostgresError',
    
    # Redis
    'RedisManager',
    'RedisError',
    
    # Trade History
    'TradeHistoryManager',
    'TradeHistoryError',
]

__version__ = '1.0.0'