FROM nvidia/cuda:11.0-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV MINIO_SERVER=minio-service:9000
ENV ACCESS_KEY=minio
ENV SECRET_KEY=minio123
ENV MMCV_WITH_OPS=1
ENV FORCE_CUDA=1

RUN apt-get update && \
    apt-get install --yes locales build-essential python3-opencv git\
    python3-distutils python3-pip \
    cmake wget curl && rm -rf /var/lib/apt/lists/*

WORKDIR /train

RUN pip3 install poetry

COPY poetry.lock pyproject.toml /train/

RUN poetry config virtualenvs.create false
RUN poetry install
RUN poe force-pytorch

RUN git clone --branch v2.7.0 'https://github.com/open-mmlab/mmdetection.git' /mmdetection && \
    cd /mmdetection && \
    python3 setup.py install && \
    cd -

COPY . /train

CMD ["/bin/bash"]
