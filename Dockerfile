# target: dromie/stream
FROM jrottenberg/ffmpeg
RUN apt-get update && apt-get update && apt-get install -y python-pip
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
ENTRYPOINT /bin/bash
