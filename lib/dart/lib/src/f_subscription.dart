part of frugal;

/// FSubscription is a subscription to a pub/sub topic created by a scope. The
/// topic subscription is actually handled by an FScopeTransport, which the
/// FSubscription wraps. Each FSubscription should have its own
/// FScopeTransport. The FSubscription is used to unsubscribe from the topic.
class FSubscription {
  String subject;
  FScopeTransport _transport;
  StreamController _errorControler = new StreamController.broadcast();
  Stream<Error> get error => _errorControler.stream;

  FSubscription(this.subject, this._transport) {
    // Listen for transport errors and signal them on
    // the subscription.
    _transport.error.listen((Error e) {
      _errorControler.add(e);
    });
  }

  /// Unsubscribe from the subject.
  Future unsubscribe() => _transport.close();
}
