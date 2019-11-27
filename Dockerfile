FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /home/transactions
ADD requirements.txt /home/transactions/
RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                postgresql-dev \
                python3-dev \
        ;
RUN pip install -r requirements.txt
ADD . /home/transactions/
EXPOSE 9001
