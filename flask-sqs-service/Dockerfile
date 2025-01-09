FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5002

ENTRYPOINT ["python"]
CMD ["app.py"]