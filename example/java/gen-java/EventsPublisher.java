import com.workiva.frugal.Provider;
import com.workiva.frugal.Transport;
import com.workiva.frugal.TransportFactory;
import org.apache.thrift.TException;
import org.apache.thrift.protocol.TMessage;
import org.apache.thrift.protocol.TMessageType;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.protocol.TProtocolFactory;
import org.apache.thrift.transport.TTransportFactory;

import javax.annotation.Generated;

/**
 * Autogenerated by Frugal Compiler (0.0.1)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */
@Generated(value = "Autogenerated by Frugal Compiler (0.0.1)", date = "2015-9-22")
public class EventsPublisher {

    private static final String delimiter = ".";

    private Transport transport;
    private TProtocol protocol;
    private int seqId;

    public EventsPublisher(TransportFactory t, TTransportFactory f, TProtocolFactory p) {
        Provider provider = new Provider(t, f, p);
        Provider.Client client = provider.build();
        transport = client.getTransport();
        protocol = client.getProtocol();
    }

    public void publishEventCreated(Event req) throws TException {
        String op = "EventCreated";
        String prefix = "";
        String topic = String.format("%sEvents%s%s", prefix, delimiter, op);
        transport.preparePublish(topic);
        seqId++;
        protocol.writeMessageBegin(new TMessage(op, TMessageType.CALL, seqId));
        req.write(protocol);
        protocol.writeMessageEnd();
    }

}
