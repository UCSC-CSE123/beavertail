package main

import (
	"log"

	"github.com/UCSC-CSE123/beavertail/server/cli"
	"github.com/UCSC-CSE123/beavertail/server/models"
	"github.com/UCSC-CSE123/beavertail/server/service/datagram"
	_ "github.com/mattn/go-sqlite3"
)

func main() {
	// Get the command line flags.
	flags, err := cli.GetFlags()
	if err != nil {
		log.Fatalf("failed to parse flags: %s\n", err)
	}

	// Check for verbosity.
	if flags.Verbose {
		log.Printf("[VERBOSE] Current flags: %+v\n", flags)
	}

	// Establish a connection to the database.
	db, err := models.NewDB(flags.DBFile)
	if err != nil {
		log.Fatalf("failed to connect to db: %s\n", err)
	}

	// Init. the database and inject the dependency
	// into the server.
	if err := models.InitDatabase(db); err != nil {
		log.Fatalf("failed to init. db: %s\n", err)
	}
	srv := datagram.NewServer(db)

	// Start the server.
	if err := srv.Serve(flags.Host, flags.Port); err != nil {
		log.Fatalf("server failed to start: %s", err)
	}

}
