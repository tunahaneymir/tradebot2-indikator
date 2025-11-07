"""
Trading Bot - FAZ 3 DEMO
=========================

BinanceManager ve RateLimiter kullanım örnekleri.

Demo Özellikleri:
    1. Connection test
    2. Market data (klines, ticker, orderbook)
    3. Account bilgileri (balance, positions)
    4. Order operations (demo - gerçek order vermez)
    5. Rate limiting demonstration
    6. Error handling

Gereksinimler:
    - Testnet API key (.env dosyasında)
    - Docker: PostgreSQL ve Redis çalışıyor olmalı
    - Python packages yüklü (requirements.txt)

Çalıştırma:
    python demo_faz3.py

Author: Trading Bot Team
Version: 1.0 (Faz 3)
Python: 3.10+
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Proje root'unu path'e ekle
sys.path.insert(0, str(Path(__file__).parent))

from src.core.config_manager import ConfigManager
from src.core.logger import setup_logger, LoggerManager
from src.binance.binance_manager import BinanceManager, BinanceError
from src.binance.rate_limiter import RateLimiter


def print_section(title: str):
    """Section başlığı yazdır."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_connection(manager: BinanceManager, logger):
    """Connection demo."""
    print_section("1. CONNECTION TEST")
    
    try:
        # Bağlan
        print("🔌 Binance API'ye bağlanılıyor...")
        manager.connect()
        
        print(f"✅ Bağlantı başarılı!")
        print(f"   📍 Testnet: {manager.testnet}")
        print(f"   📍 Base URL: {manager.base_url}")
        print(f"   📍 Connected: {manager.is_connected()}")
        
        logger.info("Connection test başarılı")
        
    except BinanceError as e:
        print(f"❌ Bağlantı hatası: {e}")
        logger.error(f"Connection error: {e}")
        raise


