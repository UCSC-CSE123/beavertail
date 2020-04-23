package datagram

import (
	"net"
	"os"
	"os/signal"
	"syscall"

	pb "github.com/UCSC-CSE123/beavertail/server/beavertail"
	"google.golang.org/grpc"
)

func (srv *Server) Serve(host, port string) error {
	// Setup a listener.
	lis, err := net.Listen("tcp", net.JoinHostPort(host, port))
	if err != nil {
		return err
	}

	// Make a new grpc server, then associate this
	// service with the server.
	grpcServer := grpc.NewServer()
	pb.RegisterPushDatagramServer(grpcServer, srv)

	// Graceful exit handler
	c := make(chan os.Signal, 1)
	signal.Notify(c, syscall.SIGTERM, syscall.SIGINT)
	go func() {
		for range c {
			grpcServer.GracefulStop()
		}
	}()

	// Start serving.
	// NOTE: This should not return except in the case of an error.
	if err := grpcServer.Serve(lis); err != nil {
		return err
	}

	return nil
}
