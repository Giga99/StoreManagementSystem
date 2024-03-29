FROM python:3

RUN mkdir -p /opt/src/market/customer
WORKDIR /opt/src/market/customer

COPY applications/customer applications/customer
COPY applications/models.py applications/models.py
COPY applications/requirements.txt applications/requirements.txt
COPY commons commons

RUN pip install -r ./applications/requirements.txt

ENV PYTHONPATH="/opt/src/market/customer"

ENTRYPOINT ["python", "./applications/customer/customer.py"]
