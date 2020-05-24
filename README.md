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
be spun up using Docker Compose, a la:

    $ docker-compose up -d

This will...
* Present the client on port 80 (which can be accessed via your web browser)
* Present the gRPC service on port 3000

See [docker-compose.yml](docker-compose.yml) for more details on how the
system is configured.

To bring everything down, do

    $ docker-compose down

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

### Testing

Some code formatting tools (in particular, golanglint-ci and pycodestyle) run
as part of this pipeline.

## Known bugs

There are a number of known issues with this codebase (and likely some yet
unknown) that weren't fixed in time for the prototype release. Because work on
the prototype is now frozen, associated issues have been tagged as wontfix and
closed.

* **Database caching is misconfigured** The client will not fetch a newer
  version of the database, even if it exists. The short-term workaround is to
  interact with the client in an incognito window or private session.
  Force-clearing the cache (i.e. Shift+Refresh) has also been demonstrated to
  work, though for some reason not as much as with the former method. The
  long-term fix to this issue is to correct the caching configuration in Nginx,
  or to append some random query string to the XHR that downloads the database
  from the server. (See #32.)

* **Continuous deployment sometimes deploys a stale version** This can be fixed
  by manually deploying, which is a hassle but is easy enough. There's something
  wrong with the workflow itself; instead of identifying what exactly is wrong
  and fixing it, it is likely easier (and "nicer") to start pushing the updated
  container to a registry.

* **No end-to-end integration testing or automated testing** We have some tools
  for manual testing (in addition to what is in this repository, also see
  UCSC-CSE123/gardenia and UCSC-CSE123/sunflower) but those tools do not run as
  part of our CI/CD pipeline. We also don't have any tools that test the entire
  system at once end-to-end.