def demo_market_data(manager: BinanceManager, logger):
    """Market data demo."""
    print_section("2. MARKET DATA")
    
    symbol = "BTCUSDT"
    
    # 2.1. Klines (Candlestick)
    print(f"\n📊 Klines - {symbol} (1h, son 5 mum)")
    try:
        klines = manager.get_klines(symbol, '1h', limit=5)
        
        print(f"   Alınan mum sayısı: {len(klines)}")
        
        # Son mumu göster
        if klines:
            last_kline = klines[-1]
            timestamp = datetime.fromtimestamp(last_kline[0] / 1000)
            print(f"\n   Son Mum:")
            print(f"   ├─ Zaman:  {timestamp}")
            print(f"   ├─ Açılış: ${float(last_kline[1]):,.2f}")
            print(f"   ├─ Yüksek: ${float(last_kline[2]):,.2f}")
            print(f"   ├─ Düşük:  ${float(last_kline[3]):,.2f}")
            print(f"   ├─ Kapanış:${float(last_kline[4]):,.2f}")
            print(f"   └─ Hacim:  {float(last_kline[5]):,.4f}")
        
        logger.info(f"Klines alındı: {len(klines)} mum")
        
    except BinanceError as e:
        print(f"   ❌ Hata: {e}")
        logger.error(f"Klines error: {e}")
    
    # 2.2. 24h Ticker
    print(f"\n📈 24h Ticker - {symbol}")
    try:
        ticker = manager.get_ticker(symbol)
        
        last_price = float(ticker['lastPrice'])
        change = float(ticker['priceChangePercent'])
        volume = float(ticker['volume'])
        high = float(ticker['highPrice'])
        low = float(ticker['lowPrice'])
        
        change_emoji = "🟢" if change > 0 else "🔴"
        
        print(f"   ├─ Son Fiyat:  ${last_price:,.2f}")
        print(f"   ├─ 24h Değişim: {change_emoji} {change:+.2f}%")
        print(f"   ├─ 24h Yüksek:  ${high:,.2f}")
        print(f"   ├─ 24h Düşük:   ${low:,.2f}")
        print(f"   └─ 24h Hacim:   {volume:,.2f} {symbol[:-4]}")
        
        logger.info(f"Ticker alındı: {symbol}")
        
    except BinanceError as e:
        print(f"   ❌ Hata: {e}")
        logger.error(f"Ticker error: {e}")
    
    # 2.3. Order Book
    print(f"\n📖 Order Book - {symbol} (Top 3)")
    try:
        orderbook = manager.get_order_book(symbol, limit=5)
        
        bids = orderbook['bids'][:3]
        asks = orderbook['asks'][:3]
        
        print(f"\n   💵 BIDS (Alış):")
        for i, bid in enumerate(bids, 1):
            price = float(bid[0])
            qty = float(bid[1])
            print(f"      {i}. ${price:,.2f} - {qty:.4f}")
        
        print(f"\n   💰 ASKS (Satış):")
        for i, ask in enumerate(asks, 1):
            price = float(ask[0])
            qty = float(ask[1])
            print(f"      {i}. ${price:,.2f} - {qty:.4f}")
        
        # Spread
        best_bid = float(bids[0][0])
        best_ask = float(asks[0][0])
        spread = ((best_ask - best_bid) / best_bid) * 100
        
        print(f"\n   📊 Spread: {spread:.4f}%")
        
        logger.info(f"Order book alındı: {symbol}")
        
    except BinanceError as e:
        print(f"   ❌ Hata: {e}")
        logger.error(f"Order book error: {e}")
    
    # 2.4. Mark Price & Funding Rate
    print(f"\n⚖️ Mark Price & Funding Rate - {symbol}")
    try:
        mark_info = manager.get_mark_price(symbol)
        
        mark_price = float(mark_info['markPrice'])
        index_price = float(mark_info['indexPrice'])
        funding_rate = float(mark_info['lastFundingRate']) * 100
        
        print(f"   ├─ Mark Price:   ${mark_price:,.2f}")
        print(f"   ├─ Index Price:  ${index_price:,.2f}")
        print(f"   └─ Funding Rate: {funding_rate:.4f}%")
        
        logger.info(f"Mark price alındı: {symbol}")
        
    except BinanceError as e:
        print(f"   ❌ Hata: {e}")
        logger.error(f"Mark price error: {e}")


