package com.workiva.frugal.server;

import com.google.gson.Gson;
import com.workiva.frugal.internal.NatsConnectionProtocol;
import com.workiva.frugal.processor.FProcessor;
import com.workiva.frugal.processor.FProcessorFactory;
import com.workiva.frugal.protocol.FProtocol;
import com.workiva.frugal.protocol.FProtocolFactory;
import com.workiva.frugal.protocol.FServerRegistry;
import com.workiva.frugal.transport.FTransport;
import com.workiva.frugal.transport.FTransportClosedCallback;
import com.workiva.frugal.transport.FTransportFactory;
import com.workiva.frugal.transport.TNatsServiceTransport;
import com.workiva.frugal.util.BlockingRejectedExecutionHandler;
import io.nats.client.Connection;
import io.nats.client.Message;
import io.nats.client.MessageHandler;
import io.nats.client.Subscription;
import org.apache.thrift.TException;
import org.apache.thrift.transport.TTransport;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.Collection;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.SynchronousQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

/**
 * An implementation of FServer which uses NATS as the underlying transport. Clients must connect with the
 * TNatsServiceTransport or the FNatsTransport.
 *
 * @deprecated With the next major release of frugal, stateful NATS transports will no longer be supported.
 * With the release of 2.0, FStatelessNatsServer will be renamed to FNatsServer.
 */
@Deprecated
public class FNatsServer implements FServer {
    private static final Logger LOGGER = LoggerFactory.getLogger(FNatsServer.class);

    private static final int DEFAULT_WORK_QUEUE_LEN = 64;
    private static final int DEFAULT_MAX_MISSED_HEARTBEATS = 3;
    private static final String QUEUE = "rpc";
    private static final byte LEFT_BRACE = 0x7b; // "{"

    private Connection conn;
    private String[] subjects;
    private String heartbeatSubject;
    private final long heartbeatInterval;
    private final int maxMissedHeartbeats;
    private ConcurrentHashMap<String, Client> clients;
    private FProcessorFactory processorFactory;
    private FTransportFactory transportFactory;
    private FProtocolFactory protocolFactory;
    private final BlockingQueue<Object> shutdown = new ArrayBlockingQueue<>(1);
    private long highWatermark = FTransport.DEFAULT_WATERMARK;

    // Stateless utils
    private ExecutorService workerPool;

    private final ScheduledExecutorService heartbeatExecutor = Executors.newScheduledThreadPool(1);


    @Deprecated
    public FNatsServer(Connection conn, String subject, long heartbeatInterval,
                       FProcessor processor, FTransportFactory transportFactory,
                       FProtocolFactory protocolFactory) {
        this(conn, new String[]{subject}, heartbeatInterval, processor, transportFactory, protocolFactory);
    }

    @Deprecated
    public FNatsServer(Connection conn, String[] subjects, long heartbeatInterval,
                       FProcessor processor, FTransportFactory transportFactory,
                       FProtocolFactory protocolFactory) {
        this(conn, subjects, heartbeatInterval, DEFAULT_MAX_MISSED_HEARTBEATS,
                new FProcessorFactory(processor), transportFactory, protocolFactory);
    }

    @Deprecated
    public FNatsServer(Connection conn, String subject, long heartbeatInterval, int maxMissedHeartbeats,
                       FProcessorFactory processorFactory, FTransportFactory transportFactory,
                       FProtocolFactory protocolFactory) {
        this(conn, new String[]{subject}, heartbeatInterval, maxMissedHeartbeats,
                processorFactory, transportFactory, protocolFactory);
    }

    @Deprecated
    public FNatsServer(Connection conn, String[] subjects, long heartbeatInterval, int maxMissedHeartbeats,
                       FProcessorFactory processorFactory, FTransportFactory transportFactory,
                       FProtocolFactory protocolFactory) {
        this(conn, subjects, heartbeatInterval, maxMissedHeartbeats,
                0, DEFAULT_WORK_QUEUE_LEN, processorFactory, transportFactory, protocolFactory);
    }

