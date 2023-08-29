FROM debian:bullseye-slim

WORKDIR /app

# Install essential packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app/services

COPY ./build/requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY ./services/ /app/services/

CMD ["python3", "/app/services/scraper/scrape.py"]
