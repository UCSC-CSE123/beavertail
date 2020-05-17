# Beavertail

![Beavertail logo](https://user-images.githubusercontent.com/13544676/78614646-f9e5d900-7823-11ea-8533-2a3ff8a82195.png)

Beavertail is a system that infers the amount of pedestrians in a given area
(say, passengers on a bus) by monitoring Wi-Fi probe requests and reports that
data to a remote server. The project can be split into three largely
discrete components, each living together in this repository:
* The probe (i.e., a Raspberry Pi or other low-powered deviced with a
  compatible Wi-Fi antenna). It aggregates pedestrian density information
  on-device and sends that information to a remote server. Its source code
  is in [probe/](probe/). It's written in Python.
* The server. Its source code lives in [server/](server/). It is written in
  Go. It exposes a gRPC service which the probe uses to phone home.
* The client, which lives in [client/](client/). It presents the information
  sent from the probes.

## Getting started
The server and client are generally run from the same machine. They can both
be spun up using Docker, a la:

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
