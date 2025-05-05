from models import UserData

def get_gemini_advice(user_data: UserData, score: float) -> dict:
    prompt = f"""Aşağıdaki çevresel alışkanlıklara göre, karbon ayak izini azaltmak için 3 spesifik ve uygulanabilir öneri ver:

1. Ulaşım: Haftada {user_data.car_km} kilometre araba kullanılıyor
2. Su Kullanımı: Günlük ortalama {user_data.daily_water_use} litre su tüketiliyor
3. Plastik Kullanımı: {"Plastik kullanılıyor" if user_data.plastic_use else "Plastik kullanılmıyor"}
4. Hesaplanan skor: {score}

⚠️ Skora göre mutlaka aşağıdaki kurallara uygun şekilde genel değerlendirme ve rozet üret:

- Eğer skor 80 veya üzerindeyse:
    - general_comment: "Skorun oldukça yüksek, tebrikler! Küçük adımlarla daha da iyisini başarabilirsin.💪🌳"
    - badge: "🌸 Gezegen Koruyucusu"

- Eğer skor 50 ile 79 arasındaysa:
    - general_comment: "Skorun orta seviyede, sürdürülebilirlik için birkaç konuda gelişebilirsin."
    - badge: "🌿 Yeşeren Yolcu"

- Eğer skor 0 ile 49 arasındaysa:
    - general_comment: "Skorun düşük🥺. Endişelenme, bu önerilerle doğa dostu adımlar atmaya hemen başlayabilirsin!"
    - badge: "🥀 Çevreye Zarar Veren"

🎯 Cevabı SADECE aşağıdaki formatta bir JSON olarak üret:
- general_comment: string
- badge: string
- car_suggestion: string
- water_suggestion: string
- plastic_suggestion: string
- overall_impact: string

TÜM cevap Türkçe olsun. JSON dışında ekstra açıklama verme.
"""
    return {
        "prompt": prompt,
        "model": "gemini-1.5-pro-001",
        "temperature": 0.7,
        "max_tokens": 700
    }
