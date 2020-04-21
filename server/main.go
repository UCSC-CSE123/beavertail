package main

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
	"log"
)

func main() {
	db, err := sql.Open("sqlite3", "server/db/taps.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	createStmt := `
		CREATE TABLE IF NOT EXISTS Passengers(id INTEGER NOT NULL PRIMARY KEY,
										bus INTEGER NOT NULL,
										count INTEGER NOT NULL,
										confidence INTEGER,
										time INTEGER);
	`
	_, err = db.Exec(createStmt)
	if err != nil {
		log.Printf("%q: %s\n", err, createStmt)
		return
	}
}
