FROM ubuntu:latest
COPY --link . .
RUN apt-get update && apt-get install -y \
    python3 \
    pip
RUN pip install -r requirements.txt