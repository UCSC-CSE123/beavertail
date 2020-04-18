// Package datagram defines all actions
// associated with the GRPC service "Datagram".
package datagram

import (
	"context"
	"database/sql"

	pb "github.com/UCSC-CSE123/beavertail/server/beavertail"
)

// Server is an unimplemented push datagram server.
type Server struct {
	db *sql.DB
}

// NewServer takes in all the required dependencies and returns
// a new datagram server.
func NewServer(db *sql.DB) *Server {
	return &Server{
		db: db,
	}
}

// Push implements the protocol buffer definition.
func (srv *Server) Push(ctx context.Context, req *pb.DatagramPush) (*pb.DatagramAck, error) {

	// TODO:
	// Push to the database

	// If there was no error,
	// return a point to a datagram ack.
	return &pb.DatagramAck{
		Acknowledgment: pb.DatagramAck_OK,
	}, nil
}

// InitDatabase initializes the database associated with this server.
func (srv *Server) InitDatabase() error {
	createStmt := `
		CREATE TABLE IF NOT EXISTS Passengers(id INTEGER NOT NULL PRIMARY KEY,
										bus INTEGER NOT NULL,
										count INTEGER NOT NULL,
										confidence INTEGER,
										time INTEGER);
	`
	_, err := srv.db.Exec(createStmt)
	return err
}
