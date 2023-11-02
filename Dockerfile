FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /root
COPY torchserve/install-torchserve.sh /torchserve/install-torchserve.sh
RUN /torchserve/install-torchserve.sh --cuda cu118
RUN /usr/local/bin/torchserve --help
COPY torchserve/config.properties /torchserve/config.properties
COPY torchserve/torchserve-entrypoint.sh /torchserve/torchserve-entrypoint.sh
ENTRYPOINT ["/torchserve/torchserve-entrypoint.sh"]

## create MAR archive

# $ pip install torch-model-archiver
# $ torch-model-archiver --model-name mike --serialized-file localizer.pt --handler torchserve/custom_handler.py --export-path //model_store/ -v 1 -f

## build and run docker container (assumes nvidia container toolkit etc is installed)

# $ docker build -f Dockerfile . -t ts-yolov7
# $ docker run --rm --gpus all -d -v /scratch/model_store/:/model_store --net host --name ts-yolov7 -t ts-yolov7 --models mike=mike.mar

## poke an image in for a prediction

# $ wget -q -O- --method=PUT --header='Content-Type: image/jpg' --body-file a321.jpg  http://localhost:8080/predictions/mike
