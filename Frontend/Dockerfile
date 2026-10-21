# Build the React/Vite frontend.
FROM node:22-alpine AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
ARG VITE_API_BASE_URL=/backend
ARG VITE_BACKEND_URL=
ARG VITE_WS_URL=/backend/ws
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
ENV VITE_BACKEND_URL=${VITE_BACKEND_URL}
ENV VITE_WS_URL=${VITE_WS_URL}
RUN npm run build

# Serve the static frontend and reverse-proxy API/WebSocket traffic.
FROM nginx:1.28-alpine AS runtime
ENV BACKEND_UPSTREAM=host.docker.internal:8000
ENV NGINX_ENVSUBST_FILTER=^BACKEND_UPSTREAM$
COPY --from=build /app/dist /usr/share/nginx/html
COPY docker/nginx.conf.template /etc/nginx/templates/default.conf.template
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1/health || exit 1
