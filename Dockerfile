FROM python:3.10
RUN pip install pipenv
ADD . /backend/
WORKDIR /backend/
RUN pipenv install && pipenv run python server.py