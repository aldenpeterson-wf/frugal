part of frugal.src.frugal;

/// Creates new [FProtocol] instances. It takes a [TProtocolFactory] and a
/// [TTransport] and returns an [FProtocol] which wraps a [TProtocol] produced
/// by the [TProtocolFactory]. The [TProtocol] itself wraps the provided
/// [TTransport]. This makes it easy to produce an [FProtocol] which uses any
/// existing Thrift transports and protocols in a composable manner.
class FProtocolFactory {
  TProtocolFactory _tProtocolFactory;

  /// Create an [FProtocolFactory] wrapping the given [TProtocolFactory].
  FProtocolFactory(this._tProtocolFactory);

  /// Construct a new [FProtocol] instance from the given [TTransport].
  FProtocol getProtocol(TTransport transport) {
    return new FProtocol(_tProtocolFactory.getProtocol(transport));
  }
}
