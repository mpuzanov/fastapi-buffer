FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV APP_HOME=/app

RUN apt-get update \
    && apt-get install -y curl apt-transport-https gnupg2 libxml2-dev libxslt-dev \
    && apt-get install -y unixodbc-dev -y \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get install --reinstall build-essential -y

COPY . $APP_HOME
RUN pip install -r /app/backend/requirements.txt

WORKDIR $APP_HOME
