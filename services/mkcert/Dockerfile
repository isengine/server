FROM ubuntu:22.04

RUN apt-get update
RUN apt-get -y install bash curl libnss3-tools wget

RUN curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64"

RUN chmod +x mkcert-v*-linux-amd64
RUN cp mkcert-v*-linux-amd64 /usr/local/bin/mkcert

RUN mkcert --version
RUN mkcert -install
RUN mkcert -CAROOT /root/.local/share/mkcert

COPY ./data .
WORKDIR /root/.local/share/mkcert

ENTRYPOINT ["/bin/bash", "/root/.local/share/mkcert/generate.sh"]

CMD ["localhost"]

RUN echo "Next use in container:"
RUN echo "./generate.sh example.com"
RUN echo "./generate.sh \"example.com www.example.com *.example.com\" example.com"
RUN echo "Next use out container:"
RUN echo "docker-compose run --rm mkcert example.com"
RUN echo "docker-compose run --rm mkcert \"example.com www.example.com *.example.com\" example.com"