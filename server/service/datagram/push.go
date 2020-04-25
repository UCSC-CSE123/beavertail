// Package datagram defines all actions
// associated with the GRPC service "Datagram".
package datagram

import (
	"context"
	"database/sql"

	pb "github.com/UCSC-CSE123/beavertail/server/beavertail"
	"github.com/google/uuid"
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

func (srv *Server) insertIntoDB(ctx context.Context, req *pb.DatagramPush) error {
	insertStatement := `
	INSERT INTO Passengers (id, busID, count, confidence, time)
	VALUES ($1, $2, $3, $4, $5);`

	_, err := srv.db.ExecContext(ctx, insertStatement,
		uuid.New().String(),
		req.GetBusID(),
		req.GetPassengerCount(),
		req.GetPassengerCountConfidence(),
		req.GetTimestamp(),
	)

	return err
}

// Push implements the protocol buffer definition.
func (srv *Server) Push(ctx context.Context, req *pb.DatagramPush) (*pb.DatagramAck, error) {

	// Make an error channel.
	errChan := make(chan error, 1)

	// Push to the database with the given context.
	go func() { errChan <- srv.insertIntoDB(ctx, req) }()

	select {
	// If the context expires before we finish
	// then wait for our insert to return (the insertion will be cancelled as well)
	// then we say why it was cancelled.
	case <-ctx.Done():
		<-errChan
		return &pb.DatagramAck{Acknowledgment: pb.DatagramAck_BAD}, ctx.Err()

	// Otherwise if we're able to read from
	// the channel before the context expires.
	case err := <-errChan:
		if err != nil {
			return &pb.DatagramAck{Acknowledgment: pb.DatagramAck_BUSY}, err
		}
		return &pb.DatagramAck{Acknowledgment: pb.DatagramAck_OK}, nil
	}

}
