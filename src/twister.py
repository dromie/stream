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

    def stopProcess(self):
        print("Sending TERM singal")
        self.transport.signalProcess('TERM')

class EncoderFactory(ProxyClientFactory):
    def __init__(self,twister):
        self.twister = twister
    
    def startEncoder(self, host):
        print("StartEncoder: ", host)
        control = EncoderControll(self.twister,False)
        p = self.twister.command_line(host)
        print("cmd: %s, args: %s"%(p[0],p[1]))
        from twisted.internet import reactor
        reactor.spawnProcess(control,p[0],p[1])
        return control

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
        self.processcontrol = encoder.startEncoder(port.getHost())

    def connectionLost(self, reason):
        print("Connection lost..")
        self.processcontrol.stopProcess()

    def dataReceived(self, data):
        print("Data received: %s" % data)
        Proxy.dataReceived(self, data)
    


class Twister(ReconnectingClientFactory):

    def __init__(self,host,port,cmdline = None):
        from twisted.internet import reactor
        reactor.connectTCP(host, port, self)
        self.cmdLine = cmdline
        if not self.cmdLine:
          self.cmdLine = ["nc","{host}", "{port}"]
        print(self.cmdLine)
        
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
  
    def command_line(self,host):
        target= {"host": host.host, "port":str(host.port)}
        l = list([ e.format(**target) for e in self.cmdLine ])
        return (l[0],l)
    
    def encoderStopped(self, isIdle):
        if isIdle:
            pass
        else:
            pass

if __name__ == '__main__':
  rtsp_host = sys.argv[1]
  rtsp_port = int(sys.argv[2])
  cmdLine=None
  if (len(sys.argv)>2):
    cmdLine = sys.argv[3].split(',')
  print("Start")

  print("From: (%s:%d)" % (rtsp_host, rtsp_port))
  print("cmdLine: ",cmdLine)
  twister = Twister(rtsp_host,rtsp_port,cmdLine)


  from twisted.internet import reactor
  print("run")
  reactor.run()

  print("end")
