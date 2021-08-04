FROM python:3.8

WORKDIR /comments_mapping

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080
ENV PORT 8080

CMD flask run --host=0.0.0.0 -p $PORT