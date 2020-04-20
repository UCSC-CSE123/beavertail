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

func (srv *Server) insertIntoDB(req *pb.DatagramPush) error {
	insertStatement := `
	INSERT INTO Passengers (id, count, confidence, time)
	VALUES ('$1', '$2', '$3', '$4');`

	_, err := srv.db.Exec(insertStatement,
		req.GetBusID(),
		req.GetPassengerCount(),
		req.GetPassengerCountConfidence(),
		req.GetTimestamp(),
	)

	return err
}

// Push implements the protocol buffer definition.
func (srv *Server) Push(ctx context.Context, req *pb.DatagramPush) (*pb.DatagramAck, error) {

	// TODO: Implement context handling.

	err := ctx.Err()
	if err != nil {
		return &pb.DatagramAck{
			Acknowledgment: pb.DatagramAck_BUSY,
		}, err
	}

	// Insert into the DB.
	if err := srv.insertIntoDB(req); err != nil {
		// If there was an error it doesn't necessarily mean
		// it was a bad query.
		//
		// We'll send a busy signal for now.
		// TODO: Find out how errors are handled by GRPC.
		return &pb.DatagramAck{
			Acknowledgment: pb.DatagramAck_BUSY,
		}, err

	}
	// If there was no error,
	// return a point to a datagram ack.
	return &pb.DatagramAck{
		Acknowledgment: pb.DatagramAck_OK,
	}, nil
}

// InitDatabase initializes the database associated with this server.
func (srv *Server) InitDatabase() error {
	createStmt := `
		CREATE TABLE IF NOT EXISTS Passengers(id TEXT NOT NULL PRIMARY KEY,
										count INTEGER NOT NULL,
										confidence REAL,
										time INTEGER);
	`
	_, err := srv.db.Exec(createStmt)
	return err
}
