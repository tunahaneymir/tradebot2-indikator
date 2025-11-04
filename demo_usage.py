"""
Config Manager ve Logger Kullanım Örneği
=========================================

Bu script, config_manager ve logger modüllerinin
nasıl kullanılacağını gösterir.

Çalıştırma:
    python demo_usage.py

.env Kullanımı:
    1. .env.example'ı kopyala: cp .env.example .env
    2. API key'leri ekle
    3. Script otomatik yükler

Author: Trading Bot Team
"""

from pathlib import Path
import time
from dotenv import load_dotenv

# .env dosyasını yükle (varsa)
load_dotenv()

# Modülleri import et
from config_manager import ConfigManager, ConfigurationError
from logger import (
    setup_logger,
    get_trading_logger,
    get_error_logger,
    get_rr_logger,
    log_performance
)


def demo_config_usage():
    """Config Manager kullanım örneği."""
    print("\n" + "=" * 60)
    print("📋 CONFIG MANAGER KULLANIMI")
    print("=" * 60)
    
    # 1. Config Manager oluştur (Singleton)
    config = ConfigManager()
    print("✅ ConfigManager instance oluşturuldu")
    
    # 2. Config dosyasını yükle
    try:
        config.load('config.yaml')
        print(f"✅ Config yüklendi: {config.config_path}")
    except ConfigurationError as e:
        print(f"❌ Config yükleme hatası: {e}")
        return
    
    # 3. Config değerlerini oku
    print("\n📖 Config Değerleri:")
    print(f"  - Environment: {config.get('system.environment')}")
    print(f"  - Log Level: {config.get('system.log_level')}")
    print(f"  - Testnet: {config.get('binance.testnet')}")
    print(f"  - Max Position: {config.get('risk.max_position_size')}")
    
    # .env'den gelen değerleri göster
    api_key = config.get('binance.api_key')
    if api_key and api_key != "":
        print(f"\n🔑 .env'den Yüklenen:")
        print(f"  - API Key: {api_key[:8]}... (gizlendi)")
        print("  ✅ .env dosyası başarıyla yüklendi!")
    else:
        print(f"\n⚠️  .env dosyası bulunamadı veya boş")
        print("  Öneri: .env.example'ı .env olarak kopyala ve doldur")
    
    # 4. Default değer ile okuma
    missing_value = config.get('nonexistent.key', 'default_value')
    print(f"  - Missing key (with default): {missing_value}")
    
    # 5. Runtime'da değer değiştir
    old_timeout = config.get('api.timeout')
    config.set('api.timeout', 60)
    new_timeout = config.get('api.timeout')
    print(f"\n🔧 Runtime değişiklik:")
    print(f"  - Eski timeout: {old_timeout}s")
    print(f"  - Yeni timeout: {new_timeout}s")
    
    # 6. Nested key erişimi
    db_host = config.get_nested('postgres', 'host')
    db_port = config.get_nested('postgres', 'port')
    print(f"\n💾 Database Config:")
    print(f"  - Host: {db_host}")
    print(f"  - Port: {db_port}")
    
    # 7. Key varlık kontrolü
    if 'binance.api_key' in config:
        print(f"\n🔑 API Key mevcut")
    
    # 8. Gerekli key'leri doğrula
    try:
        config.validate_required([
            'system.environment',
            'binance.testnet',
            'risk.max_position_size'
        ])
        print("✅ Gerekli config key'leri doğrulandı")
    except ConfigurationError as e:
        print(f"❌ Eksik config: {e}")


def demo_logger_usage():
    """Logger kullanım örneği."""
    print("\n" + "=" * 60)
    print("📝 LOGGER KULLANIMI")
    print("=" * 60)
    
    # 1. Trading logger
    trading_logger = get_trading_logger()
    print("✅ Trading logger oluşturuldu")
    
    # 2. Farklı log seviyeleri
    print("\n📋 Log Seviyeleri:")
    trading_logger.debug("Bu bir DEBUG mesajı")
    trading_logger.info("Trade açıldı: BTCUSDT LONG")
    trading_logger.warning("Yüksek volatilite tespit edildi")
    trading_logger.error("API bağlantı hatası")
    
    # 3. Extra data ile loglama
    print("\n📊 Structured Logging:")
    trading_logger.info(
        "Trade tamamlandı",
        extra={
            'extra_data': {
                'symbol': 'BTCUSDT',
                'side': 'LONG',
                'pnl': 125.50,
                'rr_achieved': 1.8
            }
        }
    )
    
    # 4. Error logger ile exception
    print("\n❌ Exception Logging:")
    error_logger = get_error_logger()
    try:
        result = 1 / 0  # ZeroDivisionError
    except ZeroDivisionError:
        error_logger.error("Hesaplama hatası", exc_info=True)
    
    # 5. RR system logger
    print("\n🎯 RR System Logging:")
    rr_logger = get_rr_logger()
    rr_logger.info(
        "RR faktörü güncellendi",
        extra={
            'extra_data': {
                'old_factor': 1.0,
                'new_factor': 1.05,
                'learning_rate': 0.015,
                'reason': 'profitable_trade'
            }
        }
    )
    
    # 6. Custom logger
    print("\n⚙️ Custom Logger:")
    custom_logger = setup_logger('my_custom_module')
    custom_logger.info("Custom modül çalışıyor")
    
    print("\n✅ Tüm log'lar logs/ dizinine kaydedildi")


