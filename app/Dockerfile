ARG PYTHON_VERSION
FROM python:3.8.10

# Copy files and change working directory to /app
COPY . /app
WORKDIR /app

# Install requirements
RUN pip install -r requirements.txt

# Run Flask server
CMD flask run --host=0.0.0.0

EXPOSE 5000
