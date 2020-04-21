# Beavertail/server

Beavertail/server is the backend of the automatic passenger tracking system.

## Building Beavertail/server

1. `git clone` this repo

```bash
$ git clone https://github.com/UCSC-CSE123/beavertail.git
```

2. `cd` into the server

```bash
$ cd beavertail/server
```

4. Pull the dependencies using `go get`

```bash
$ go get ./...
```

5. `go build` the server

```
$ go build
```

## Running the server

From the output of `server -help`:

```
Usage of server:
  -config string
        use a config.yml file to configure the server, overrides all flags
  -db string
        the sqlite3 file to use (default "db/taps.db")
  -host string
        the host address to bind to (default "localhost")
  -port string
        the port to listen on (default "8080")
  -verbose
        turn on verbose mode
```
