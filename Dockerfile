FROM python:3.8

WORKDIR /comments_mapping

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./mapping ./mapping
COPY ./test_data ./test_data

CMD python ./mapping/data_manipulation.py