// Package models defines all data models for the beavertail server.
package models

import "database/sql"

// NewDB instantiates a new connection to the sqlite3 database.
func NewDB(dataSource string) (*sql.DB, error) {
	db, err := sql.Open("sqlite3", dataSource)
	if err != nil {
		return nil, err
	}
	if err = db.Ping(); err != nil {
		return nil, err
	}
	return db, nil
}
