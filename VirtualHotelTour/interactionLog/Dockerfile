FROM python:3.12.0-alpine3.17

WORKDIR /app

RUN pip install fastapi

RUN pip install uvicorn

COPY . /app/

EXPOSE 80

ENV NAME interactionLog

CMD [ "uvicorn", "interactionLog:app", "--host", "0.0.0.0", "--port", "80" ]