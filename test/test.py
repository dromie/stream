#!/usr/bin/env python
from twisted.trial import unittest
from twisted.internet.protocol import ClientFactory, ServerFactory, Protocol
from twisted.internet.defer import Deferred

import sys
import os
sys.path.insert(0, os.path.abspath('../src'))

import twister

class Sender(Protocol):
  def connectionMade(self):
    self.transport.write(self.factory.testdata)
    self.transport.loseConnection()

class TwistedTest(unittest.TestCase):
  def setUp(self):
    from twisted.internet import reactor
    factory = Factory.forProtocol(Sender)
    factory.testdata="01234567890"
    self.port = reactor.listenTCP(0, factory, interface="127.0.0.1")
    self.twister=Twister('localhost', self.port.getHost().port )

  def tearDown(self):
    port, self.port = self.port, None
    return port.stopListening()


  def test_twister(self):
    return Deferred()    
