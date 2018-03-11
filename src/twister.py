#!/usr/bin/env python
import sys

from twisted.internet.protocol import  ReconnectingClientFactory, ProcessProtocol
from twisted.protocols.portforward import Proxy, ProxyClientFactory

class EncoderControll(ProcessProtocol):
    def __init__(self, twister, idle=True):
        self.twister = twister
        self.idle = idle

    def connectionMade(self):
        self.twister.notifyStarted(self.idle)

    def processEnded(self, status):
        print("Process ended: %s" % status)
        self.twister.notifyStopped(self.idle)

    def outReceived(self,data):
        print("PP: %s" % data)

    def stopProcess(self):
        print("Sending TERM singal")
        self.transport.signalProcess('TERM')

class EncoderFactory(ProxyClientFactory):
    def __init__(self,twister):
        self.twister = twister
    

class CameraFeed(Proxy):
    def __init__(self,twister):
        self.twister = twister

    def connectionMade(self):
        print("Connected to camera feed")
        self.transport.pauseProducing()
        listener = ProxyClientFactory()
        listener.setServer(self)
        encoder = EncoderFactory(self.twister)
        encoder.setServer(self)
        from twisted.internet import reactor
        port = reactor.listenTCP(0, listener)

    def connectionLost(self, reason):
        print("Connection lost..")
        self.twister.stopEncoder()
        self.twister.startIdle()

    def dataReceived(self, data):
        print("Data received: %s" % data)
        Proxy.dataReceived(self, data)
    

CONNECTING = 1
CONNECTED = 2

class Twister(ReconnectingClientFactory):



    def __init__(self,host,port,cmdlineEncoder = None, cmdlineIdle = None):
        self.state = CONNECTING
        from twisted.internet import reactor
        reactor.connectTCP(host, port, self)
        self.cmdLine = { False:cmdlineEncoder, True:cmdlineIdle }
        self.control = None
        if not self.cmdLine[False]:
          self.cmdLine[False] = ["nc","{host}", "{port}"]
        print(self.cmdLine)
        self.startIdle()
        
    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print("Connected to %s" % addr)
        self.stateTransition(CONNECTED) 
        return CameraFeed(self)

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)
        self.stateTransition(CONNECTING) 
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason: %s, delay: %d', (reason, self.delay))
        self.stateTransition(CONNECTING) 
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
 
    def stateTransition(self, newstate):
        if self.state != newstate:
          if (self.state,newstate) == (CONNECTING,CONNECTED):
            # Will be done by CameraFeed
            pass
          if (self.state,newstate) == (CONNECTED,CONNECTING):
            self.stopEncoder()
            self.startIdle()

    def command_line(self, host, cmdline):
        target = None
        if not host is None:
          target= {"host": host.host, "port":str(host.port)} 
        l = list([ e.format(**target) for e in cmdline ])
        return (l[0],l)
    

    def start(self, idle, host = None):
      print("StartEncoder: ", host)
      if not self.control is None:
        self.control.stopProcess()

      if not self.cmdLine[idle] is None:
        self.control = EncoderControll(self, idle)
        p = self.command_line(host,self.cmdLine[idle])
        print("cmd: %s, args: %s"%(p[0],p[1]))
        from twisted.internet import reactor
        reactor.spawnProcess(self.control,p[0],p[1])
      else:
        print("cmdLine for idle:%s is None"% (str(idle)) )

    def stop(self):
      if not self.control is None:
        self.control.stopProcess()
        self.control = None

    def startEncoder(self, host):
      self.start(False, host)

    def startIdle(self):
      self.start(True)

    def stopEncoder(self):
      self.stop()

    def stopIdle(self):
      self.stop()


    def notifyStarted(self, isIdle):
      pass

    def notifyStopped(self, isIdle):
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
