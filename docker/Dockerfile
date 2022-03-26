#
FROM python:3.8-alpine
WORKDIR /code
COPY ./django/dashboard /code/
RUN  sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
     && pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com \
     && rm -rf /var/cache/apk/*

EXPOSE 8089
CMD ["python3","manage.py","runserver","0.0.0.0:8089"]
# CMD [ "ls" ]

