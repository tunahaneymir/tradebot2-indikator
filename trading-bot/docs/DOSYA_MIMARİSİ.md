# 📁 TRADING BOT - TAM DOSYA MİMARİSİ

## 🌳 Tam Dizin Ağacı

```
trading-bot/                          # Ana proje dizini
│
├── .vscode/                          # VSCode ayarları
│   ├── settings.json                 # Editor ayarları
│   └── launch.json                   # Debug konfigürasyonu
│
├── src/                              # Kaynak kod
│   ├── __init__.py                   # Paket işaretleyici
│   │
│   ├── core/                         # ✅ FAZ 1 TAMAMLANDI
│   │   ├── __init__.py
│   │   ├── config_manager.py         # ✅ Config yöneticisi (348 satır)
│   │   ├── logger.py                 # ✅ Log sistemi (485 satır)
│   │   └── constants.py              # ⏳ Faz 1 (sonraki)
│   │
│   ├── database/                     # ⏳ FAZ 2 (Hafta 1-2)
│   │   ├── __init__.py
│   │   ├── postgres_manager.py       # PostgreSQL bağlantı yöneticisi
│   │   ├── redis_manager.py          # Redis önbellek yöneticisi
│   │   └── influxdb_manager.py       # InfluxDB zaman serisi
│   │
│   ├── operations/                   # ⏳ FAZ 2 & 6
│   │   ├── __init__.py
│   │   ├── trade_history_manager.py  # ⏳ Faz 2 (Trade geçmişi)
│   │   ├── shutdown_manager.py       # ⏳ Faz 6 (Kapatma yöneticisi)
│   │   ├── backup_manager.py         # ⏳ Faz 6 (Yedekleme)
│   │   └── health_monitor.py         # ⏳ Faz 6 (Sistem sağlığı)
│   │
│   ├── data/                         # ⏳ FAZ 3 (Hafta 2-3)
│   │   ├── __init__.py
│   │   ├── binance_client.py         # Binance API wrapper
│   │   ├── data_preprocessor.py      # Veri ön işleme
│   │   ├── cache_manager.py          # Redis önbellekleme
│   │   └── websocket_handler.py      # Real-time veri
│   │
│   ├── agents/                       # ⏳ FAZ 3
│   │   ├── __init__.py
│   │   ├── coin_selection_agent.py   # Coin seçim ajanı (adapte edilecek)
│   │   └── market_regime_detector.py # Piyasa rejim tespiti
│   │
│   ├── indicators/                   # ⏳ FAZ 4 (Hafta 3-4)
│   │   ├── __init__.py
│   │   ├── base_indicator.py         # Temel indikatör sınıfı
│   │   ├── supertrend.py             # SuperTrend
│   │   ├── most.py                   # MOST
│   │   ├── qqe_mod.py                # QQE MOD
│   │   ├── rvol.py                   # RVOL
│   │   └── atr.py                    # ATR
│   │
│   ├── trading/                      # ⏳ FAZ 4 & 5 (Hafta 4-5)
│   │   ├── __init__.py
│   │   ├── signal_generator.py       # Sinyal üretici
│   │   ├── order_executor.py         # Emir yürütücü
│   │   ├── position_manager.py       # Pozisyon yöneticisi
│   │   └── trading_engine.py         # Ana trading motoru
│   │
│   ├── risk/                         # ⏳ FAZ 5 (Hafta 4-5)
│   │   ├── __init__.py
│   │   ├── adaptive_rr_system.py     # Adaptif RR sistemi
│   │   ├── risk_manager.py           # Risk yöneticisi
│   │   └── portfolio_manager.py      # Portföy yöneticisi
│   │
│   ├── ml/                           # ⏳ FAZ 7 (Hafta 7-8)
│   │   ├── __init__.py
│   │   ├── feature_engineer.py       # Özellik mühendisliği
│   │   ├── model_manager.py          # Model yönetimi
│   │   └── model_trainer.py          # Model eğitimi
│   │
│   ├── rl/                           # ⏳ FAZ 7 (Hafta 7-8)
│   │   ├── __init__.py
│   │   ├── ppo_agent.py              # PPO RL ajanı
│   │   ├── environment.py            # Gym ortamı
│   │   └── reward_function.py        # Ödül fonksiyonu
│   │
│   ├── dashboard/                    # ⏳ FAZ 8 (Hafta 8-9)
│   │   ├── __init__.py
│   │   ├── learning_dashboard.py     # Öğrenme dashboard'u
│   │   ├── visual_dashboard.py       # Görsel dashboard
│   │   └── grafana_exporter.py       # Prometheus metrikleri
│   │
│   └── utils/                        # ⏳ Gerektiğinde
│       ├── __init__.py
│       ├── validators.py             # Doğrulama fonksiyonları
│       ├── decorators.py             # Yardımcı decorator'lar
│       └── helpers.py                # Genel yardımcı fonksiyonlar
│
├── config/                           # Konfigürasyon dosyaları
│   ├── config.yaml                   # ✅ Ana config (411 satır)
│   ├── config_dev.yaml               # ⏳ Development config
│   ├── config_prod.yaml              # ⏳ Production config
│   └── secrets.yaml                  # ⏳ API keys (git'de yok)
│
├── tests/                            # Test dosyaları
│   ├── __init__.py                   # ✅
│   ├── test_config_manager.py        # ✅ Config testleri (358 satır)
│   ├── test_logger.py                # ✅ Logger testleri (424 satır)
│   │
│   ├── test_postgres_manager.py      # ⏳ Faz 2
│   ├── test_trade_history.py         # ⏳ Faz 2
│   ├── test_binance_client.py        # ⏳ Faz 3
│   ├── test_coin_selection.py        # ⏳ Faz 3
│   ├── test_indicators.py            # ⏳ Faz 4
│   ├── test_signal_generator.py      # ⏳ Faz 4
│   ├── test_rr_system.py             # ⏳ Faz 5
│   ├── test_risk_manager.py          # ⏳ Faz 5
│   ├── test_trading_engine.py        # ⏳ Faz 5
│   │
│   └── integration/                  # Entegrasyon testleri
│       ├── __init__.py
│       ├── test_full_pipeline.py     # ⏳ Faz 9
│       └── test_shutdown_recovery.py # ⏳ Faz 9
│
├── state/                            # Runtime state (gitignore)
│   ├── rr_weights.json               # RR sistem ağırlıkları
│   ├── rr_learning_history.json      # RR öğrenme geçmişi
│   ├── trade_history_buffer.json     # Bekleyen DB yazmaları
│   ├── open_positions.json           # Aktif pozisyonlar
│   ├── model_checkpoint.pkl          # ML model durumu
│   ├── rl_experience_replay.pkl      # RL deneyim tamponu
│   └── system_metrics.json           # Sistem metrikleri
│
├── backups/                          # Otomatik yedekler (gitignore)
│   ├── 2025-01-04_12-00-00/
│   │   ├── state/
│   │   ├── logs/
│   │   └── models/
│   ├── 2025-01-04_13-00-00/
│   └── ...
│
├── logs/                             # Log dosyaları (gitignore)
│   ├── trading.log                   # Ana trading log
│   ├── trading.log.1                 # Rotated log
│   ├── errors.log                    # Error log
│   ├── performance.log               # Performance metrikleri
│   ├── rr_system.log                 # RR sistem log
│   └── shutdown_reports/             # Kapatma raporları
│       ├── 2025-01-04_14-30-00.json
│       └── ...
│
├── data/                             # Veri dosyaları (gitignore)
│   ├── raw/                          # Ham piyasa verisi
│   │   ├── BTCUSDT_1m_2025-01.csv
│   │   └── ...
│   ├── processed/                    # İşlenmiş veri
│   │   ├── BTCUSDT_features.parquet
│   │   └── ...
│   └── parquet/                      # Sıkıştırılmış arşivler
│       └── 2025-01.parquet
│
├── models/                           # Kaydedilmiş ML modeller (gitignore)
│   ├── coin_selector_v1.pkl          # Coin seçim modeli
│   ├── coin_selector_v2.pkl
│   ├── lightgbm_direction_v1.pkl     # Yön tahmini
│   ├── lstm_price_v1.h5              # LSTM model
│   └── ppo_agent_checkpoint_1000.zip # RL agent
│
├── scripts/                          # Yardımcı scriptler
│   ├── setup_databases.py            # ⏳ DB şema oluştur
│   ├── migrate_data.py               # ⏳ Veri taşıma
│   ├── backtest_strategy.py          # ⏳ Backtest
│   ├── generate_report.py            # ⏳ Performans raporu
│   └── cleanup.py                    # ⏳ Temizlik scripti
│
├── notebooks/                        # Jupyter notebook'lar
│   ├── 01_veri_kesfi.ipynb           # ⏳ Veri analizi
│   ├── 02_indikator_test.ipynb       # ⏳ İndikatör testleri
│   ├── 03_ml_model_egitimi.ipynb     # ⏳ ML model eğitimi
│   └── 04_performans_analizi.ipynb   # ⏳ Performans analizi
│
├── docs/                             # Dokümantasyon
│   ├── trading_bot_mimarisi_v4.1_TR.md  # ✅ Ana mimari
│   ├── RR_SYSTEM_FINAL.md                # ✅ RR sistem detayları
│   ├── FAZ1_OZET.md                      # ✅ Faz 1 özeti
│   ├── VSCODE_KURULUM.md                 # ✅ VSCode rehberi
│   ├── PROJE_YAPISI_TR.md                # ✅ Proje yapısı
│   ├── YENİ_CHAT_CONTEXT_TR.md           # ✅ Yeni chat context
│   │
│   ├── api_referans.md                   # ⏳ API dokümantasyonu
│   ├── deployment_rehberi.md             # ⏳ Deployment
│   └── sorun_giderme.md                  # ⏳ Troubleshooting
│
├── venv/                             # Python virtual environment (gitignore)
│   ├── bin/
│   ├── lib/
│   └── ...
│
├── .vscode/                          # VSCode ayarları
│   ├── settings.json                 # Editor ayarları
│   └── launch.json                   # Debug config
│
├── .git/                             # Git repository
│   └── ...
│
├── .gitignore                        # Git ignore kuralları
├── .env                              # Ortam değişkenleri (gitignore)
├── .env.example                      # Ortam değişkeni şablonu
├── requirements.txt                  # ✅ Python bağımlılıkları
├── setup.py                          # ⏳ Paket kurulum
├── README.md                         # ⏳ Proje README
├── LICENSE                           # ⏳ Lisans
├── demo_usage.py                     # ✅ Demo script (289 satır)
└── main.py                           # ⏳ Ana giriş noktası
```

