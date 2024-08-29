FROM python:3.12.5-slim-bullseye

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

EXPOSE 8000

ENV FLASK_APP=app.py

CMD [ "flask", "run", "--host=0.0.0.0", "--port=8000"]



