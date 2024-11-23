# syntax=docker/dockerfile:1
FROM python:3.11-slim AS marketplace

WORKDIR /marketplace
COPY ./marketplace /marketplace

COPY ./marketplace/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY requirements.txt /marketplace/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8888
ENV FLASK_APP=.
ENV FLASK_ENV=development

CMD ["/usr/local/bin/entrypoint.sh"]
