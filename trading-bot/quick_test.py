"""
Trading Bot - Hızlı Test ve Doğrulama
======================================

API key'lerin ve konfigürasyonun doğruluğunu kontrol et.

Çalıştırma:
    python quick_test.py
"""

import sys
from pathlib import Path

# Proje root'unu path'e ekle
sys.path.insert(0, str(Path(__file__).parent))

def test_config():
    """Config yükleme testi."""
    print("=" * 70)
    print("1️⃣  CONFIG TESTI")
    print("=" * 70)
    
    try:
        from src.core.config_manager import ConfigManager
        
        config = ConfigManager()
        config.load('config/config.yaml')
        
        # API key kontrolü
        api_key = config.get('binance.api_key')
        api_secret = config.get('binance.api_secret')
        testnet = config.get('binance.testnet')
        
        print(f"✅ Config yüklendi!")
        print(f"   API Key: {api_key[:20] if api_key else 'YOK'}...")
        print(f"   API Secret: {api_secret[:20] if api_secret else 'YOK'}...")
        print(f"   Testnet: {testnet}")
        
        if not api_key or not api_secret:
            print("\n❌ HATA: API key veya secret boş!")
            print("   .env dosyasını kontrol edin:")
            print("   - CONFIG_BINANCE_API_KEY=...")
            print("   - CONFIG_BINANCE_API_SECRET=...")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Config hatası: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_imports():
    """Import testleri."""
    print("\n" + "=" * 70)
    print("2️⃣  IMPORT TESTI")
    print("=" * 70)
    
    try:
        from src.binance import BinanceManager, RateLimiter
        from src.core import ConfigManager, setup_logger
        
        print("✅ Tüm modüller import edildi!")
        return True
        
    except Exception as e:
        print(f"❌ Import hatası: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_binance_connection():
    """Binance bağlantı testi."""
    print("\n" + "=" * 70)
    print("3️⃣  BINANCE BAĞLANTI TESTI")
    print("=" * 70)
    
    try:
        from src.core.config_manager import ConfigManager
        from src.binance.binance_manager import BinanceManager
        
        # Config yükle
        config = ConfigManager()
        config.load('config/config.yaml')
        
        # Manager oluştur
        print("🔧 BinanceManager oluşturuluyor...")
        manager = BinanceManager(config)
        
        # Bağlan
        print("🔌 Binance API'ye bağlanılıyor...")
        manager.connect()
        
        print("✅ Bağlantı başarılı!")
        print(f"   Base URL: {manager.base_url}")
        print(f"   Testnet: {manager.testnet}")
        
        # Basit test - ticker al
        print("\n📊 Test: BTCUSDT ticker...")
        ticker = manager.get_ticker_price('BTCUSDT')
        price = float(ticker['price'])
        print(f"   BTC Fiyat: ${price:,.2f}")
        
        # Manager'ı kapat
        manager.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        print("\n💡 Çözümler:")
        print("   1. .env dosyasındaki API key'leri kontrol et")
        print("   2. demo.binance.com'da API key'in aktif mi kontrol et")
        print("   3. İnternet bağlantını kontrol et")
        import traceback
        traceback.print_exc()
        return False


def test_rate_limiter():
    """Rate limiter testi."""
    print("\n" + "=" * 70)
    print("4️⃣  RATE LIMITER TESTI")
    print("=" * 70)
    
    try:
        from src.binance.rate_limiter import RateLimiter
        
        limiter = RateLimiter(max_weight_per_minute=100, window_seconds=5)
        
        # Birkaç request simüle et
        for i in range(5):
            wait_time = limiter.wait_if_needed(weight=10)
            limiter.add_request(weight=10)
        
        stats = limiter.get_statistics()
        
        print("✅ Rate limiter çalışıyor!")
        print(f"   Total requests: {stats['total_requests']}")
        print(f"   Total weight: {stats['total_weight_used']}")
        print(f"   Current usage: {stats['usage_percentage']:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Rate limiter hatası: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ana test fonksiyonu."""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║              TRADING BOT - HIZLI TEST                            ║
    ║              Konfigürasyon ve Bağlantı Kontrolü                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    results = []
    
    # Testleri çalıştır
    results.append(("Config", test_config()))
    results.append(("Import", test_imports()))
    results.append(("Binance Connection", test_binance_connection()))
    results.append(("Rate Limiter", test_rate_limiter()))
    
    # Sonuçları özetle
    print("\n" + "=" * 70)
    print("📊 TEST SONUÇLARI")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ BAŞARILI" if result else "❌ BAŞARISIZ"
        print(f"   {name:25s}: {status}")
    
    print(f"\n   Toplam: {passed}/{total} test geçti")
    
    if passed == total:
        print("\n🎉 TÜM TESTLER BAŞARILI!")
        print("   demo_faz3.py çalıştırabilirsin:")
        print("   python demo_faz3.py")
        return 0
    else:
        print("\n⚠️  BAZI TESTLER BAŞARISIZ!")
        print("   Yukarıdaki hataları düzelt ve tekrar dene.")
        return 1


if __name__ == "__main__":
    exit(main())