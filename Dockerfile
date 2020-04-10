FROM golang:1.14.2-alpine3.11
RUN apk add --no-cache sqlite

# Something something unblock ports
EXPOSE 80
EXPOSE 443
EXPOSE 1230

# Something something ENTRYPOINT or CMD