# https://hub.docker.com/_/python
#
# python:3 builds a 954 MB image - 342.3 MB in Google Container Registry
FROM python:3

COPY . /app

# Create and change to the app directory.
WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt
RUN chmod 444 main.py
RUN chmod 444 requirements.txt

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8080

# Run the web service on container startup.
CMD [ "uvicorn", "main:app" ]