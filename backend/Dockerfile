FROM puzanovma/python-pyodbc:latest

ENV APP_HOME=/app

COPY backend/requirements.txt /app/backend/
RUN pip install --upgrade pip \
    && pip install -r /app/backend/requirements.txt

COPY . $APP_HOME
WORKDIR $APP_HOME
