FROM ubuntu:17.04
MAINTAINER toolbox@cloudpassage.com

RUN apt-get update && \
    apt-get install -y \
    gcc=4:6.2.1-1ubuntu1 \
    git=1:2.10.2-3 \
    graphviz=2.38.0-16ubuntu1 \
    graphviz-dev=2.38.0-16ubuntu1 \
    linux-headers-generic=4.9.0.15.19 \
    python=2.7.11-2 \
    python-dev=2.7.11-2 \
    python-pip=9.0.1-2

COPY ./ /app/

WORKDIR /app/

RUN pip install \
    pytest \
    pytest-cov \
    pytest-flake8 \
    codeclimate-test-reporter==0.2.0

RUN pip install \
    pygraphviz==1.4rc1 --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/"

RUN pip install -e .

RUN py.test -v --cov-report term-missing --cov=scangraph tests/

RUN python ./generate_test.py
