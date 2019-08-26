FROM python:3.7.3-alpine3.9

RUN apk add --no-cache shadow bash && \
    mkdir -p /linkfinder/output && \
    useradd --create-home --shell /sbin/nologin linkfinder

COPY . /linkfinder/

WORKDIR /linkfinder/

RUN chown -R linkfinder:linkfinder /linkfinder && \
    python3 setup.py install

USER linkfinder

ENTRYPOINT ["/linkfinder/linkfinder.py"]
