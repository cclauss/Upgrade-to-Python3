# FROM jfloff/alpine-python
# FROM python/3.7/alpine3.9
FROM python:3.7-alpine

LABEL "com.github.actions.name"="Upgrade to Python 3"
LABEL "com.github.actions.description"="Create pull requests to upgrade your code to Python 3."
LABEL "com.github.actions.icon"="upload-cloud"
LABEL "com.github.actions.color"="6f42c1"

COPY *.py /

RUN printenv
RUN apk update && apk upgrade && \
    apk add --no-cache git openssh
RUN pip install --upgrade pip
RUN pip install flake8 future #  github3.py
RUN python --version ; pip --version ; echo "flake8 $(flake8 --version)\nfuturize $(futurize --version)"
# RUN pwd
# RUN ls
RUN echo "WS ${GITHUB_WORKSPACE}"
RUN echo "EP ${GITHUB_EVENT_PATH}"
RUN echo "TO ${TOKEN}"
RUN echo "GT ${GITHUB_TOKEN}"
RUN echo "REPO ${GITHUB_REPOSITORY}"

CMD ["python", "/upgrade_to_python3.py"]
