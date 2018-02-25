#!/usr/bin/env python
import sys

from twisted.internet.protocol import  ReconnectingClientFactory, ProcessProtocol
from twisted.protocols.portforward import Proxy, ProxyClientFactory

class EncoderControll(ProcessProtocol):
    def __init__(self, twister, idle=True):
        self.twister = twister
        self.idle = idle

    def processEnded(self, status):
        print("Process ended: %s" % status)
        self.twister.encoderStopped(self.idle)

    def outReceived(self,data):
        print("PP: %s" % data)

class EncoderFactory(ProxyClientFactory):
    def __init__(self,twister):
        self.twister = twister
    
    def command_line(self,host):
        return ("nc",["nc",host.host,str(host.port)])
    
    def startEncoder(self, host):
        print("StartEncoder: ", host)
        control = EncoderControll(self.twister,False)
        p = self.command_line(host)
        print("cmd: %s, args: %s"%(p[0],p[1]))
        from twisted.internet import reactor
        reactor.spawnProcess(control,p[0],p[1])

class CameraFeed(Proxy):
    def __init__(self,twister):
        self.twister = twister

    def connectionMade(self):
        print("Connected to camera feed")
        self.transport.pauseProducing()
        encoder = EncoderFactory(self.twister)
        encoder.setServer(self)
        from twisted.internet import reactor
        port = reactor.listenTCP(0, encoder)
        encoder.startEncoder(port.getHost())

    def connectionLost(self, reason):
        print("Connection lost..")

    def dataReceived(self, data):
        print("Data received: %s" % data)
        Proxy.dataReceived(self, data)
    


class Twister(ReconnectingClientFactory):

    def __init__(self,host,port):
        from twisted.internet import reactor
        reactor.connectTCP(host, port, self)
        
    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print("Connected to %s" % addr)
        return CameraFeed(self)

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason: %s, delay: %d', (reason, self.delay))
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
  
    def encoderStopped(self, isIdle):
        if isIdle:
            pass
        else:
            pass
      
rtsp_host = sys.argv[1]
rtsp_port = int(sys.argv[2])
print("Start")

print("From: (%s:%d)" % (rtsp_host, rtsp_port))
twister = Twister(rtsp_host,rtsp_port)


from twisted.internet import reactor
print("run")
reactor.run()

print("end")
