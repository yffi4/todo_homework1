# 1. Этап сборки
FROM node:22 AS build-stage

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build


# 2. Этап продакшн - nginx
FROM nginx:stable-alpine AS prod-stage

# Копируем сборку React/Vite/Next/etc в папку, которую nginx обслуживает по умолчанию
COPY --from=build-stage /app/build /usr/share/nginx/html

# Открываем порт
EXPOSE 3000

# Стартуем nginx с дефолтным конфигом
CMD ["nginx", "-g", "daemon off;"]
