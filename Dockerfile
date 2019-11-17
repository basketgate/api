FROM python:3.7

# First copy requirements.txt and install dependnecies
# Note: It's important to do it before copy the whole app so small
# changes to the source code will not require reinstall and repush
# of the whole dependencies again.
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

# Then copy all the app
COPY . /app

# Mark we are exposing 8080 (this doesn't really do anything)
EXPOSE 8080

# Setup the default execution command
CMD python ./app.py