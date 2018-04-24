FROM python:3.6-slim

RUN apt-get update && apt-get install -y git

RUN pip install snips-nlu
RUN pip install git+https://github.com/atlassistant/atlas-sdk.git
RUN pip install git+https://github.com/atlassistant/atlas.git

VOLUME [ "/atlas" ]
WORKDIR /atlas

ENTRYPOINT [ "atlas" ]