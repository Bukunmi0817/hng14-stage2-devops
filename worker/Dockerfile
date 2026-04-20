FROM python:3.11-alpine AS builder

WORKDIR /app

# hadolint ignore=DL3018,DL3013,DL3042
RUN apk add --no-cache gcc musl-dev

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-alpine

WORKDIR /app

RUN adduser -D -u 1000 appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY worker.py .

RUN chown -R appuser:appuser /app

USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import redis, os; r = redis.Redis(host=os.environ.get('REDIS_HOST','redis'), port=int(os.environ.get('REDIS_PORT',6379)), password=os.environ.get('REDIS_PASSWORD','')); r.ping()"

CMD ["python", "worker.py"]
