FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask requests

COPY . /app

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]
