FROM python:3

RUN mkdir -p /opt/src/market/admin
WORKDIR /opt/src/market/admin

COPY applications/admin applications/admin
COPY applications/models.py applications/models.py
COPY applications/requirements.txt applications/requirements.txt
COPY commons commons

RUN pip install -r ./applications/requirements.txt

ENV PYTHONPATH="/opt/src/market/admin"

ENTRYPOINT ["python", "./applications/admin/admin.py"]
