import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Dosya yolları ---
DATA_DIR = "data"
GRAFIK_DIR = "grafikler"

ADV_FILE = f"{DATA_DIR}/Advertising.csv"
TIPS_FILE = f"{DATA_DIR}/tips.csv"
RETAIL_FILE = f"{DATA_DIR}/OnlineRetail2.csv"


# --- Fonksiyonlar ---
def klasor_kontrol():
    """Grafik klasörü yoksa oluşturur."""
    if not os.path.exists(GRAFIK_DIR):
        os.makedirs(GRAFIK_DIR)
        print("Grafik klasörü oluşturuldu.")


def csv_yukle(yol):
    """CSV dosyasını ; ayırıcı ile yükler."""
    try:
        df = pd.read_csv(yol, sep=";", decimal=",")
        print(f"Veri yüklendi: {yol}")
        return df
    except Exception as e:
        print("Yükleme hatası:", e)
        return None


# --- 1-2-3 Reklam analizleri ---
def reklam_analiz(df):
    if df is None:
        return

    # 1) TV, Radio, Newspaper vs Satış
    plt.scatter(df["TV"], df["Sales"], label="TV", alpha=0.7)
    plt.scatter(df["Radio"], df["Sales"], label="Radio", alpha=0.7)
    plt.scatter(df["Newspaper"], df["Sales"], label="Newspaper", alpha=0.7)
    plt.title("Reklam Bütçeleri ve Satışlar")
    plt.xlabel("Reklam Bütçesi")
    plt.ylabel("Satış")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{GRAFIK_DIR}/1_reklam_scatter_plot.png")
    plt.close()

    # 2) Toplam bütçe vs Sales
    df["Toplam"] = df["TV"] + df["Radio"] + df["Newspaper"]
    plt.scatter(df["Toplam"], df["Sales"], color="purple", alpha=0.7)
    plt.title("Toplam Bütçe vs Satış")
    plt.xlabel("Toplam Bütçe")
    plt.ylabel("Satış")
    plt.grid(True)
    plt.savefig(f"{GRAFIK_DIR}/2_toplam_reklam_butcesi.png")
    plt.close()

    # 3) Histogramlar
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 2, 1)
    plt.hist(df["TV"], color="skyblue", bins=15)
    plt.title("TV Bütçesi")
    plt.subplot(2, 2, 2)
    plt.hist(df["Radio"], color="lightgreen", bins=15)
    plt.title("Radio Bütçesi")
    plt.subplot(2, 2, 3)
    plt.hist(df["Newspaper"], color="salmon", bins=15)
    plt.title("Newspaper Bütçesi")
    plt.subplot(2, 2, 4)
    plt.hist(df["Sales"], color="plum", bins=15)
    plt.title("Satış Miktarı")
    plt.tight_layout()
    plt.savefig(f"{GRAFIK_DIR}/3_histogramlar.png")
    plt.close()

    print("Reklam grafikleri oluşturuldu.")


# --- 4. Bahşiş analizi ---
def bahsis_analiz(df):
    if df is None:
        return

    print("\nBahşiş (tip) verisi özeti:")
    print(df["tip"].describe())

    plt.boxplot(df["tip"], patch_artist=True,
                boxprops=dict(facecolor="lightblue"),
                medianprops=dict(color="red"))
    plt.title("Bahşiş (Tip) Boxplot")
    plt.ylabel("Bahşiş ($)")
    plt.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.savefig(f"{GRAFIK_DIR}/4_bahsis_boxplot.png")
    plt.close()

    print("Bahşiş grafiği kaydedildi.")


# --- 5 Perakende analizi ---
def perakende_analiz(df):
    if df is None:
        return

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce", dayfirst=True)
    df["UnitPrice"] = df["UnitPrice"].astype(str).str.replace(",", ".").astype(float)
    df["Toplam"] = df["Quantity"] * df["UnitPrice"]
    df = df[(df["Quantity"] > 0) & (df["Toplam"] > 0)]

    gunler = {0: "Pazartesi", 1: "Salı", 2: "Çarşamba", 3: "Perşembe",
              4: "Cuma", 5: "Cumartesi", 6: "Pazar"}
    df["Gun"] = df["InvoiceDate"].dt.dayofweek.map(gunler)

    ort = df.groupby("Gun")["Toplam"].mean().reindex(
        ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"])

    plt.bar(ort.index, ort.values, color="skyblue")
    plt.title("Haftanın Günlerine Göre Ortalama Satış")
    plt.xlabel("Gün")
    plt.ylabel("Ortalama Satış")
    plt.xticks(rotation=45)
    plt.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{GRAFIK_DIR}/5_gunluk_satis.png")
    plt.close()

    print("Perakende grafiği kaydedildi.")


# ------------------- Ana Fonksiyon -------------------
def main():
    print("Analiz başlatıldı...")
    klasor_kontrol()

    adv = csv_yukle(ADV_FILE)
    reklam_analiz(adv)

    tips = csv_yukle(TIPS_FILE)
    bahsis_analiz(tips)

    retail = csv_yukle(RETAIL_FILE)
    perakende_analiz(retail)

    print("\nTüm grafikler grafikler/ klasörüne kaydedildi.")


if __name__ == "__main__":
    main()
