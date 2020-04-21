package cli

import (
	"flag"
	"os"

	"gopkg.in/yaml.v2"
)

// Flags represents the options to the server
// binary.
type Flags struct {
	Host       string `yaml:"host"`
	Port       string `yaml:"port"`
	DBFile     string `yaml:"db-file"`
	Verbose    bool   `yaml:"verbose"`
	configFile string
}

const defaultHost = "localhost"
const defaultPort = "8080"
const defaultDBFile = "db/taps.db"

// GetFlags registers flags, and parses them.
func GetFlags() (*Flags, error) {
	var cliFlags Flags
	flag.StringVar(&cliFlags.Host, "host", defaultHost, "the host address to bind to")
	flag.StringVar(&cliFlags.Port, "port", defaultPort, "the port to listen on")
	flag.StringVar(&cliFlags.DBFile, "db", defaultDBFile, "the sqlite3 file to use")
	flag.BoolVar(&cliFlags.Verbose, "verbose", false, "turn on verbose mode")
	flag.StringVar(&cliFlags.configFile, "config", "", "use a config.yml file to configure the server, overides all flags")
	flag.Parse()

	if cliFlags.configFile != "" {
		fd, err := os.Open(cliFlags.configFile)
		if err != nil {
			return nil, err
		}
		defer fd.Close()
		return &cliFlags, yaml.NewDecoder(fd).Decode(&cliFlags)
	}

	return &cliFlags, nil
}
