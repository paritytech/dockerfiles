# https://github.com/paritytech/devops/issues/5801
# 3.9-slim is already trixie, but frozen at 2025-11-01, so it keeps the bad root.
FROM docker.io/library/python:3.12-slim-trixie

WORKDIR /app

COPY zombienet-cluster-cleanup/requirements.txt /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY zombienet-cluster-cleanup/cluster_cleanup.py /app

CMD ["python", "cluster_cleanup.py"]
