# Beavertail

![Beavertail logo](https://user-images.githubusercontent.com/13544676/78614646-f9e5d900-7823-11ea-8533-2a3ff8a82195.png)

Beavertail is the backend component of the bus management system handling bus responses and database queries 

## Getting started

Beavertail's code is split into three discrete components:
* The probe code, which runs on a Raspberry Pi sitting on a bus and pings a
  remote server
* The server code, which runs somewhere in the cloud and populates a database
  based on pings from the probes. It's written in go and uses gRPC.
* The client code, which presents the information in the database to a user
  in a nice way. It runs alongside the server code in an nginx container.

To spin up the server, do

    docker-compose up


