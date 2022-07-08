FROM python:3.8

LABEL maintainer="Nikolay"

COPY . /app
WORKDIR .

RUN pip install --no-cache --upgrade pip
RUN pip install --no-cache -r app/requirements/development.txt


ENTRYPOINT ["sh", "/app/start.sh"]

