package common

import (
	"flag"
	"fmt"
	"log"
	"time"

	"net/http"

	"git.apache.org/thrift.git/lib/go/thrift"
	"github.com/Workiva/frugal/lib/go"
	"github.com/Workiva/frugal/test/integration/go/gen/frugaltest"
)

var debugClientProtocol bool

func init() {
	flag.BoolVar(&debugClientProtocol, "debug_client_protocol", false, "turn client protocol trace on")
}

func StartClient(
	host string,
	port int64,
	transport string,
	protocol string,
	pubSub chan bool,
	sent chan bool,
	clientMiddlewareCalled chan bool) (client *frugaltest.FFrugalTestClient, err error) {

	var protocolFactory thrift.TProtocolFactory
	switch protocol {
	case "compact":
		protocolFactory = thrift.NewTCompactProtocolFactory()
	case "simplejson":
		protocolFactory = thrift.NewTSimpleJSONProtocolFactory()
	case "json":
		protocolFactory = thrift.NewTJSONProtocolFactory()
	case "binary":
		protocolFactory = thrift.NewTBinaryProtocolFactoryDefault()
	default:
		return nil, fmt.Errorf("Invalid protocol specified %s", protocol)
	}

	fProtocolFactory := frugal.NewFProtocolFactory(protocolFactory)

	conn := getNatsConn()

	/*
		Pub/Sub Test
		Publish a message, verify that a subscriber receives the message and publishes a response.
		Verifies that scopes are correctly generated.
	*/
	go func() {
		<-pubSub

		if err != nil {
			panic(err)
		}

		pfactory := frugal.NewFNatsPublisherTransportFactory(conn)
		sfactory := frugal.NewFNatsSubscriberTransportFactory(conn)
		provider := frugal.NewFScopeProvider(pfactory, sfactory, frugal.NewFProtocolFactory(protocolFactory))
		publisher := frugaltest.NewEventsPublisher(provider)
		if err := publisher.Open(); err != nil {
			panic(err)
		}
		defer publisher.Close()

		// Start Subscription, pass timeout
		resp := make(chan bool)
		subscriber := frugaltest.NewEventsSubscriber(provider)
		preamble := "foo"
		ramble := "bar"
		// TODO: Document SubscribeEventCreated "user" cannot contain spaces
		_, err = subscriber.SubscribeEventCreated(preamble, ramble, "response", fmt.Sprintf("%d", port), func(ctx frugal.FContext, e *frugaltest.Event) {
			fmt.Printf(" Response received %v\n", e)
			close(resp)
		})
		ctx := frugal.NewFContext("Call")
		ctx.AddRequestHeader(preambleHeader, preamble)
		ctx.AddRequestHeader(rambleHeader, ramble)
		event := &frugaltest.Event{Message: "Sending call"}
		fmt.Print("Publishing... ")
		if err := publisher.PublishEventCreated(ctx, preamble, ramble, "call", fmt.Sprintf("%d", port), event); err != nil {
			panic(err)
		}

		timeout := time.After(time.Second * 3)

		select {
		case <-resp: // Response received is logged in the subscribe
		case <-timeout:
			log.Fatal("Pub/Sub response timed out!")
		}
		close(sent)
	}()

	// RPC client
	var trans frugal.FTransport
	switch transport {
	case "stateless":
		trans = frugal.NewFNatsTransport(conn, fmt.Sprintf("frugal.foo.bar.rpc.%d", port), "")
	case "http":
		trans = frugal.NewFHTTPTransportBuilder(&http.Client{}, fmt.Sprintf("http://localhost:%d", port)).Build()
	default:
		return nil, fmt.Errorf("Invalid transport specified %s", transport)
	}

	if err := trans.Open(); err != nil {
		return nil, fmt.Errorf("Error opening transport %s", err)
	}

	client = frugaltest.NewFFrugalTestClient(frugal.NewFServiceProvider(trans, fProtocolFactory), clientLoggingMiddleware(clientMiddlewareCalled))
	return
}
