import flet as ft
import random
import time
import threading
import traceback

# =============================================================================
# SORU BANKASI (Kodun İçine Gömülü - Dosya Hatası Yok)
# =============================================================================
TUM_SORULAR = [
    {
        "soru": "Türkiye'nin en doğusu ile en batısı arasında kaç dakikalık zaman farkı vardır?",
        "siklar": ["A) 60", "B) 76", "C) 45", "D) 90", "E) 30"],
        "dogru": "B",
        "konu": "Coğrafi Konum",
        "aciklama": "19 meridyen x 4 dakika = 76 dakika."
    },
    {
        "soru": "Hangisi Türkiye'de dağların kıyıya paralel uzanmasının sonucudur?",
        "siklar": ["A) Koy ve körfez azdır", "B) Ulaşım kolaydır", "C) İklim içlere sokulur", "D) Kıta sahanlığı geniştir", "E) Delta ovası kolay oluşur"],
        "dogru": "A",
        "konu": "Yerşekilleri",
        "aciklama": "Dağlar paralel olunca kıyı düzleşir, girinti çıkıntı (koy) azalır."
    },
    {
        "soru": "En fazla yağış alan ilimiz hangisidir?",
        "siklar": ["A) Trabzon", "B) Antalya", "C) Rize", "D) Muğla", "E) Zonguldak"],
        "dogru": "C",
        "konu": "İklim",
        "aciklama": "Rize, Türkiye'nin yağış şampiyonudur."
    },
    {
        "soru": "GAP projesi hangi bölgemizde uygulanmaktadır?",
        "siklar": ["A) Ege", "B) Karadeniz", "C) Güneydoğu Anadolu", "D) Doğu Anadolu", "E) İç Anadolu"],
        "dogru": "C",
        "konu": "Ekonomi",
        "aciklama": "Güneydoğu Anadolu Projesi."
    }
]

# --- RENKLER ---
class Renk:
    bg = "#F0F4F8"; primary = "#6C5CE7"; text = "#2D3436"; white = "#FFFFFF"
    success = "#00B894"; error = "#FF7675"

def main(page: ft.Page):
    # --- KRİTİK BÖLÜM: ÇALIŞAN KODUN YAPISI ---
    # Kodun tamamını try-except içine alıyoruz. Hata olsa bile gri ekran vermez, hatayı yazar.
    try:
        page.title = "KPSS PRO"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = Renk.bg
        page.padding = 20
        page.scroll = "AUTO"

        # 1. Ekrana hemen bir şey çizelim (Gri ekranı engeller)
        loading_text = ft.Text("🚀 Uygulama Başlatılıyor...", size=20, color="blue", weight="bold")
        page.add(loading_text)
        page.update()
        
        # 2. Kısa bir bekleme (Sistemin nefes alması için)
        time.sleep(0.5)

        # 3. Oyun Değişkenleri
        state = {
            "index": 0,
            "dogru": 0,
            "aktif_sorular": random.sample(TUM_SORULAR, len(TUM_SORULAR)), # Soruları karıştır
            "cevaplandi": False
        }

        # --- OYUN FONKSİYONLARI ---
        
        def oyunu_baslat(e):
            state["index"] = 0
            state["dogru"] = 0
            state["aktif_sorular"] = random.sample(TUM_SORULAR, len(TUM_SORULAR))
            soru_getir()

        def soru_getir():
            page.clean()
            
            if state["index"] >= len(state["aktif_sorular"]):
                # Oyun Bitti Ekranı
                page.add(
                    ft.Column([
                        ft.Icon("emoji_events", size=80, color=Renk.primary),
                        ft.Text("TEST BİTTİ", size=30, weight="bold"),
                        ft.Text(f"Doğru Sayısı: {state['dogru']}", size=20, color="green"),
                        ft.ElevatedButton("Tekrar Başla", on_click=oyunu_baslat, bgcolor=Renk.primary, color="white")
                    ], alignment="center", horizontal_alignment="center")
                )
                page.update()
                return

            soru = state["aktif_sorular"][state["index"]]
            state["cevaplandi"] = False

            # Soru Kartı
            page.add(
                ft.Container(
                    content=ft.Text(soru["soru"], size=18, weight="bold", text_align="center"),
                    padding=20, bgcolor="white", border_radius=15
                )
            )

            # Şıklar
            for sik in soru["siklar"]:
                page.add(
                    ft.ElevatedButton(
                        text=sik,
                        width=350,
                        on_click=lambda e, s=sik: cevap_kontrol(e, s, soru)
                    )
                )
            
            page.update()

        def cevap_kontrol(e, secilen, soru_data):
            if state["cevaplandi"]: return
            state["cevaplandi"] = True
            
            dogru_mu = soru_data["dogru"] in secilen
            if dogru_mu:
                e.control.bgcolor = Renk.success
                e.control.color = "white"
                state["dogru"] += 1
            else:
                e.control.bgcolor = Renk.error
                e.control.color = "white"
            
            e.control.update()
            
            # Otomatik geçiş
            def gecis():
                time.sleep(1)
                state["index"] += 1
                soru_getir()
            threading.Thread(target=gecis).start()

        # --- AÇILIŞ MENÜSÜ ---
        page.clean()
        page.add(
            ft.Column([
                ft.Icon("check_circle", size=60, color="green"), # Çalıştığını gösteren ikon
                ft.Text("SİSTEM HAZIR", size=20, color="green", weight="bold"),
                ft.Divider(),
                ft.Text("KPSS COĞRAFYA", size=30, weight="bold", color=Renk.text),
                ft.ElevatedButton("TESTE BAŞLA", on_click=oyunu_baslat, width=200, height=50, bgcolor=Renk.primary, color="white")
            ], alignment="center", horizontal_alignment="center", spacing=20)
        )
        page.update()

    except Exception as e:
        # HATA OLURSA GRİ EKRAN YERİNE KIRMIZI YAZI ÇIKSIN
        page.bgcolor = "white"
        page.clean()
        page.add(
            ft.Column([
                ft.Icon("error", color="red", size=50),
                ft.Text("UYGULAMA HATASI", size=25, color="red"),
                ft.Container(content=ft.Text(traceback.format_exc()), bgcolor="#FFEBEE", padding=10)
            ], scroll="AUTO")
        )
        page.update()

# --- KRİTİK GİRİŞ ---
if __name__ == "__main__":
    ft.app(target=main)