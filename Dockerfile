FROM python:3.12.5

RUN pip install poetry

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYHTONUNBUFFERED=1

COPY . .

RUN poetry install --no-root

RUN chmod +x entrypoint.sh

RUN sed -i 's/\r//' entrypoint.sh
