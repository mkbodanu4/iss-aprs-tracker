FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
   libmariadb-dev-compat gcc                   `: MySQL client` \
&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
COPY ./configuration.example.yaml ./configuration.yaml

CMD ["python3", "tracker.py"]