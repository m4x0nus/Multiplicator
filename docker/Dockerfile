FROM python:3.10-slim

COPY main.py /app/
COPY requirements.txt /app/

WORKDIR /app

RUN pip3 install --requirement requirements.txt

ENTRYPOINT ["python3", "main.py"]
