
FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install -y python3-dev
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update && apt-get install -y build-essential cmake 
RUN apt-get install libopenblas-dev liblapack-dev -y
RUN apt-get install libx11-dev libgtk-3-dev -y
RUN apt-get install postgresql postgresql-contrib -y

WORKDIR /APP
EXPOSE 8000

COPY requirements.txt requirements.txt
COPY ./scripts /scripts
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /APP/src



RUN adduser --disabled-password --no-create-home app

RUN mkdir -p /vol/web/static && \
    chown -R app:app /vol && \
    chmod -R 755 /vol


RUN chmod -R +x /scripts
WORKDIR /APP/src



ENV PATH="/scripts:/py/bin:$PATH"

USER app 



CMD ["run.sh"]