@log_performance()
def demo_performance_tracking():
    """Performance tracking decorator örneği."""
    print("\n" + "=" * 60)
    print("⏱️  PERFORMANCE TRACKING")
    print("=" * 60)
    
    print("🔄 Yavaş fonksiyon çalıştırılıyor...")
    time.sleep(0.5)
    
    # Bazı hesaplamalar
    total = sum(range(1000000))
    
    print("✅ Fonksiyon tamamlandı (duration performance.log'da)")
    return total


def demo_real_world_scenario():
    """Gerçek dünya senaryosu örneği."""
    print("\n" + "=" * 60)
    print("🌍 GERÇEK DÜNYA SENARYOSU")
    print("=" * 60)
    
    # 1. Config ve logger'ı başlat
    config = ConfigManager()
    config.load('config.yaml')
    logger = get_trading_logger()
    
    logger.info("Trading bot başlatıldı")
    
    # 2. Config'den ayarları oku
    testnet = config.get('binance.testnet')
    max_position = config.get('risk.max_position_size')
    rr_min = config.get('rr_system.min_rr')
    rr_max = config.get('rr_system.max_rr')
    
    print(f"\n⚙️  Bot Ayarları:")
    print(f"  - Testnet modu: {testnet}")
    print(f"  - Max pozisyon: {max_position}")
    print(f"  - RR aralığı: {rr_min} - {rr_max}")
    
    # 3. Simüle edilmiş trade
    logger.info("Trade analizi başlatıldı", extra={
        'extra_data': {
            'symbol': 'BTCUSDT',
            'timeframe': '15m',
            'signal_confidence': 0.75
        }
    })
    
    # Risk kontrolü
    if max_position > 0.05:
        logger.warning(
            "Yüksek risk tespit edildi",
            extra={'extra_data': {'max_position': max_position}}
        )
    
    # Trade açma simülasyonu
    logger.info("Trade açıldı: BTCUSDT LONG @ 45000", extra={
        'extra_data': {
            'symbol': 'BTCUSDT',
            'side': 'LONG',
            'entry_price': 45000,
            'position_size': 0.02,
            'stop_loss': 44500,
            'take_profit': 45900,
            'rr_target': 1.8
        }
    })
    
    # Trade tamamlandı
    time.sleep(0.2)
    logger.info("Trade kapatıldı: BTCUSDT LONG", extra={
        'extra_data': {
            'symbol': 'BTCUSDT',
            'exit_price': 45850,
            'pnl': 170.0,
            'pnl_percent': 1.89,
            'rr_achieved': 1.7,
            'duration_seconds': 3600
        }
    })
    
    print("\n✅ Simülasyon tamamlandı (detaylar logs/trading.log'da)")


def demo_error_handling():
    """Hata yönetimi örneği."""
    print("\n" + "=" * 60)
    print("🚨 HATA YÖNETİMİ")
    print("=" * 60)
    
    logger = get_trading_logger()
    error_logger = get_error_logger()
    
    # 1. Config hatası
    print("\n1️⃣  Config Hatası Simülasyonu:")
    try:
        config = ConfigManager()
        config.load('nonexistent_config.yaml')
    except ConfigurationError as e:
        error_logger.error(f"Config yüklenemedi: {e}")
        print(f"  ❌ Yakalandı: {e}")
    
    # 2. API hatası simülasyonu
    print("\n2️⃣  API Hatası Simülasyonu:")
    try:
        # API çağrısı simülasyonu
        raise ConnectionError("Binance API'ye bağlanılamadı")
    except ConnectionError as e:
        error_logger.error("API bağlantı hatası", exc_info=True)
        logger.warning("API hatası - yeniden deneniyor...")
        print(f"  ❌ Yakalandı: {e}")
    
    # 3. Trade hatası simülasyonu
    print("\n3️⃣  Trade Hatası Simülasyonu:")
    try:
        # Yetersiz bakiye
        raise ValueError("Yetersiz bakiye: Position açılamıyor")
    except ValueError as e:
        error_logger.error(f"Trade hatası: {e}", extra={
            'extra_data': {
                'symbol': 'BTCUSDT',
                'required_margin': 1000,
                'available_margin': 500
            }
        })
        print(f"  ❌ Yakalandı: {e}")
    
    print("\n✅ Tüm hatalar loglandı (errors.log)")


def main():
    """Ana demo fonksiyonu."""
    print("\n")
    print("🚀" * 30)
    print("  TRADING BOT - CONFIG & LOGGER DEMO")
    print("🚀" * 30)
    
    try:
        # 1. Config demo
        demo_config_usage()
        
        # 2. Logger demo
        demo_logger_usage()
        
        # 3. Performance tracking demo
        result = demo_performance_tracking()
        
        # 4. Gerçek dünya senaryosu
        demo_real_world_scenario()
        
        # 5. Hata yönetimi
        demo_error_handling()
        
        print("\n" + "=" * 60)
        print("🎉 TÜM DEMO'LAR TAMAMLANDI!")
        print("=" * 60)
        print("\n📁 Oluşturulan dosyalar:")
        print("  - logs/trading.log      (Trading log'ları)")
        print("  - logs/errors.log       (Error log'ları)")
        print("  - logs/performance.log  (Performance log'ları)")
        print("  - logs/rr_system.log    (RR system log'ları)")
        print("\n💡 İpucu: Log dosyalarını incelemek için:")
        print("  tail -f logs/trading.log")
        
    except Exception as e:
        print(f"\n❌ Demo hatası: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
