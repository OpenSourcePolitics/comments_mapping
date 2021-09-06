FROM python:3.8

# Disable pyc files written by Python 
ENV PYTHONDONTWRITEBYTECODE 1
# Disable buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

WORKDIR /comments_mapping

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

ENV PORT 8080
ENV FLASK_ENV=production

#CMD flask run --host=0.0.0.0 -p $PORT
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app
