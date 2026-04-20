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
COPY main.py .

RUN chown -R appuser:appuser /app

USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
