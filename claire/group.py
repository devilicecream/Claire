__author__ = 'walter'
from .server import Server
from .config import STATUS_OK, STATUS_BAD, pretty
from .process import Process
import logging

log = logging.getLogger('Claire')


class Group(object):
    def __init__(self, config, name):
        self.config = config
        self.name = name
        self.result = {}
        self.status = STATUS_OK

    def test(self):
        log.info("Group %s" % self.name)
        items = self.config['hosts'].items(self.name)
        servers = [i[0] for i in items if i[1] is None]
        for server in servers:
            server = Server(self.config, server)
            check = dict(items).get('check')
            failure = dict(items).get('failure', None)
            instances = dict(items).get('instances', 1)
            server.processes = [Process(check, instances, failure=failure)]
            status = server.test()
            if status != STATUS_OK:
                self.status = STATUS_BAD
            self.result[server.hostname] = status == STATUS_OK and "OK" or "ERROR"
        return self.status

    def __repr__(self):
        return """Group: %s\nStatus: %s\nServers:\n%s""" % (self.name,
                                                            self.status == STATUS_OK and "OK" or "ERROR",
                                                            pretty(self.result))