FROM python:3.10.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /backend/requirements.txt

COPY ./backend /backend

RUN pip3 install -r ./backend/requirements.txt
