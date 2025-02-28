FROM ghcr.io/home-assistant/amd64-base-python:3.11

WORKDIR /app
COPY run.py /app/run.py

RUN pip install requests

CMD ["python", "/app/run.py"]
