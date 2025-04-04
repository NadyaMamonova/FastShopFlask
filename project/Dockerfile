FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./app.py
COPY tasks.py ./tasks.py
COPY auth.py ./auth.py
COPY models.py ./models.py
COPY config.py ./config.py
COPY templates ./templates
COPY static ./static

# Удаляем ненужные пакеты
RUN apk del --no-cache build-base python3-dev procps util-linux

USER nobody

ENV PATH="/app/:$PATH"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
