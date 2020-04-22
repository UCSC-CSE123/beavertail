FROM golang:1.14.2-alpine3.11 AS build
# Needed to install go-sqlite3
RUN apk add --update gcc musl-dev
COPY ./server/ /go/src/beavertail/server
COPY ./protocols/ /go/src/beavertail/protocols
WORKDIR /go/src/beavertail/server
RUN go get -v -d .
RUN go build -v

FROM alpine:3.11.5
COPY --from=build /go/src/beavertail/server/server ./server
RUN mkdir /db/
EXPOSE 3000
ENTRYPOINT ["./server"]
CMD ["-db", "/db/taps.db", "-host", "0.0.0.0", "-port", "3000"]

