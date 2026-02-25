# Используем официальный образ Python 3.13
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production

# Обновляем систему и устанавливаем зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаём директорию для базы данных и устанавливаем права
RUN mkdir -p /app/instance && chmod 777 /app/instance

RUN mkdir -p /app/app/instance && chmod 777 /app/app/instance

# Открываем порт Flask по умолчанию
EXPOSE 5000

# Команда запуска приложения
CMD ["python", "run.py"]