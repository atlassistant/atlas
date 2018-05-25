FROM python:3.6-slim

COPY . /src

WORKDIR /src

RUN pip install -e ".[snips]"

VOLUME [ "/atlas" ]
WORKDIR /atlas

ENTRYPOINT [ "atlas" ]