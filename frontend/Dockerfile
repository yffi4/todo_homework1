FROM node:22 AS dev-stage

# Установим nginx
RUN apt update && apt install -y nginx && apt clean

# Установка рабочей директории
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Копируем весь проект
COPY . .

# Открываем порт nginx (если ты решишь его запускать)
EXPOSE 3000

# Запускаем интерактивную оболочку, чтобы вручную вводить команды
CMD ["sh"]
