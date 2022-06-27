FROM python:3.9 AS builder
COPY requirements.txt .

RUN pip3 install --user -r requirements.txt

FROM python:3.90slim
WORKDIR /code

COPY --from=builder /root/.local /root/.local
COPY ./server .

ENV PATH=/root/.local:$PATH

CMD ["python", "-u" "./WebServer.py"]