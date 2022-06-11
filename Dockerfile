FROM python:3.8.9
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["uvicorn","--host","0.0.0.0","sql_app.main:app"]