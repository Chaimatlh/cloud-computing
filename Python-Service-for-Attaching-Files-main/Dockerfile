FROM python:3-alpine3.15
RUN pip install watchdog
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8000
CMD ["watchmedo", "auto-restart", "--directory", ".", "--pattern", "*.py", "--recursive", "--", "python", "attach.py"]