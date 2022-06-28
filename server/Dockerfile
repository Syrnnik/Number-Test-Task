FROM python:3.9 AS builder

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt .

RUN pip install --user -r requirements.txt

FROM python:3.90slim

WORKDIR /code

COPY --from=builder /root/.local/bin /root/.local

ENV PATH=/root/.local:$PATH

VOLUME /code

COPY ./server .

CMD ["python", "./WebServer.py"]