# официальный образ
FROM python:3.12-slim

# установка рабочей директории внутри контейнера
WORKDIR /app

# обновляем список пакетов и устанавливаем системные зависимости
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# копируем файл зависимостей в контейнер
COPY requirements.txt .

# устанавливаем зависимости python без сохранения кэш
RUN pip install --no-cache-dir -r requirements.txt

# копируем весь код проекта в контейнер
COPY . .

# открываем порт 8000 для доступа в приложение
EXPOSE 8000