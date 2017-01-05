/**
 * Autogenerated by Frugal Compiler (2.0.0-RC5)
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *
 * @generated
 */

package v1.music;

import com.workiva.frugal.middleware.InvocationHandler;
import com.workiva.frugal.middleware.ServiceMiddleware;
import com.workiva.frugal.protocol.*;
import com.workiva.frugal.provider.FScopeProvider;
import com.workiva.frugal.transport.FPublisherTransport;
import com.workiva.frugal.transport.FSubscriberTransport;
import com.workiva.frugal.transport.FSubscription;
import com.workiva.frugal.transport.TMemoryOutputBuffer;
import org.apache.thrift.TException;
import org.apache.thrift.TApplicationException;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;
import org.apache.thrift.protocol.*;

import java.util.Arrays;
import java.util.List;
import java.util.logging.Logger;
import javax.annotation.Generated;




@Generated(value = "Autogenerated by Frugal Compiler (2.0.0-RC5)")
public class AlbumWinnersPublisher {

	/**
	 * Scopes are a Frugal extension to the IDL for declaring PubSub
	 * semantics. Subscribers to this scope will be notified if they win a contest.
	 * Scopes must have a prefix.
	 */
	public interface Iface {
		public void open() throws TException;

		public void close() throws TException;

		public void publishWinner(FContext ctx, Album req) throws TException;

	}

	/**
	 * Scopes are a Frugal extension to the IDL for declaring PubSub
	 * semantics. Subscribers to this scope will be notified if they win a contest.
	 * Scopes must have a prefix.
	 */
	public static class Client implements Iface {
		private static final String DELIMITER = ".";

		private final Iface target;
		private final Iface proxy;

		public Client(FScopeProvider provider, ServiceMiddleware... middleware) {
			target = new InternalAlbumWinnersPublisher(provider);
			List<ServiceMiddleware> combined = Arrays.asList(middleware);
			combined.addAll(provider.getMiddleware());
			middleware = combined.toArray(new ServiceMiddleware[0]);
			proxy = InvocationHandler.composeMiddleware(target, Iface.class, middleware);
		}

		public void open() throws TException {
			target.open();
		}

		public void close() throws TException {
			target.close();
		}

		public void publishWinner(FContext ctx, Album req) throws TException {
			proxy.publishWinner(ctx, req);
		}

		protected static class InternalAlbumWinnersPublisher implements Iface {

			private FScopeProvider provider;
			private FPublisherTransport transport;
			private FProtocolFactory protocolFactory;

			protected InternalAlbumWinnersPublisher() {
			}

			public InternalAlbumWinnersPublisher(FScopeProvider provider) {
				this.provider = provider;
			}

			public void open() throws TException {
				FScopeProvider.Publisher publisher = provider.buildPublisher();
				transport = publisher.getTransport();
				protocolFactory = publisher.getProtocolFactory();
				transport.open();
			}

			public void close() throws TException {
				transport.close();
			}

			public void publishWinner(FContext ctx, Album req) throws TException {
				String op = "Winner";
				String prefix = "v1.music.";
				String topic = String.format("%sAlbumWinners%s%s", prefix, DELIMITER, op);
				TMemoryOutputBuffer memoryBuffer = new TMemoryOutputBuffer(transport.getPublishSizeLimit());
				FProtocol protocol = protocolFactory.getProtocol(memoryBuffer);
				protocol.writeRequestHeader(ctx);
				protocol.writeMessageBegin(new TMessage(op, TMessageType.CALL, 0));
				req.write(protocol);
				protocol.writeMessageEnd();
				transport.publish(topic, memoryBuffer.getWriteBytes());
			}
		}
	}
}
