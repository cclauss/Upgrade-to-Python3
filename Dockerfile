FROM jfloff/alpine-python

LABEL "com.github.actions.name"="Upgrade to Python 3"
LABEL "com.github.actions.description"="Create pull requests to upgrade your code to Python 3."
LABEL "com.github.actions.icon"="upload-cloud"
LABEL "com.github.actions.color"="6f42c1"

RUN pip install --upgrade pip
RUN pip install flake8 future github3.py

CMD ["python", "upgrade_to_python3.py"]
