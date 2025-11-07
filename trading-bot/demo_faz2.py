"""
Trading Bot - Faz 2 Demo
=========================

Faz 2 modüllerini test etmek için demo script.
PostgreSQL, Redis ve TradeHistoryManager kullanımı.

Kullanım:
    python demo_faz2.py

Not: Gerçek PostgreSQL ve Redis olmazsa hata verir.
     Test için mock'lu testleri kullan: pytest faz2/

Author: Trading Bot Team
Version: 1.0
Python: 3.10+
"""

import sys
from pathlib import Path
from datetime import datetime
import time

# Parent dizini path'e ekle
sys.path.insert(0, str(Path(__file__).parent))

try:
    from src.database.postgres_manager import PostgresManager, DatabaseError
    from src.database.redis_manager import RedisManager, RedisError
    from src.database.trade_history_manager import TradeHistoryManager, TradeHistoryError
except ImportError as e:
    print(f"❌ Import hatası: {e}")
    print("💡 Dosyaların doğru dizinde olduğundan emin olun")
    sys.exit(1)


def print_section(title: str):
    """Bölüm başlığı yazdır."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_postgres():
    """PostgreSQL Manager testi."""
    print_section("📦 POSTGRESQL MANAGER TEST")
    
    try:
        # Manager oluştur
        db = PostgresManager(
            host="localhost",
            port=5432,
            database="trading_bot",
            user="trading_user",
            password="password",
            min_conn=1,
            max_conn=5
        )
        print(f"✅ Manager oluşturuldu: {db}")
        
        # Bağlan
        print("\n🔌 Bağlanıyor...")
        db.connect()
        print("✅ PostgreSQL bağlantısı başarılı!")
        
        # Health check
        print("\n💓 Health check...")
        health = db.health_check()
        print(f"✅ Healthy: {health['healthy']}")
        print(f"   Latency: {health['latency_ms']} ms")
        print(f"   Pool: {health['pool']}")
        
        # Tabloları oluştur
        print("\n🗄️ Tabloları oluşturuyor...")
        if not db.table_exists('trades'):
            db.create_tables()
            print("✅ Tablolar oluşturuldu!")
        else:
            print("✅ Tablolar zaten mevcut")
        
        # İstatistikler
        print("\n📊 Veritabanı istatistikleri...")
        stats = db.get_stats()
        for table, count in stats.items():
            status = "✅" if count >= 0 else "❌"
            print(f"   {status} {table}: {count} kayıt")
        
        # Basit query
        print("\n🔍 Test query...")
        result = db.execute("SELECT 1 as test", fetch_one=True)
        print(f"✅ Query sonucu: {result}")
        
        # Kapat
        db.close()
        print("\n✅ PostgreSQL test tamamlandı!")
        
        return db
        
    except DatabaseError as e:
        print(f"\n❌ PostgreSQL hatası: {e}")
        print("\n💡 Çözüm:")
        print("   docker run -d --name trading-postgres -p 5432:5432 \\")
        print("     -e POSTGRES_DB=trading_bot \\")
        print("     -e POSTGRES_USER=trading_user \\")
        print("     -e POSTGRES_PASSWORD=password \\")
        print("     postgres:15")
        return None
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        return None


def test_redis():
    """Redis Manager testi."""
    print_section("🔴 REDIS MANAGER TEST")
    
    try:
        # Manager oluştur
        redis = RedisManager(
            host="localhost",
            port=6379,
            db=0
        )
        print(f"✅ Manager oluşturuldu: {redis}")
        
        # Bağlan
        print("\n🔌 Bağlanıyor...")
        redis.connect()
        print("✅ Redis bağlantısı başarılı!")
        
        # Health check
        print("\n💓 Health check...")
        health = redis.health_check()
        print(f"✅ Healthy: {health['healthy']}")
        print(f"   Latency: {health['latency_ms']} ms")
        print(f"   Keys: {health['key_count']}")
        print(f"   Memory: {health['used_memory_mb']} MB")
        
        # Key-value test
        print("\n🔑 Key-value operasyonları...")
        redis.set('demo_key', {'test': 'value', 'timestamp': datetime.now().isoformat()}, ttl=60)
        value = redis.get('demo_key')
        print(f"✅ Set/Get: {value}")
        
        # Hash test
        print("\n#️⃣ Hash operasyonları...")
        redis.hset('demo_hash', 'field1', 'value1')
        redis.hset('demo_hash', 'field2', 'value2')
        hash_value = redis.hget('demo_hash', 'field1')
        print(f"✅ Hash get: {hash_value}")
        
        # List test
        print("\n📋 List operasyonları...")
        redis.rpush('demo_list', 'item1', 'item2', 'item3')
        items = redis.lrange('demo_list', 0, -1)
        print(f"✅ List items: {items}")
        
        # Cleanup
        print("\n🧹 Temizlik...")
        redis.delete('demo_key', 'demo_hash', 'demo_list')
        print("✅ Test key'leri silindi")
        
        # Kapat
        redis.close()
        print("\n✅ Redis test tamamlandı!")
        
        return redis
        
    except RedisError as e:
        print(f"\n❌ Redis hatası: {e}")
        print("\n💡 Çözüm:")
        print("   docker run -d --name trading-redis -p 6379:6379 redis:7")
        return None
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        return None


def test_trade_history():
    """Trade History Manager testi."""
    print_section("📊 TRADE HISTORY MANAGER TEST")
    
    try:
        # Managers'ları başlat
        print("🔧 Managers'ları başlatıyor...")
        
        postgres = PostgresManager(
            host="localhost",
            database="trading_bot",
            user="trading_user",
            password="password"
        )
        postgres.connect()
        
        # Tabloları oluştur
        if not postgres.table_exists('trades'):
            postgres.create_tables()
        
        redis = RedisManager(host="localhost")
        redis.connect()
        
        # Trade History Manager
        thm = TradeHistoryManager(postgres, redis)
        print("✅ TradeHistoryManager hazır")
        
        # Trade oluştur
        print("\n📈 Demo trade oluşturuyor...")
        trade_id = thm.create_trade(
            symbol='BTCUSDT',
            side='LONG',
            entry_price=50000.0,
            quantity=0.1,
            stop_loss=49000.0,
            take_profit=52000.0,
            rr_ratio=2.0,
            signal_confidence=0.85,
            signal_type='DEMO',
            timeframe='15m',
            notes='Faz 2 demo trade'
        )
        print(f"✅ Trade oluşturuldu: {trade_id[:8]}...")
        
        # Trade'i al
        print("\n🔍 Trade bilgisi alınıyor...")
        trade = thm.get_trade(trade_id)
        print(f"✅ Symbol: {trade['symbol']}")
        print(f"   Side: {trade['side']}")
        print(f"   Entry: ${trade['entry_price']}")
        print(f"   Quantity: {trade['quantity']}")
        print(f"   RR: {trade['rr_ratio']}")
        
        # Pozisyon güncelle
        print("\n📊 Pozisyon güncelleniyor...")
        thm.update_position(trade_id, current_price=51000.0)
        print("✅ Pozisyon güncellendi (51000 USDT)")
        
        # Açık pozisyonlar
        print("\n📋 Açık pozisyonlar...")
        positions = thm.get_open_positions()
        print(f"✅ Toplam açık pozisyon: {len(positions)}")
        
        # Trade'i kapat
        print("\n🎯 Trade kapatılıyor...")
        time.sleep(1)  # Kısa bekleme (duration için)
        result = thm.close_trade(
            trade_id,
            exit_price=52000.0,
            exit_reason='TP_HIT',
            fees=5.0,
            notes='Demo trade başarılı'
        )
        
        print(f"✅ Trade kapatıldı!")
        print(f"   PnL: ${result['pnl']:.2f}")
        print(f"   PnL %: {result['pnl_percentage']:.2f}%")
        print(f"   Net PnL: ${result['net_pnl']:.2f}")
        print(f"   Actual RR: {result['actual_rr']:.2f}")
        print(f"   Duration: {result['duration_seconds']:.0f}s")
        print(f"   Exit Reason: {result['exit_reason']}")
        
        # Son trade'ler
        print("\n📜 Son trade'ler...")
        recent = thm.get_recent_trades(limit=5)
        print(f"✅ Son {len(recent)} trade:")
        for i, t in enumerate(recent, 1):
            pnl_sign = "+" if t.get('net_pnl', 0) > 0 else ""
            print(f"   {i}. {t['symbol']} {t['side']} - "
                  f"PnL: {pnl_sign}${t.get('net_pnl', 0):.2f}")
        
        # İstatistikler
        print("\n📊 Genel istatistikler...")
        stats = thm.get_stats()
        print(f"✅ Toplam trade: {stats['total_trades']}")
        print(f"   Kazanan: {stats['winning_trades']}")
        print(f"   Kaybeden: {stats['losing_trades']}")
        print(f"   Win Rate: {stats['win_rate']:.2f}%")
        print(f"   Profit Factor: {stats['profit_factor']:.2f}")
        print(f"   Avg RR: {stats['avg_actual_rr']:.2f}")
        
        # Kapat
        postgres.close()
        redis.close()
        print("\n✅ Trade History Manager test tamamlandı!")
        
        return True
        
    except TradeHistoryError as e:
        print(f"\n❌ Trade History hatası: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ana fonksiyon."""
    print("\n" + "🚀" * 30)
    print("  TRADING BOT - FAZ 2 DEMO")
    print("  Database Layer Test")
    print("🚀" * 30)
    
    # PostgreSQL test
    postgres_ok = test_postgres() is not None
    
    # Redis test
    redis_ok = test_redis() is not None
    
    # Trade History test (sadece her ikisi de çalışıyorsa)
    if postgres_ok and redis_ok:
        trade_history_ok = test_trade_history()
    else:
        trade_history_ok = False
        print_section("⚠️ TRADE HISTORY MANAGER ATLANILDI")
        print("PostgreSQL veya Redis çalışmıyor")
    
    # Özet
    print_section("📋 TEST SONUÇLARI")
    print(f"PostgreSQL Manager:     {'✅ BAŞARILI' if postgres_ok else '❌ BAŞARISIZ'}")
    print(f"Redis Manager:          {'✅ BAŞARILI' if redis_ok else '❌ BAŞARISIZ'}")
    print(f"Trade History Manager:  {'✅ BAŞARILI' if trade_history_ok else '❌ BAŞARISIZ'}")
    
    if postgres_ok and redis_ok and trade_history_ok:
        print("\n🎉 TÜM TESTLER BAŞARILI!")
        print("✅ Faz 2 modülleri çalışıyor")
        print("🚀 Faz 3'e geçmeye hazırsınız!")
    else:
        print("\n⚠️ BAZI TESTLER BAŞARISIZ")
        print("💡 Gerekli servislerin çalıştığından emin olun:")
        if not postgres_ok:
            print("   - PostgreSQL (port 5432)")
        if not redis_ok:
            print("   - Redis (port 6379)")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Demo durduruldu (Ctrl+C)")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
