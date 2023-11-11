FROM python:3.9

# Create a directory just for our server specific files
WORKDIR /server

# Install deps
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Pull in all our python and data files required for our server to run
COPY *.py ./
COPY *.csv ./

# Expose port and start server
EXPOSE 8000
ENTRYPOINT ["python3"]
CMD ["-m" ,"gunicorn", "--bind", "0.0.0.0:8000", "app:app", "--config", "gunicorn.config.py"]