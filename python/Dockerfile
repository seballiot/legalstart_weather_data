FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN mkdir -p /app/output

CMD ["python", "extract_data.py"]
