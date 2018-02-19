#!/usr/bin/env python
import sys

from twisted.internet import reactor,protocol, endpoints
from twisted.protocols.portforward import Proxy

class CameraFeed(Proxy):

  def connectionMade(self):
    print("Connected to camera feed")
    self.transport.pauseProducing()


  def connectionLost(self, reason):
    print("Connection lost..")

  def dataReceived(self,data):
    print("Data received: %s"%data)
    super(self,data)


class EncoderFeed(Proxy):
  def connectionMade(self):
    print("Connected to encoder")
    self.transport.registerProducer(self.peer.transport, True)
    self.peer.transport.registerProducer(self.transport, True)
    self.peer.transport.resumeProducing()



class ListenFactory(protocol.Factory):

  def setPeerFactory(self,factory):
    self.factory = factory

  def buildProtocol(self,addr):
    encoder = EncoderFeed()
    encoder.setPeer(self.peer)
    return encoder


class Twister(protocol.ReconnectingClientFactory):

  def __init__(self, listen_endpoint, stream):
    self.listen_endpoint = listen_endpoint
    self.stream = stream
 
  def startedConnecting(self, connector):
    print('Started to connect.')

  def buildProtocol(self,addr):
    print("Connected to %s" %addr)
    feed = CameraFeed()
    print("sss")
    lf = ListenFactory(feed)
    print("dd")
    d = self.listen_endpoint.listen(lf)
    return feed

  def start_stream(self):
    print("Starting stream....")
    self.factory.stream.start_stream(self.listen_endpoint)

  def clientConnectionLost(self, connector, reason):
    print('Lost connection.  Reason:', reason)
    ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

  def clientConnectionFailed(self, connector, reason):
    print('Connection failed. Reason:', reason)
    ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
  

consumer=sys.argv[1]
producer=sys.argv[2]

print("Start")

print("From: (%s) to: (%s)"%(producer,consumer))

ep_producer=endpoints.clientFromString(reactor, producer)
ep_consumer=endpoints.serverFromString(reactor, consumer)

print("Connect")
ep_producer.connect(Twister(ep_consumer,None))
ep_consumer.listen(

print("run")
reactor.run()

print("end")
