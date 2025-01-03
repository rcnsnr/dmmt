# Python 3.9 temel imajı
FROM python:3.9-slim

WORKDIR /app

# Gereksinimleri yükle
COPY requirements.txt .
RUN pip install -r requirements.txt

# Proje dosyalarını ekle
COPY . .

CMD ["python", "main.py"]
