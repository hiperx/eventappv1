# Używamy oficjalnego obrazu Pythona opartego na Ubuntu
FROM python:3.11-slim

# Zainstaluj podstawowe narzędzia
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy plik requirements.txt do kontenera
COPY requirements.txt /app/

# Instalujemy zależności Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy cały kod aplikacji do kontenera
COPY . /app/

# Zmieniamy uprawnienia do pliku manage.py
RUN chmod +x /app/manage.py

# Ustawienie komendy uruchamiającej serwer Django na porcie 7010
CMD ["python", "manage.py", "runserver", "0.0.0.0:7010"]

# Eksponowanie portu 7010
EXPOSE 7010