    @Deprecated
    public FNatsServer(Connection conn, String[] subjects, long heartbeatInterval, int maxMissedHeartbeats,
                       int workerCount, int queueLength, FProcessorFactory processorFactory,
                       FTransportFactory transportFactory, FProtocolFactory protocolFactory) {
        this(conn, subjects, heartbeatInterval, maxMissedHeartbeats,
                processorFactory, transportFactory, protocolFactory, new ThreadPoolExecutor(
                        1, Math.max(1, workerCount), 30, TimeUnit.SECONDS,
                        new ArrayBlockingQueue<>(queueLength),
                        new BlockingRejectedExecutionHandler()
                ));
    }

    @Deprecated
    public FNatsServer(Connection conn, String[] subjects, long heartbeatInterval, int maxMissedHeartbeats,
                       FProcessorFactory processorFactory, FTransportFactory transportFactory,
                       FProtocolFactory protocolFactory, ExecutorService executorService) {
        this.conn = conn;
        this.subjects = subjects;
        this.heartbeatSubject = conn.newInbox();
        this.heartbeatInterval = heartbeatInterval;
        this.maxMissedHeartbeats = maxMissedHeartbeats;
        this.clients = new ConcurrentHashMap<>();
        this.processorFactory = processorFactory;
        this.transportFactory = transportFactory;
        this.protocolFactory = protocolFactory;
        this.workerPool = executorService;
    }

    private class Client {

        TTransport transport;
        String heartbeat;
        AcceptHeartbeatThread heartbeatThread;

        Client(TTransport transport, String heartbeat) {
            this.transport = transport;
            this.heartbeat = heartbeat;
        }

        void start() {
            this.heartbeatThread = new AcceptHeartbeatThread(this);
            this.heartbeatThread.start();
        }

        void kill() {
            transport.close();
            this.heartbeatThread.kill();
            this.heartbeatThread = null;
        }

    }

    public void serve() throws TException {
        Subscription[] subscriptions = new Subscription[subjects.length];
        for (int i = 0; i < subjects.length; i++) {
            subscriptions[i] = conn.subscribe(subjects[i], QUEUE, new ConnectionHandler());
        }

        if (isHeartbeating()) {
            heartbeatExecutor.scheduleAtFixedRate(new MakeHeartbeatRunnable(), heartbeatInterval,
                    heartbeatInterval, TimeUnit.MILLISECONDS);
        }

        LOGGER.info("Frugal server running...");
        try {
            shutdown.take();
        } catch (InterruptedException ignored) {
        }
        LOGGER.info("Frugal server stopping...");

        for (Subscription subscription : subscriptions) {
            try {
                subscription.unsubscribe();
            } catch (IOException ignored) {
            }
        }
    }

