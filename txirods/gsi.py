#############################################################################
#
# Copyright (c) 2010 Russell Sim <russell.sim@gmail.com> and Contributors.
# All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from zope.interface import implements
from twisted.internet import defer, reactor
from twisted.internet import interfaces
from twisted.python import log
from pyGlobus.security import GSSCred, GSSContext, GSSContextException
from pyGlobus.security import GSSName, GSSMechs, GSSUsage
from pyGlobus.security import ContextRequests, GSSCredException
from pyGlobus import gssc


class GSIAuth(object):
    implements(interfaces.IPushProducer)

    def beginAuthentication(self, data, consumer, producer):
        self.paused = 0; self.stopped = 0
        self.consumer = consumer
        self.producer = producer
        self.deferred = deferred = defer.Deferred()
        self.consumer.registerProducer(self, False)
        self.producer.registerConsumer(self)
        self.data = {}
        self.buffer = ''
        self.resumeProducing(data, first=True)
        return deferred

    def pauseProducing(self):
        self.paused = True

    def write(self, data):
        # TODO should use the buffer in the class
        #self.buffer = self.buffer + data
        self.resumeProducing(data)

    def resumeProducing(self, data='', first=False):
        # transport calls resumeProducing when this is attached
        if not first and not data:
            return
        self.paused = False
        if first:
            if not data:
                # Already Authed because there was no DN
                # recieved from the server
                self.consumer.unregisterProducer()
                self.producer.unregisterConsumer()
                reactor.callLater(0.001, self.deferred.callback, True)
                return
            server_dn = data.split('\0')[0]
            log.msg(server_dn)
            self.data['server_dn'] = server_dn

            # create credential
            init_cred = GSSCred()
            name, mechs, usage = GSSName(free=False), GSSMechs(), GSSUsage()

            try:
                init_cred.acquire_cred(name, mechs, usage)
            except GSSCredException:
                self.deferred.errback()
                return

            try:
                lifetime, credName = init_cred.inquire_cred()
            except GSSCredException:
                self.deferred.errback()
                return

            context = GSSContext()
            requests = ContextRequests()

            target_name = GSSName()
            major, minor, targetName_handle = \
                   gssc.import_name('arcs-df.vpac.org',
                                    gssc.cvar.GSS_C_NT_HOSTBASED_SERVICE)
            target_name._handle = targetName_handle

            requests.set_mutual()
            requests.set_replay()

            self.data.update({'name': name, 'lifetime': lifetime,
                              'credName': credName, 'targetName': target_name,
                              'todelete': name, 'context': context,
                              'requests': requests, 'cred': init_cred})
        else:
            context = self.data['context']
            init_cred = self.data['cred']
            target_name = self.data['targetName']
            requests = self.data['requests']
            self.buffer = self.buffer + data
            data = self.buffer

        try:
            major, minor, outToken = \
                   context.init_context(init_cred=init_cred,
                                        target_name=target_name,
                                        inputTokenString=data,
                                        requests=requests)
        except GSSContextException:
            # XXX this doesn't seem to be called, no idea
            print GSSContextException
        else:
            self.buffer = ''

        self.consumer.write(outToken)
        # XXX WTF is with this number?
        if major == gssc.GSS_S_COMPLETE:
            # Reset all class variables
            self.consumer.msg_len = 0
            self.consumer.unregisterProducer()
            self.producer.unregisterConsumer()
            # There is a minor delay because the other end cannot
            # detect when the gsi auth has finished
            reactor.callLater(0.001, self.deferred.callback, True)
        return

    def stopProducing(self):
        print 'stopProducing: invoked'
        self.consumer.unregisterProducer()
        self.producer.unregisterConsumer()
