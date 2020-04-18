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
