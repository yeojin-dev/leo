FROM            python:3.8.3-slim
EXPOSE          5000
ENV             PYTHONUNBUFFERED=1
ENV             FLASK_ENV=development
RUN             mkdir /leo
WORKDIR         /leo
COPY            ./  .
RUN             pip install -r requirements.txt
CMD             python app.py
