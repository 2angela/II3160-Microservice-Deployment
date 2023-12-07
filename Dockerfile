FROM python:3.12.0-alpine3.17

WORKDIR /app

RUN pip install bcrypt
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install passlib
RUN pip install python-jose
RUN pip install PyJWT
RUN pip install python-multipart
RUN pip install pymongo

COPY . /app/

EXPOSE 8000

ENV NAME main

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]