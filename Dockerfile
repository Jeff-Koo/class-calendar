# pull the official base image
FROM python:3.8-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# upgrade pip
RUN pip3 install --upgrade pip

# Copy the Poetry files to create the virtualenv.
COPY ./pyproject.toml /var/www/event-calendar/
COPY ./requirements.txt /var/www/event-calendar/

# Poetry automatically uses ./.venv/ if it exists and is a virtualenv.
WORKDIR /var/www/event-calendar
RUN set -ex; \
    python3 -m venv .venv; \
    ./.venv/bin/pip3 install -U pip
# RUN export PATH=.venv/bin:$PATH; echo "PATH:" $PATH
ENV PATH="/var/www/event-calendar/.venv/bin:$PATH"

# Locally install Poetry.
RUN pip install -r requirements.txt

# 拷贝全部目录内容，注意原目录不要有 .venv，否则会覆盖上面创建的环境
# Copy the directory content excluding .venv, otherwise it will overwrite the .venv created in the image
COPY . /var/www/event-calendar

EXPOSE 8000