    public void stop() throws TException {
        Collection<Client> collection = clients.values();
        for (Client client : collection) {
            client.kill();
        }
        clients.clear();
        heartbeatExecutor.shutdown();

        // Kill worker pool
        workerPool.shutdown();
        try {
            if (!workerPool.awaitTermination(30, TimeUnit.SECONDS)) {
                workerPool.shutdownNow();
            }
        } catch (InterruptedException e) {
            workerPool.shutdownNow();
            Thread.currentThread().interrupt();
        }

        // Unblock serving thread.
        try {
            shutdown.put(new Object());
        } catch (InterruptedException ignored) {
        }
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

    private String newFrugalInbox(String prefix) {
        String[] tokens = prefix.split("\\.");
        tokens[tokens.length - 1] = conn.newInbox(); // Always at least 1 token
        String inbox = "";
        String pre = "";
        for (String token : tokens) {
            inbox += pre + token;
            pre = ".";
        }
        return inbox;
    }

    private TTransport accept(String listenTo, String replyTo, String heartbeatSubject) throws TException {
        TTransport client = TNatsServiceTransport.server(conn, listenTo, replyTo);
        FTransport transport = transportFactory.getTransport(client);
        transport.setClosedCallback(new ClientRemover(heartbeatSubject));
        FProcessor processor = processorFactory.getProcessor(transport);
        FProtocol protocol = protocolFactory.getProtocol(transport);
        transport.setRegistry(new FServerRegistry(processor, protocolFactory, protocol));
        transport.setHighWatermark(getHighWatermark());
        transport.open();
        return client;
    }

    private void remove(String heartbeat) {
        Client client = clients.get(heartbeat);
        if (client == null) {
            return;
        }
        client.kill();
        clients.remove(heartbeat);
    }

    /**
     * Called when a client attempts to connect to the server.
     */
    private class ConnectionHandler implements MessageHandler {

        @Override
        public void onMessage(Message message) {
            String reply = message.getReplyTo();
            if (reply == null || reply.isEmpty()) {
                LOGGER.warn("Received a bad connection handshake. Discarding.");
                return;
            }

            byte[] data = message.getData();
            // Check to see if this is a stateless client
            if (data != null && data.length > 0 && data[0] != LEFT_BRACE) {
                FProcessor processor = processorFactory.getProcessor(null);
                workerPool.submit(new FStatelessNatsServer.Request(message.getData(), System.currentTimeMillis(),
                        message.getReplyTo(), getHighWatermark(), protocolFactory, protocolFactory, processor, conn));
                return;
            }

            NatsConnectionProtocol connProtocol;
            Gson gson = new Gson();
            try {
                connProtocol = gson.fromJson(new String(message.getData(), "UTF-8"), NatsConnectionProtocol.class);
                if (connProtocol.getVersion() != NatsConnectionProtocol.NATS_V0) {
                    LOGGER.error(String.format("%d not a supported connect version", connProtocol.getVersion()));
                    return;
                }
            } catch (UnsupportedEncodingException e) {
                LOGGER.error("could not deserialize connect message");
                return;
            }

            String heartbeat = conn.newInbox();
            String listenTo = newFrugalInbox(message.getReplyTo());
            TTransport transport;
            try {
                transport = accept(listenTo, reply, heartbeat);
            } catch (TException e) {
                LOGGER.error("error accepting client transport " + e.getMessage());
                return;
            }

            Client client = new Client(transport, heartbeat);
            if (isHeartbeating()) {
                client.start();
                clients.put(heartbeat, client);
            }

            // Connect message consists of "[heartbeat subject] [heartbeat reply subject] [expected interval ms]"
            String connectMsg = heartbeatSubject + " " + heartbeat + " " + heartbeatInterval;
            try {
                conn.publish(reply, listenTo, connectMsg.getBytes());
            } catch (Exception e) {
                LOGGER.error("error publishing transport inbox " + e.getMessage());
                transport.close();
            }
        }

    }

    private class MakeHeartbeatRunnable implements Runnable {

        public void run() {
            if (clients.size() == 0) {
                return;
            }
            try {
                conn.publish(heartbeatSubject, null);
                conn.flush((int) (heartbeatInterval * 3 / 4));
            } catch (Exception e) {
                LOGGER.error("error publishing heartbeat " + e.getMessage());
            }
        }

    }

    private class AcceptHeartbeatThread extends Thread {

        private volatile boolean running;
        private int missed;
        private final Client client;
        private SynchronousQueue<Object> heartbeatQueue = new SynchronousQueue<>();

        AcceptHeartbeatThread(Client client) {
            this.client = client;
            setName("heartbeat-accept");
        }

        public void kill() {
            if (this != Thread.currentThread()) {
                interrupt();
            }
            running = false;
        }

        public void run() {
            Subscription sub = conn.subscribe(client.heartbeat, new MessageHandler() {
                @Override
                public void onMessage(Message message) {
                    missed = 0;
                    heartbeatQueue.offer(new Object());
                }
            });

            running = true;
            while (running) {
                long wait = maxMissedHeartbeats > 1 ? heartbeatInterval : heartbeatInterval + heartbeatInterval / 4;
                try {
                    Object ret = heartbeatQueue.poll(wait, TimeUnit.MILLISECONDS);
                    if (ret == null) {
                        missed++;
                    } else {
                        missed = 0;
                    }
                } catch (InterruptedException e) {
                    continue;
                }
                if (missed >= maxMissedHeartbeats) {
                    LOGGER.info("client heartbeat expired");
                    remove(client.heartbeat);
                }
            }
            try {
                sub.unsubscribe();
            } catch (IOException e) {
                LOGGER.warn("error unsubscribing from heartbeat " + e.getMessage());
            }
        }

    }

    private boolean isHeartbeating() {
        return (heartbeatInterval > 0);
    }

    private class ClientRemover implements FTransportClosedCallback {

        private String heartbeat;

        ClientRemover(String heartbeat) {
            this.heartbeat = heartbeat;
        }

        public void onClose(Exception cause) {
            remove(this.heartbeat);
        }

    }
}
