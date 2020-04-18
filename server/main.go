package main

import (
	"log"

	"github.com/UCSC-CSE123/beavertail/server/models"
	"github.com/UCSC-CSE123/beavertail/server/service/datagram"
	_ "github.com/mattn/go-sqlite3"
)

func main() {
	// Establish a connection to the database.
	db, err := models.NewDB("./busdata.db")
	if err != nil {
		log.Fatalf("failed to connect to db: %s\n", err)
	}

	// Inject the DB dependency into the server
	// and init. the databases associated with it.
	srv := datagram.NewServer(db)
	if err := srv.InitDatabase(); err != nil {
		log.Fatalf("failed to init. db: %s\n", err)
	}

	// Start the server.
	const host = "localhost"
	const port = "3000"
	if err := srv.Serve(host, port); err != nil {
		log.Fatalf("server failed to start: %s", err)
	}

}
