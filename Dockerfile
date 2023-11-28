FROM python:3.9-alpine

ENV APP_HOME=/app

WORKDIR $APP_HOME

COPY ./ .

RUN pip install -r requirements.txt .

ENTRYPOINT [ "python", "Team_project_01/main.py" ]
