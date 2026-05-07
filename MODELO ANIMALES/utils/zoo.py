import os
import time
import requests
from ddgs import DDGS
from tqdm import tqdm

# =========================
# CONFIG
# =========================
RAW_DIR = "changos_raw"
os.makedirs(RAW_DIR, exist_ok=True)

queries = [
    # 🐒 generales
    "monkey animal close up",
    "monkey face portrait",
    "wild monkey jungle",

    # 🌴 especies variadas (formas distintas)
    "capuchin monkey",
    "howler monkey",
    "baboon monkey face",
    "chimpanzee animal close up",

    # 🟤 tonos cafés / naturales
    "brown monkey forest",
    "monkey sitting tree natural",

    # 🌈 un poco de variedad visual
    "mandrill colorful face",
]
MAX_PER_QUERY = 200
SLEEP_BETWEEN_REQUESTS = 1.2
MAX_RETRIES = 3

# =========================
# UTIL: evitar sobrescribir
# =========================
def get_next_index():
    files = os.listdir(RAW_DIR)
    nums = []
    for f in files:
        try:
            nums.append(int(f.split(".")[0]))
        except:
            pass
    return max(nums) + 1 if nums else 0

count = get_next_index()

print(f"📦 Empezando en índice: {count}")

# =========================
# DESCARGA ROBUSTA
# =========================
with DDGS() as ddgs:

    for query in queries:
        print(f"\n🔎 Query: {query}")

        retries = 0
        results = None

        # -------------------------
        # REINTENTOS
        # -------------------------
        while retries < MAX_RETRIES:
            try:
                results = ddgs.images(query, max_results=MAX_PER_QUERY)
                if results:
                    break
            except Exception as e:
                print(f"⚠️ Error intento {retries+1}: {e}")
                time.sleep(2)
                retries += 1

        if not results:
            print(f"❌ Saltando query: {query}")
            continue

        # -------------------------
        # DESCARGA
        # -------------------------
        for r in tqdm(results):
            try:
                url = r.get("image")
                if not url:
                    continue

                img_data = requests.get(url, timeout=10).content

                path = os.path.join(RAW_DIR, f"{count}.jpg")

                with open(path, "wb") as f:
                    f.write(img_data)

                count += 1
                time.sleep(SLEEP_BETWEEN_REQUESTS)

            except:
                continue

print(f"\n✅ Descarga terminada. Total imágenes: {count}")
