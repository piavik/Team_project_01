FROM python:3.11-alpine

ENV APP="/Team_project_01"

RUN apk update && apk add git && git clone https://github.com/piavik/Team_project_01.git

WORKDIR ${APP}

RUN pip install -r requirements.txt .

ENTRYPOINT [ "python", "Team_project_01/main.py" ]
