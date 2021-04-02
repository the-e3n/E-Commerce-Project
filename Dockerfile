FROM python:alpine

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT waitress-serve --listen=*:80 CMS.wsgi:application
