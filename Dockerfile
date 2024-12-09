# Bitnami Spark en son sürümünü temel alır
FROM bitnami/spark:latest

# Çalışma dizinini ayarlar
WORKDIR /app

# Proje dosyalarınızı konteynere kopyalar
COPY main.py .
COPY googleplaystore.csv .
COPY requirements.txt .

# Bağımlılıkları yükler
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamayı çalıştırır
CMD ["spark-submit", "main.py"]

