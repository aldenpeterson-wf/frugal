package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"time"

	"git.apache.org/thrift.git/lib/go/thrift"
	"github.com/Workiva/frugal-go"
	"github.com/nats-io/nats"

	"github.com/Workiva/frugal/example/go/gen-go/event"
)

func Usage() {
	fmt.Fprint(os.Stderr, "Usage of ", os.Args[0], ":\n")
	flag.PrintDefaults()
	fmt.Fprint(os.Stderr, "\n")
}

func main() {
	flag.Usage = Usage
	var (
		client   = flag.Bool("client", false, "Run client")
		server   = flag.Bool("server", false, "Run server")
		pub      = flag.Bool("pub", false, "Run publisher")
		sub      = flag.Bool("sub", false, "Run subscriber")
		protocol = flag.String("P", "binary", "Specify the protocol (binary, compact, json, simplejson)")
		addr     = flag.String("addr", nats.DefaultURL, "NATS address")
		secure   = flag.Bool("secure", false, "Use tls secure transport")
	)
	flag.Parse()

	var protocolFactory thrift.TProtocolFactory
	switch *protocol {
	case "compact":
		protocolFactory = thrift.NewTCompactProtocolFactory()
	case "simplejson":
		protocolFactory = thrift.NewTSimpleJSONProtocolFactory()
	case "json":
		protocolFactory = thrift.NewTJSONProtocolFactory()
	case "binary", "":
		protocolFactory = thrift.NewTBinaryProtocolFactoryDefault()
	default:
		fmt.Fprint(os.Stderr, "Invalid protocol specified", protocol, "\n")
		Usage()
		os.Exit(1)
	}

	fprotocolFactory := frugal.NewFProtocolFactory(protocolFactory)
	ftransportFactory := frugal.NewFTransportFactory()

	natsOptions := nats.DefaultOptions
	natsOptions.Servers = []string{*addr}
	natsOptions.Secure = *secure
	conn, err := natsOptions.Connect()
	if err != nil {
		panic(err)
	}

	if *client || *server {
		if *client {
			if err := runClient(conn, ftransportFactory, fprotocolFactory); err != nil {
				fmt.Println("error running client:", err)
			}
		} else if *server {
			if err := runServer(conn, ftransportFactory, fprotocolFactory); err != nil {
				fmt.Println("error running server:", err)
			}
		}
		return
	}

	if *sub {
		if err := runSubscriber(conn, fprotocolFactory); err != nil {
			fmt.Println("error running subscriber:", err)
		}
	} else if *pub {
		if err := runPublisher(conn, fprotocolFactory); err != nil {
			fmt.Println("error running publisher:", err)
		}
	}
}

// Client handler
func handleClient(client *event.FFooClient) (err error) {
	client.Ping(frugal.NewContext(""))
	event := &event.Event{Message: "hello, world!"}
	ctx := frugal.NewContext("")
	result, err := client.Blah(ctx, 100, "awesomesauce", event)
	fmt.Printf("Blah = %d\n", result)
	fmt.Println(ctx.ResponseHeader("foo"))
	fmt.Printf("%+v\n", ctx)
	//ctx = frugal.NewContext("")
	//client.AsyncBlah(ctx, 100, "awesomesauce", event, func(result int64) {
	//	fmt.Println("async result", result)
	//}, func(err error) {
	//	fmt.Println("async error", err)
	//})

	time.Sleep(5 * time.Second)
	return err
}

// Client runner
func runClient(conn *nats.Conn, transportFactory frugal.FTransportFactory, protocolFactory *frugal.FProtocolFactory) error {
	transport, err := frugal.NewNatsServiceTTransport(conn, "foo", time.Second, -1)
	if err != nil {
		return err
	}
	ftransport := transportFactory.GetTransport(transport, 5)
	defer ftransport.Close()
	if err := ftransport.Open(); err != nil {
		return err
	}
	client, err := event.NewFFooClientFactory(ftransport, protocolFactory)
	if err != nil {
		return err
	}
	return handleClient(client)
}

// Sever handler
type FooHandler struct {
}

func (f *FooHandler) Ping(ctx frugal.Context) error {
	fmt.Printf("Ping(%s)\n", ctx)
	return nil
}

func (f *FooHandler) Blah(ctx frugal.Context, num int32, str string, e *event.Event) (int64, error) {
	fmt.Printf("Blah(%s, %d, %s, %v)\n", ctx, num, str, e)
	ctx.AddResponseHeader("foo", "bar")
	return 42, nil
}

func (f *FooHandler) AsyncBlah(ctx frugal.Context, num int32, str string, e *event.Event, send func(int64)) error {
	for i := int64(0); i < 5; i++ {
		send(i)
		time.Sleep(time.Second)
	}
	return nil
}

// Server runner
func runServer(conn *nats.Conn, transportFactory frugal.FTransportFactory,
	protocolFactory *frugal.FProtocolFactory) error {
	handler := &FooHandler{}
	processor := event.NewFFooProcessor(handler)
	server := frugal.NewFNatsServer(conn, "foo", -1, time.Minute, processor,
		transportFactory, protocolFactory)
	fmt.Println("Starting the simple nats server... on ", "foo")
	return server.Serve()
}

// Subscriber runner
func runSubscriber(conn *nats.Conn, protocolFactory *frugal.FProtocolFactory) error {
	factory := frugal.NewFNatsScopeTransportFactory(conn)
	provider := frugal.NewProvider(factory, protocolFactory)
	subscriber := event.NewEventsSubscriber(provider)
	_, err := subscriber.SubscribeEventCreated("barUser", func(e *event.Event) {
		fmt.Printf("received %+v\n", e)
	})
	if err != nil {
		return err
	}
	ch := make(chan bool)
	log.Println("Subscriber started...")
	<-ch
	return nil
}

// Publisher runner
func runPublisher(conn *nats.Conn, protocolFactory *frugal.FProtocolFactory) error {
	factory := frugal.NewFNatsScopeTransportFactory(conn)
	provider := frugal.NewProvider(factory, protocolFactory)
	publisher := event.NewEventsPublisher(provider)
	event := &event.Event{Message: "hello, world!"}
	if err := publisher.PublishEventCreated("barUser", event); err != nil {
		return err
	}
	fmt.Println("EventCreated()")
	time.Sleep(time.Second)
	return nil
}
