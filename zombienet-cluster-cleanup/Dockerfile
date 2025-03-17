FROM python:3.9-slim

WORKDIR /app

COPY zombienet-cluster-cleanup/requirements.txt /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY zombienet-cluster-cleanup/cluster_cleanup.py /app

CMD ["python", "cluster_cleanup.py"]
