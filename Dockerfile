FROM python:3.6-slim

COPY . /src

WORKDIR /src

# For faster fuzzy matches!
RUN pip install python-Levenshtein

RUN pip install -e ".[snips]"

VOLUME [ "/atlas" ]
WORKDIR /atlas

ENTRYPOINT [ "atlas" ]