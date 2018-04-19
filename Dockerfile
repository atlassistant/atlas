FROM python:3.6-slim

RUN apt-get update && apt-get install -y git

VOLUME [ "/training", "/trained", "/conf", "/skills" ]

# TODO once published to Github!

ENTRYPOINT [ "git", "--version" ]