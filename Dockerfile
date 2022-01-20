FROM python:3.10

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
CMD python -u main.py