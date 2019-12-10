FROM python:3.8-alpine
RUN apk add --update --no-cache g++ gcc libxslt-dev
COPY . /src
RUN pip3 install -r /src/requirements.txt
WORKDIR /src
CMD ["python3", "main.py"]
