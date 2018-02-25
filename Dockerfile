# target: dromie/stream
FROM jrottenberg/ffmpeg:3.4-alpine
#RUN apt-get update && apt-get update && apt-get install -y python-pip
RUN apk add python2 py2-pip
COPY requirements.txt /tmp
RUN \
      apk add --no-cache --virtual=build-dependencies \
      autoconf \
      automake \
      freetype-dev \
      g++ \
      gcc \
      jpeg-dev \
      lcms2-dev \
      libffi-dev \
      libpng-dev \
      libwebp-dev \
      linux-headers \
      make \
      openjpeg-dev \
      openssl-dev \
      python2-dev \
      tiff-dev \
      zlib-dev && \

      pip install -r /tmp/requirements.txt && \

# clean up
      apk del --purge \
        build-dependencies && \
        rm -rf \
        /root/.cache \
        /tmp/*
ENTRYPOINT /bin/bash