---

## 📊 Dosya İstatistikleri

### ✅ Tamamlananlar (Faz 1)
```
Kaynak Kod:
  - src/core/config_manager.py    (348 satır)
  - src/core/logger.py            (485 satır)
  
Test Kod:
  - tests/test_config_manager.py  (358 satır)
  - tests/test_logger.py          (424 satır)
  
Config:
  - config/config.yaml            (411 satır)
  
Demo:
  - demo_usage.py                 (289 satır)
  
Dokümantasyon:
  - docs/FAZ1_OZET.md             (314 satır)
  - docs/VSCODE_KURULUM.md        (yeni)
  
Toplam: ~2,900 satır
Test Kapsama: >88%
```

### ⏳ Yapılacaklar (Faz 2+)
```
Faz 2 (Hafta 1-2):
  - postgres_manager.py
  - redis_manager.py
  - trade_history_manager.py
  - Testler
  
Faz 3-9 (Hafta 3-10):
  - 20+ modül
  - 30+ test dosyası
  - ML/RL modeller
  - Dashboard'lar
```

---

## 🎯 Kritik Dosya Açıklamaları

### Zorunlu Dosyalar (Şu An)
```
✅ OLMALI:
  - src/core/config_manager.py
  - src/core/logger.py
  - config/config.yaml
  - tests/test_config_manager.py
  - tests/test_logger.py
  - demo_usage.py
  - requirements.txt
  
✅ OLUŞTURULMALI (Boş):
  - src/__init__.py
  - src/core/__init__.py
  - tests/__init__.py
```

