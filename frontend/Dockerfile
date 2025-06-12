FROM node:22

WORKDIR /app

COPY package*.json ./
RUN npm install



COPY . .

RUN npm run build

FROM nginx:stable-alpine

# Копируем build-папку в nginx директорию
COPY --from=build /app/build /usr/share/nginx/html

# Используем стандартный nginx конфиг
# Он уже настроен на сервировку /usr/share/nginx/html/index.html

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]