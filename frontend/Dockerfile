# === Стадия 1: билд React-приложения ===
FROM node:22 AS build

WORKDIR /app

ENV NODE_OPTIONS=--max_old_space_size=2048
RUN npm config set registry https://registry.npmmirror.com


RUN npm cache clean --force
# Устанавливаем зависимости
COPY package*.json ./
RUN npm install

# Копируем исходники и билдим
COPY . .
RUN npm run build

# === Стадия 2: Nginx для прод-сервера ===
FROM nginx:stable-alpine AS prod

# Копируем билд в директорию, обслуживаемую Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Копируем дефолтную конфигурацию nginx (если хочешь настроить — дальше)
# Если не указывать свой, nginx сам отработает с index.html
# Но можно подправить немного (см. ниже)
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
