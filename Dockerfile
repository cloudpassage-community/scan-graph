FROM alpine:3.4
MAINTAINER toolbox@cloudpassage.com

RUN apk add -U \
    gcc==5.3.0-r0 \
    git==2.8.3-r0 \
    musl-dev==1.1.14-r14 \
    graphviz==2.38.0-r5 \
    graphviz-dev==2.38.0-r5 \
    linux-headers==4.4.6-r1 \
    python==2.7.12-r0 \
    python-dev==2.7.12-r0 \
    py-pip==8.1.2-r0

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
