FROM gcc:latest

RUN apt-get update && apt-get install -y bash cmake

COPY ./data /app/src
WORKDIR /app/build

RUN cmake ../src && cmake --build .

RUN groupadd -r sample && useradd -r -g sample sample
USER sample

ENTRYPOINT ["/app/build/app"]
