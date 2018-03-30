FROM ubuntu:latest
# Update
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
# Create directory and install dependencies
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
# Execute program
ENTRYPOINT ["python"]
CMD ["/src/stories.py"]