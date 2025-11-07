import requests

url = "https://api.binance.com/api/v3/ping"
response = requests.get(url)

if response.status_code == 200:
    print("✅ API çalışıyor!")
else:
    print(f"❌ API hatası: {response.status_code}")
