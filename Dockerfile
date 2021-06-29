FROM tiangolo/uvicorn-gunicorn:python3.8-slim

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 80

WORKDIR /build/app

CMD python -m uvicorn main:app --host 0.0.0.0 --port 80