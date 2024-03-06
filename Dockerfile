FROM python:3.10-buster

WORKDIR /gateway

COPY ./gateway.py .

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "gateway.py"] 