### Otomatik Oluşacak
```
🔄 KOD ÇALIŞINCA OLUŞUR:
  - logs/trading.log
  - logs/errors.log
  - logs/performance.log
  - logs/rr_system.log
```

### Git İçin
```
📝 OLUŞTURULMALI:
  - .gitignore
  - .env.example
  - README.md (opsiyonel)
```

---

## 📄 .gitignore İçeriği

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
build/
dist/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Ortam
.env
config/secrets.yaml

# State ve Loglar
state/
logs/
backups/

# Veri
data/raw/
data/processed/
*.parquet
*.csv
*.json

# Modeller
models/*.pkl
models/*.zip
models/*.h5

# Notebook'lar
.ipynb_checkpoints/

# Test
.pytest_cache/
.coverage
htmlcov/

# İşletim Sistemi
.DS_Store
Thumbs.db
```

---

## 🔗 Dosya Bağımlılıkları

### Import Grafiği (Şu An)
```python
demo_usage.py
    ├── src.core.config_manager
    │   └── yaml (external)
    └── src.core.logger
        └── logging (builtin)

test_config_manager.py
    ├── pytest (external)
    └── src.core.config_manager

test_logger.py
    ├── pytest (external)
    └── src.core.logger
```

### Gelecek Bağımlılıklar (Faz 2+)
```python
main.py
    ├── config_manager
    ├── logger
    ├── postgres_manager
    ├── trade_history_manager
    ├── binance_client
    ├── coin_selection_agent
    ├── signal_generator
    ├── adaptive_rr_system
    ├── risk_manager
    ├── trading_engine
    └── ...
```

---

## 📦 Dosya Boyutları (Tahmini)

```
Faz 1 (Mevcut):
  Kod:     833 satır    ~30 KB
  Test:    782 satır    ~28 KB
  Config:  411 satır    ~15 KB
  Demo:    289 satır    ~10 KB
  Docs:  1,200 satır    ~50 KB
  Toplam: ~133 KB

Faz 9 (Tamamlandığında - Tahmini):
  Kod:    ~15,000 satır  ~500 KB
  Test:   ~10,000 satır  ~350 KB
  Config:   ~1,000 satır  ~40 KB
  Docs:     ~5,000 satır ~200 KB
  Toplam: ~1.1 MB (kod + doc)
  
  + Models: ~50-200 MB (ML/RL modeller)
  + Data:   ~1-10 GB (piyasa verisi)
  + Logs:   ~100 MB/gün
```

---

## 🎯 Kilometre Taşı Dosyaları

```
Faz 1 ✅: config_manager.py, logger.py
Faz 2 ⏳: postgres_manager.py, trade_history_manager.py
Faz 3 ⏳: binance_client.py, coin_selection_agent.py
Faz 4 ⏳: supertrend.py, signal_generator.py
Faz 5 ⏳: adaptive_rr_system.py, trading_engine.py
Faz 6 ⏳: shutdown_manager.py, backup_manager.py
Faz 7 ⏳: model_manager.py, ppo_agent.py
Faz 8 ⏳: learning_dashboard.py, visual_dashboard.py
Faz 9 ⏳: main.py (tam entegrasyon)
```

---

**✅ Dosya mimarisi tam ve detaylı hazırlandı!**
