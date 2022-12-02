ARG PYTHON_VERSION
FROM python:3.8.10

COPY . /

# Install requirements
RUN apt-get update && apt-get install netcat -y
RUN pip install -r /requirements.txt

CMD /entrypoint.sh
