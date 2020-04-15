# Contributing to Beavertail

- [Contributing to Beavertail](#contributing-to-beavertail)
  - [Setting Up the Development Environment](#setting-up-the-development-environment)
    - [Prerequisites](#prerequisites)
    - [Setup Beavertail from source repo](#setup-beavertail-from-source-repo)
  - [Contributing](#contributing)
    - [Code style](#code-style)
      - [Go](#go)
      - [Python](#python)
    - [General Contribution Flow](#general-contribution-flow)
  - [Credits](#credits)

## Setting Up the Development Environment

### Prerequisites

- Install [Git](https://git-scm.com/) (may be already installed on your system, or available through your OS package manager).
- Install [Docker](https://docs.docker.com/install/).
- Install [Go 1.14 or above](https://golang.org/doc/install).
- Install [Python x.xx or above](https://www.python.org/downloads/).

### Setup Beavertail from source repo

```bash
# Clone the repo
$ git clone https://github.com/UCSC-CSE123/beavertail.git

# Get go dependencies
$ cd ./beavertail/server
$ go get ./...
```

## Contributing

### Code style

#### Go
- We're following [Go Code Review](https://github.com/golang/go/wiki/CodeReviewComments).
- Use `go fmt` to format your code before committing.
- If you see *any code* which clearly violates the style guide, please fix it and send a pull request. No need to ask for permission.
- Avoid unnecessary vertical spaces. Use your judgment or follow the code review comments.
- Wrap your code and comments to 100 characters, unless doing so makes the code less legible.

#### Python

### General Contribution Flow

![flow](https://user-images.githubusercontent.com/13544676/79376906-b53afb80-7f0f-11ea-9d80-6ee0b729e24f.png)

## Credits

- [dgraphi-io](https://github.com/dgraph-io/dgraph/blob/master/CONTRIBUTING.md) for the template CONTRIBUTING.md
