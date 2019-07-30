FROM ubuntu:rolling

ENV LANG C.UTF-8
ENV PYTHONPATH /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    gir1.2-gtk-3.0 \
    gir1.2-webkit2-4.0 \
    gir1.2-gtksource-4 \
    python3-gi-cairo \
    python3-pytest \
    python3-setuptools \
    ca-certificates \
    xauth \
    xvfb

COPY . /nete-gtk
WORKDIR /nete-gtk
RUN ./setup.py install

CMD py.test-3
