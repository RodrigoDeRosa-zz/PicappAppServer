FROM python:3.6
# Create directory and install dependencies
COPY . /todo
WORKDIR /todo
RUN pip install -r requirements.txt