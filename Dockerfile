FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY service/ ./service/

EXPOSE 3000

CMD ["python", "service/app.py"]
