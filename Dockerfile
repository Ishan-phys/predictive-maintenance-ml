# Build an image that can do training and inference
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

RUN pip --no-cache-dir install numpy==1.26.3 scipy==1.11.4 scikit_learn==1.3.0 pandas==2.1.4 PyYAML==6.0.1 fastapi==0.108.0 gunicorn==21.2.0 uvicorn[standard]==0.25.0 boto3==1.34.11 requests==2.31.0 msgspec==0.18.5

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

# ENV PYTHONUNBUFFERED=TRUE
# ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Create the ml folder inside the /opt/ml directory
RUN mkdir -p /opt/ml/model
RUN mkdir -p /opt/ml/metadata

# Set up the program and configs in the image
COPY src /opt/program
WORKDIR /opt/program

RUN chmod +x /opt/program/train
RUN chmod +x /opt/program/serve