def demo_account(manager: BinanceManager, logger):
    """Account demo."""
    print_section("3. ACCOUNT INFO")
    
    # 3.1. Balance
    print("\n💰 Account Balance")
    try:
        balances = manager.get_balance()
        
        # Non-zero balances
        non_zero = [b for b in balances if float(b['walletBalance']) > 0]
        
        print(f"   Toplam asset sayısı: {len(balances)}")
        print(f"   Non-zero balances: {len(non_zero)}")
        
        if non_zero:
            print(f"\n   Top Balances:")
            for i, balance in enumerate(non_zero[:5], 1):
                asset = balance['asset']
                wallet = float(balance['walletBalance'])
                available = float(balance['availableBalance'])
                
                print(f"   {i}. {asset:8s} - Wallet: {wallet:15,.8f} | Available: {available:15,.8f}")
        
        logger.info(f"Balance alındı: {len(balances)} assets")
        
    except BinanceError as e:
        print(f"   ❌ Hata: {e}")
        logger.error(f"Balance error: {e}")
    
    # 3.2. Positions
    print("\n📊 Open Positions")
    try:
        positions = manager.get_positions()
        
        # Açık pozisyonlar (positionAmt != 0)
        open_positions = [p for p in positions if float(p['positionAmt']) != 0]
        
        print(f"   Toplam position: {len(positions)}")
        print(f"   Açık position: {len(open_positions)}")
        
        if open_positions:
            print(f"\n   Açık Pozisyonlar:")
            for i, pos in enumerate(open_positions, 1):
                symbol = pos['symbol']
                amount = float(pos['positionAmt'])
                entry = float(pos['entryPrice'])
                unrealized_pnl = float(pos['unRealizedProfit'])
                
                side = "LONG" if amount > 0 else "SHORT"
                pnl_emoji = "🟢" if unrealized_pnl > 0 else "🔴"
                
                print(f"   {i}. {symbol:10s} | {side:5s} | Amount: {abs(amount):.4f}")
                print(f"      Entry: ${entry:,.2f} | PnL: {pnl_emoji} ${unrealized_pnl:+,.2f}")
        else:
            print("   ℹ️  Açık pozisyon yok")
        
        logger.info(f"Positions alındı: {len(open_positions)} open")
        
    except BinanceError as e:
        print(f"   ❌ Hata: {e}")
        logger.error(f"Positions error: {e}")
    
    # 3.3. Open Orders
    print("\n📝 Open Orders")
    try:
        orders = manager.get_open_orders()
        
        print(f"   Açık emir sayısı: {len(orders)}")
        
        if orders:
            print(f"\n   Açık Emirler:")
            for i, order in enumerate(orders[:10], 1):
                symbol = order['symbol']
                side = order['side']
                order_type = order['type']
                price = float(order['price']) if order['price'] else 0
                qty = float(order['origQty'])
                
                print(f"   {i}. {symbol:10s} | {side:4s} {order_type:6s} | "
                      f"Price: ${price:,.2f} | Qty: {qty:.4f}")
        else:
            print("   ℹ️  Açık emir yok")
        
        logger.info(f"Orders alındı: {len(orders)} open")
        
    except BinanceError as e:
        print(f"   ❌ Hata: {e}")
        logger.error(f"Orders error: {e}")


def demo_rate_limiting(manager: BinanceManager, logger):
    """Rate limiting demo."""
    print_section("4. RATE LIMITING")
    
    print("\n⏱️ Rate Limiter Status")
    
    # Current status
    status = manager.get_rate_limit_status()
    
    usage_pct = status['usage_percentage']
    bar_length = 50
    filled = int(bar_length * usage_pct / 100)
    bar = '█' * filled + '░' * (bar_length - filled)
    
    print(f"\n   Current Usage: [{bar}] {usage_pct:.1f}%")
    print(f"   ├─ Current Weight: {status['current_weight']}/{status['max_weight']}")
    print(f"   ├─ Available:      {status['available_weight']}")
    print(f"   ├─ Requests:       {status['requests_in_window']}")
    print(f"   └─ Total Requests: {status['total_requests']}")
    
    # Rapid requests demonstration
    print(f"\n⚡ Rapid Request Test (10 requests)")
    
    start_time = time.time()
    
    for i in range(10):
        try:
            # Ticker request (weight=1)
            manager.get_ticker_price('BTCUSDT')
            print(f"   Request {i+1}/10 - ✅", end='')
            
            # Status
            status = manager.get_rate_limit_status()
            print(f" (Weight: {status['current_weight']}/{status['max_weight']})")
            
            time.sleep(0.1)  # Throttle
            
        except BinanceError as e:
            print(f"   ❌ Error: {e}")
            break
    
    elapsed = time.time() - start_time
    
    print(f"\n   ⏱️ Toplam süre: {elapsed:.2f}s")
    print(f"   📊 Final stats:")
    
    final_status = manager.get_rate_limit_status()
    print(f"      ├─ Total requests: {final_status['total_requests']}")
    print(f"      ├─ Total weight:   {final_status['total_weight_used']}")
    print(f"      └─ Waits:          {final_status['waits']}")
    
    logger.info("Rate limiting demo tamamlandı")


