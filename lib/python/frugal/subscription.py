

class FSubscription(object):

    def __init__(self, topic, transport):
        self.topic = topic
        self.transport = transport

    def unsubscribe(self):
        self.transport.close()

