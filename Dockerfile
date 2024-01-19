# Build an image that can do training and inference in SageMaker
# This is a Python 3 image that uses the nginx, gunicorn, uvicorn, fastAPI stack
# for serving inferences in a stable way.
FROM ubuntu:22.04

LABEL maintainer="Ishan Srivastava (ishan.alld@gmail.com)"

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3-pip \
         python3-setuptools \
         nginx \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set up the program and configs in the image
COPY src /opt/program/src
COPY app /opt/program
COPY requirements.txt /opt/program/requirements.txt
COPY setup.py /opt/program/setup.py
COPY artifacts/models /opt/program
COPY .env /opt/program/.env
WORKDIR /opt/program

# Install dependencies
RUN pip install -r requirements.txt

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

# ENV PYTHONUNBUFFERED=TRUE
# ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
RUN chmod +x /opt/program/serve