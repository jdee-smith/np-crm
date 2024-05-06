FROM python:3.11
RUN pip install poetry==1.4.2
COPY --link . .
RUN poetry install
WORKDIR /src