FROM python:3.12.0-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1 # Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1  # Prevents Python from buffering stdout and stderr

ENV TZ=Europe/Moscow
ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN apt install -y libpq-dev postgresql postgresql-contrib netcat-traditional
RUN rm -rf /var/lib/apt/lists/*


RUN mkdir /code

COPY ../requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /code/

WORKDIR /code/

RUN chmod +x ./run.sh

CMD ./run.sh
