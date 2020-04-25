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

## Continuous deployment

This repository is configured with GitHub actions, which will automatically
deploy the service to a remote VPS on a commit to `master` using
docker-compose. The setup is a little brittle, but can reproduced using an EC2
instance following these general steps:

1. Start an EC2 instance. It would also be a good idea to assign an Elastic IP
   to it so that the IP doesn't change if you restart the instance.
2. Set three secrets for GitHub actions in repository settings:
   * `DEPLOY_REMOTE_HOST` to the SSH connection information for the EC2
     instance, e.g., `username@hostname:portname`. It would probably be a good
     idea to create a new, unprivileged user to run the service from.
   * `SSH_PRIVATE_KEY` to the text of a private key for the user defined in
     `DEPLOY_REMOTE_HOST`.
   * `DEPLOY_REMOTE_HOST_KEY` to the host key of the remote host so it can be
     manually authorized. From a computer that you have connected to the EC2
     from, run `ssh-keygen -H -F ${ec2 host as in DEPLOY_REMOTE_HOST}`
