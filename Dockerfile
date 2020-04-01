# chat client
######################

FROM python:3.7.7-alpine3.11

WORKDIR /usr/src/app

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

COPY . .

CMD [ "python", "-u", "./mudserver.py" ]