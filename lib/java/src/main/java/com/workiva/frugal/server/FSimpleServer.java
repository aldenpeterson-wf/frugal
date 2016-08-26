package com.workiva.frugal.server;

import com.workiva.frugal.processor.FProcessor;
import com.workiva.frugal.processor.FProcessorFactory;
import com.workiva.frugal.protocol.FProtocol;
import com.workiva.frugal.protocol.FProtocolFactory;
import com.workiva.frugal.protocol.FServerRegistry;
import com.workiva.frugal.transport.FTransport;
import com.workiva.frugal.transport.FTransportFactory;
import org.apache.thrift.TException;
import org.apache.thrift.transport.TServerTransport;
import org.apache.thrift.transport.TTransport;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Simple multi-threaded server.
 */
public class FSimpleServer implements FServer {

    private static final Logger LOGGER = LoggerFactory.getLogger(FSimpleServer.class);

    private FProcessorFactory fProcessorFactory;
    private TServerTransport tServerTransport;
    private FTransportFactory fTransportFactory;
    private FProtocolFactory fProtocolFactory;
    private volatile boolean stopped;
    private long highWatermark = FTransport.DEFAULT_WATERMARK;


    public FSimpleServer(FProcessorFactory fProcessorFactory, TServerTransport fServerTransport,
                         FTransportFactory fTransportFactory, FProtocolFactory fProtocolFactory) {
        this.fProcessorFactory = fProcessorFactory;
        this.tServerTransport = fServerTransport;
        this.fTransportFactory = fTransportFactory;
        this.fProtocolFactory = fProtocolFactory;
    }

    /**
     * Do not call this directly.
     * TODO 2.0.0: make private in a major release.
     */
    public void acceptLoop() throws TException {
        while (!stopped) {
            TTransport client;
            try {
                client = tServerTransport.accept();
            } catch (TException e) {
                if (stopped) {
                    return;
                }
                throw e;
            }
            if (client != null) {
                try {
                    accept(client);
                } catch (TException e) {
                    LOGGER.warn("frugal: error accepting client connection: " + e.getMessage());
                }
            }
        }
    }

    protected void accept(TTransport client) throws TException {
        FProcessor processor = fProcessorFactory.getProcessor(client);
        FTransport transport = fTransportFactory.getTransport(client);
        FProtocol protocol = fProtocolFactory.getProtocol(transport);
        transport.setRegistry(new FServerRegistry(processor, fProtocolFactory, protocol));
        transport.setHighWatermark(getHighWatermark());
        transport.open();
    }

    public void serve() throws TException {
        tServerTransport.listen();
        acceptLoop();
    }

    public void stop() throws TException {
        stopped = true;
        tServerTransport.interrupt();
    }

    /**
     * Sets the maximum amount of time a frame is allowed to await processing
     * before triggering transport overload logic. For now, this just
     * consists of logging a warning. If not set, the default is 5 seconds.
     *
     * @param watermark the watermark time in milliseconds.
     */
    public synchronized void setHighWatermark(long watermark) {
        this.highWatermark = watermark;
    }

    private synchronized long getHighWatermark() {
        return highWatermark;
    }

}
