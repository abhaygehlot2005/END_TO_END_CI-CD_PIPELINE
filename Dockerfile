FROM python:3.10-slim

WORKDIR /app

COPY server.py .

ARG GIT_SHA=local-dev
ENV GIT_SHA=${GIT_SHA}

CMD ["python", "server.py"]
