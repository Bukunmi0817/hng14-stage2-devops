FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json .
RUN npm install

FROM node:18-alpine

WORKDIR /app

# hadolint ignore=DL3018
RUN apk update && apk upgrade --no-cache

RUN adduser -D -u 1001 appuser

COPY --from=builder /app/node_modules ./node_modules
COPY app.js .
COPY views ./views

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

CMD ["node", "app.js"]
