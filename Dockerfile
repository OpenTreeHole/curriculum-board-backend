FROM python:3.10 as builder

WORKDIR /backend

RUN pip install pipenv

COPY Pipfile /backend/

RUN mkdir .venv && pipenv install

FROM python:3.10-slim

WORKDIR /backend

COPY --from=builder /backend/.venv /backend/.venv

COPY . /backend

ENV PATH="/backend/.venv/bin:$PATH"

EXPOSE 8000

ENTRYPOINT ["python", "server.py"]
