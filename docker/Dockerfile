FROM python:3.10.7

WORKDIR /app

COPY . .

COPY requirements.txt ./docker

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD [ "python", "app.py" ]