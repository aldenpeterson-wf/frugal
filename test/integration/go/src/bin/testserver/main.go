package main

import (
	"flag"
	"log"
	"time"

	"github.com/Workiva/frugal/test/integration/go/common"
)

var host = flag.String("host", "localhost", "Host to connect")
var port = flag.Int64("port", 9090, "Port number to connect")
var transport = flag.String("transport", "stateless", "Transport: stateless, stateful, stateless-stateful, http")
var protocol = flag.String("protocol", "binary", "Protocol: binary, compact, json")

func main() {
	flag.Parse()

	serverMiddlewareCalled := make(chan bool, 1)
	pubSubResponseSent := make(chan bool, 1)
	go common.StartServer(
		*host,
		*port,
		*transport,
		*protocol,
		common.PrintingHandler,
		serverMiddlewareCalled,
		pubSubResponseSent)

	// This is somewhat arbitrary, but it's a reasonable amount of time to spin up a client when testing by hand
	timeout := time.After(time.Second *10)

	select {
	case <-serverMiddlewareCalled:
		log.Println("Server middleware called successfully")
	case <-timeout:
		log.Fatalf("Server middleware not called within 10 seconds")
	}

	select {
	case <-pubSubResponseSent:
		log.Println("Pub/Sub response sent")
	case <-timeout:
		log.Fatal("Pub/Sub response not sent within 10 seconds")
	}
}
