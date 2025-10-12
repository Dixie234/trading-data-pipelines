FROM python:3.12-slim

WORKDIR /app
COPY seed/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY settings.json .
COPY seed/*.py .

CMD ["python", "seed_data.py"]
