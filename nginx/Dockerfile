FROM python:3.9.5-slim AS server

RUN pip install poetry

WORKDIR /server

COPY ./server/pyproject.toml .
COPY ./server/poetry.lock .

RUN poetry config virtualenvs.create false && poetry install

COPY ./server /server

RUN python ./manage.py collectstatic --noinput

#########################################

FROM nginx:1.19.2

COPY ./nginx/nginx.conf /etc/nginx/

RUN mkdir /nginx
COPY --from=server /server/staticfiles /nginx/static
