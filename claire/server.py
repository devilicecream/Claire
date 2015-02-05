__author__ = 'walter'
from .config import Client, STATUS_UNTESTED, STATUS_OK, STATUS_BAD
import socket
import logging

log = logging.getLogger('Claire')
socket.setdefaulttimeout(10)


class Server(object):
    def __init__(self, config, hostname):
        self.config = config
        self.hostname = hostname
        self.processes = []
        self.status = STATUS_UNTESTED

    def test(self):
        """
        Try connection to the server and then check the processes
        """
        log.info("--> Checking server %s" % self.hostname)
        client = Client()
        try:
            client.connect(host=self.hostname)
        except (socket.gaierror, socket.timeout):
            self.status = STATUS_BAD

        if self.status != STATUS_BAD:
            self.status = STATUS_OK
            for process in self.processes:
                result = process.test(client)
                if result != STATUS_OK:
                    log.warning("* Process %s DOWN. Reporting" % process.name)
                    self.status = STATUS_BAD
                    self.config['reporter'].report_process(process, self)
        else:
            log.warning("* Server %s DOWN. Reporting" % self.hostname)
            self.config['reporter'].report_server(self)
        return self.status

    def __repr__(self):
        return """
            Hostname: %s\n
            Status: %s\n
            Processes: %s\n
        """ % (self.hostname,
               self.status == STATUS_OK and "OK" or "UNREACHABLE",
               self.processes)
