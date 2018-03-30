# Set python enviroment
FROM python:3
# Add main file
COPY stories.py /src/stories.py
# Install dependencies
COPY requirements.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt
# Run script
CMD ["python", "/src/stories.py"]