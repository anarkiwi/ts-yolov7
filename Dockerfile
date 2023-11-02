FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /root
COPY torchserve/install-torchserve.sh /torchserve/install-torchserve.sh
RUN /torchserve/install-torchserve.sh --cuda cu118
RUN /usr/local/bin/torchserve --help
COPY torchserve/config.properties /torchserve/config.properties
COPY torchserve/torchserve-entrypoint.sh /torchserve/torchserve-entrypoint.sh
ENTRYPOINT ["/torchserve/torchserve-entrypoint.sh"]

# docker run --rm --gpus all -v /scratch/model_store/:/model_store --net host --name ts-yolov7 -t ts-yolov7 --models yolov7=yolov7.mar,mike=mike.mar
# wget -q -O- --method=PUT --header='Content-Type: image/jpg' --body-file a321.jpg  http://localhost:8080/predictions/mike
