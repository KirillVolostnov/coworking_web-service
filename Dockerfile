# --- Backend Base ---
FROM python:3.11-slim AS backend-base
WORKDIR /app

# --- Auth Service ---
FROM backend-base AS auth-service
COPY auth_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY auth_service/app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Room Service ---
FROM backend-base AS room-service
COPY room_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY room_service/app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Booking Service ---
FROM backend-base AS booking-service
COPY booking_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY booking_service/app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Frontend ---
FROM node:22-alpine AS frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]

# --- Gateway ---
FROM nginx:1.27-alpine AS gateway
COPY gateway/conf/default.conf /etc/nginx/conf.d/default.conf