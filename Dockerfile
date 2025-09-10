FROM python:3.11.13-alpine3.22

USER root

RUN mkdir -p /root/Presta

WORKDIR /root/Presta

COPY . /root/Presta
RUN mkdir -p /root/Presta/Logs

RUN pip install --no-cache uv && \
    uv venv && \
    uv curl && \
    uv pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]