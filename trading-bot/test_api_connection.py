# test_api_connection.py
from binance.client import Client
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

api_key = os.getenv("CONFIG_BINANCE_API_KEY")
api_secret = os.getenv("CONFIG_BINANCE_API_SECRET")
testnet = os.getenv("CONFIG_BINANCE_TESTNET", "false").lower() == "true"

print("🔍 Binance API bağlantısı test ediliyor...")
print(f"Testnet modu: {testnet}")

# Binance istemcisini başlat
client = Client(api_key, api_secret, testnet=testnet)

# 1️⃣ Ping testi
try:
    response = client.ping()
    print("✅ Ping başarılı:", response)
except Exception as e:
    print("❌ Ping başarısız:", e)

# 2️⃣ Gerçek veri isteği (BTCUSDT fiyatı)
try:
    ticker = client.get_symbol_ticker(symbol="BTCUSDT")
    print("📊 Veri çekildi:", ticker)
except Exception as e:
    print("❌ Veri çekilemedi:", e)
