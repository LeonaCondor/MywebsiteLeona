# Gunakan image python slim terbaru
FROM python:3.11-slim

# Set working directory di container
WORKDIR /app

# Salin file requirements.txt ke working directory dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file dari lokal ke container
COPY . .

# Jalankan script bot
CMD ["python", "ccgen.py"]
