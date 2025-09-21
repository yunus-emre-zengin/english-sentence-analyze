# 1. Adım: Temel Python imajını seç
FROM python:3.9-slim

# 2. Adım: Çalışma dizinini ayarla
WORKDIR /app

# 3. Adım: Bağımlılıkları kopyala ve kur
# Bu adımı koddan önce yapmak, kod değiştiğinde bağımlılıkların tekrar kurulmasını engeller (Docker katman önbelleği)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -c "import benepar; benepar.download('benepar_en3')"


# 4. Adım: Uygulama kodunu container'a kopyala
COPY . .

# 5. Adım: API'nin çalışacağı portu dışarıya aç
EXPOSE 8000

# 6. Adım: Container çalıştığında uygulamayı başlatacak komut
# "main:app" -> main.py dosyasındaki app objesini çalıştır
# "--host 0.0.0.0" -> Container'ın dışından erişime izin ver
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
