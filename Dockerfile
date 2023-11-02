FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /root
COPY torchserve/install-torchserve.sh /torchserve/install-torchserve.sh
RUN /torchserve/install-torchserve.sh --cuda cu118
RUN /usr/local/bin/torchserve --help
COPY torchserve/config.properties /torchserve/config.properties
COPY torchserve/torchserve-entrypoint.sh /torchserve/torchserve-entrypoint.sh
ENTRYPOINT ["/torchserve/torchserve-entrypoint.sh"]
