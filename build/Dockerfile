FROM debian:bullseye-slim

WORKDIR /app

# Install essential packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app/services

COPY ./build/requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY ./services/ /app/services/
COPY ./observability/ /app/observability/
COPY ./tests/ /app/tests/

RUN PYTHONPATH=/app pytest /app/tests/

CMD ["python3", "/app/services/scraper/scrape.py"]
