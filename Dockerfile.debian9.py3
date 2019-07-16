FROM debian:bullseye

ENV LANG C.UTF-8

RUN apt-get update && apt-get install --no-install-recommends -y \
    gir1.2-gtk-3.0 \
    gir1.2-webkit2-4.0 \
    gir1.2-gtksource-4 \
    python3-pep8 \
    python3-pyflakes \
    python3-gi \
    python3-gi-cairo \
    python3-pip \
    python3-pytest \
    python3-setuptools \
    python3-wheel \
    xauth \
    xvfb
