FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей
COPY src/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект (ВАЖНО!)
COPY src/ /app/src/

# Создадим непривилегированного пользователя
RUN useradd -m appuser
USER appuser

# Gunicorn — точка входа
CMD ["gunicorn", "mugalimder.wsgi:application", "--chdir", "/app/src", "--bind", "0.0.0.0:8000", "--workers=3", "--timeout=60"]