def demo_error_handling(manager: BinanceManager, logger):
    """Error handling demo."""
    print_section("5. ERROR HANDLING")
    
    # 5.1. Invalid symbol
    print("\n❌ Invalid Symbol Test")
    try:
        invalid_symbol = "INVALIDUSDT"
        print(f"   Testing: {invalid_symbol}")
        manager.get_ticker(invalid_symbol)
        print(f"   ⚠️ Hata oluşmadı (beklenmedik)")
        
    except BinanceError as e:
        print(f"   ✅ Beklenen hata yakalandı:")
        print(f"      Code: {e.code}")
        print(f"      Message: {e}")
        logger.info("Invalid symbol error başarıyla yakalandı")
    
    # 5.2. Invalid order (demo - gerçek order vermiyoruz)
    print("\n❌ Invalid Order Test (Simulated)")
    print(f"   ℹ️  Bu demo gerçek order vermez, sadece error handling gösterir")
    print(f"   ✅ Gerçek senaryoda invalid order parametreleri yakalanır")
    
    logger.info("Error handling demo tamamlandı")


def main():
    """Main demo function."""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                  TRADING BOT - FAZ 3 DEMO                        ║
    ║              Binance API & Rate Limiting                         ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Logger setup
    LoggerManager.initialize(log_dir="logs", level=10)  # DEBUG
    logger = setup_logger('demo_faz3')
    
    logger.info("=" * 70)
    logger.info("FAZ 3 DEMO BAŞLADI")
    logger.info("=" * 70)
    
    try:
        # Config yükle
        print("📋 Konfigürasyon yükleniyor...")
        config = ConfigManager()
        
        # Config dosyası varsa yükle, yoksa env'den al
        config_path = Path("config/config.yaml")
        if config_path.exists():
            config.load(config_path)
            print(f"   ✅ Config yüklendi: {config_path}")
        else:
            print(f"   ⚠️ Config dosyası bulunamadı, .env kullanılıyor")
            # Manuel set
            import os
            config.set('binance.api_key', os.getenv('CONFIG_BINANCE_API_KEY'))
            config.set('binance.api_secret', os.getenv('CONFIG_BINANCE_API_SECRET'))
            config.set('binance.testnet', True)
            config.set('binance.rate_limit', 1200)
            config.set('binance.timeout', 10)
        
        # Validate
        config.validate_required([
            'binance.api_key',
            'binance.api_secret'
        ])
        print(f"   ✅ Config validasyonu başarılı")
        
        # BinanceManager oluştur
        print("\n🔧 BinanceManager oluşturuluyor...")
        manager = BinanceManager(config)
        print(f"   ✅ Manager oluşturuldu")
        print(f"   📍 Testnet: {manager.testnet}")
        
        # Demo'ları çalıştır
        demo_connection(manager, logger)
        
        time.sleep(1)
        demo_market_data(manager, logger)
        
        time.sleep(1)
        demo_account(manager, logger)
        
        time.sleep(1)
        demo_rate_limiting(manager, logger)
        
        time.sleep(1)
        demo_error_handling(manager, logger)
        
        # Kapanış
        print_section("DEMO TAMAMLANDI")
        
        print("\n✅ Tüm demo'lar başarıyla tamamlandı!")
        print(f"\n📊 Özet:")
        
        stats = manager.get_rate_limit_status()
        print(f"   ├─ Toplam request:  {stats['total_requests']}")
        print(f"   ├─ Toplam weight:   {stats['total_weight_used']}")
        print(f"   └─ Rate limit wait: {stats['waits']}")
        
        print(f"\n📝 Log dosyası: logs/demo_faz3.log")
        
        # Manager'ı kapat
        manager.close()
        print(f"\n🔌 Connection kapatıldı")
        
        logger.info("=" * 70)
        logger.info("FAZ 3 DEMO TAMAMLANDI")
        logger.info("=" * 70)
        
    except BinanceError as e:
        print(f"\n❌ Binance Error: {e}")
        logger.error(f"Binance error: {e}", exc_info=True)
        return 1
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        logger.error(f"Unexpected error: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        # Logger'ları kapat
        LoggerManager.shutdown()
    
    return 0


if __name__ == "__main__":
    exit(main())