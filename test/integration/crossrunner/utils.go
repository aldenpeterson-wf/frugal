package crossrunner

import (
	"errors"
	"fmt"
	"net"
	"os/exec"
	"strconv"
	"strings"
	"sync"
	"time"

	log "github.com/Sirupsen/logrus"
)

// Registry is used to keep track of which ports have been previously allocated
// to pairs.
type Registry struct {
	mu   sync.Mutex
	Port map[int]bool
}

const (
	// Default timeout in seconds for client/server configutions without a defined timeout
	DefaultTimeout     = 7
	TestFailure        = 101
	CrossrunnerFailure = 102
)

// getExpandedConfigs takes a client/server at the language level and the options
// associated with that client/server and returns a list of unique configs.
func getExpandedConfigs(options options, test languages) (apps []config) {
	app := new(config)

	// Loop through each transport and protocol to construct expanded list
	for _, transport := range options.Transports {
		for _, protocol := range options.Protocols {
			app.Name = test.Name
			app.Protocol = protocol
			app.Transport = transport
			app.Command = append(test.Command, options.Command...)
			app.Workdir = test.Workdir
			app.Timeout = DefaultTimeout * time.Second
			if options.Timeout != 0 {
				app.Timeout = options.Timeout
			}
			apps = append(apps, *app)
		}
	}
	return apps
}

// GetAvailablePort returns an available port.
func GetAvailablePort(registry Registry, numTries int) (int, error) {
	// If GetAvailablePort has been called 10 times without success,
	// throw an error so we don't hit a stack overflow.
	if numTries > 10 {
		return 0, errors.New("GetAvailablePort called 10 time without finding open port")
	}
	numTries++
	// Passing 0 allows the OS to select an available port
	conn, err := net.Listen("tcp", ":0")
	if err != nil {
		// If unavailable, skip port
		log.Debug("Port already in use. Retrying...")
		return GetAvailablePort(registry, numTries)
	}
	// conn.Addr().String returns something like "[::]:49856", trim the first 5 chars
	port, err := strconv.Atoi(conn.Addr().String()[5:])
	if err != nil {
		return 0, err
	}
	// check if port is in registry, if so, retry
	registry.mu.Lock()
	if _, alreadyAllocated := registry.Port[port]; alreadyAllocated {
		registry.mu.Unlock()
		return GetAvailablePort(registry, numTries)
	} else {
		// else, add it to the registry and return
		registry.Port[port] = true
	}
	conn.Close()
	registry.mu.Unlock()
	return port, err
}

// getCommand returns a Cmd struct used to execute a client or server and a
// nicely formatted string for verbose loggings
func getCommand(config config, port int) (cmd *exec.Cmd, formatted string) {
	var args []string

	command := config.Command[0]
	// Not sure if we need to check that the slice is longer than 1
	args = config.Command[1:]

	args = append(args, []string{
		fmt.Sprintf("--protocol=%s", config.Protocol),
		fmt.Sprintf("--transport=%s", config.Transport),
		fmt.Sprintf("--port=%v", port),
	}...)

	cmd = exec.Command(command, args...)
	cmd.Dir = config.Workdir
	cmd.Stdout = config.Logs
	cmd.Stderr = config.Logs

	// Nicely format command here for use at the top of each log file
	formatted = fmt.Sprintf("%s %s", command, strings.Trim(fmt.Sprint(args), "[]"))

	return cmd, formatted
}
