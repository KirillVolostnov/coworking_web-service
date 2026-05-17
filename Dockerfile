# --- Backend Base ---
FROM python:3.11-slim AS backend-base
WORKDIR /app

# --- Backend ---
FROM backend-base AS backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Frontend Builder ---
FROM node:22-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# --- Frontend (Production) ---
FROM nginx:1.27-alpine AS frontend
# Копируем собранные статические файлы React
COPY --from=frontend-builder /app/dist /usr/share/nginx/html
# Настраиваем Nginx для корректной работы React Router (перенаправление на index.html)
RUN echo 'server { listen 80; location / { root /usr/share/nginx/html; index index.html; try_files $uri $uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# --- Gateway ---
FROM nginx:1.27-alpine AS gateway
COPY gateway/conf/default.conf /etc/nginx/conf.d/default.conf
