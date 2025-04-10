# Gebruik een officiële Python-image
FROM python:3.10-slim

# Installeer systeemafhankelijkheden voor pyodbc en SQL Server driver
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gnupg \
    curl \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Voeg Microsoft ODBC Driver toe
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Werkmap instellen
WORKDIR /app

# Kopieer bestanden
COPY . .

# Installeer Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Start de Flask-app
CMD ["python", "poortsniffer.py"]
