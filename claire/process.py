__author__ = 'walter'
from .config import STATUS_UNTESTED, STATUS_OK, STATUS_BAD, pretty
from collections import OrderedDict
import re


class Process(object):
    def __init__(self, name, instances=1, failure=None):
        self.name = name
        self.instances = int(instances)
        self.active_instances = 0
        self.status = STATUS_UNTESTED
        self.failure = failure
        self.info = []

    def test(self, client):
        """
        Test the process
        """
        stdin, stdout, stderr = client.exec_command('pidof -x %s' % self.name)
        lines = stdout.readlines()
        if not len(lines):
            self.active_instances = 0
            self.status = STATUS_BAD
        else:
            self.active_instances = len(lines[0].split(" "))
            if self.active_instances < self.instances:
                self.status = STATUS_BAD
            else:
                self.status = STATUS_OK
            stdin, stdout, stderr = client.exec_command('ps aux | grep "%s"' % self.name)
            lines = stdout.readlines()
            for index, line in enumerate(lines):
                if 'grep' not in line:
                    line = re.sub(r'[ \t]+', ' ', line)
                    user, pid, cpu, mem, _, _, _, status, start, time, command = line.split(' ', 10)
                    instance = OrderedDict(User=user,
                                           PID=pid,
                                           CPU=cpu + "%",
                                           MEM=mem + "%",
                                           Status=status,
                                           Start=start,
                                           Time=time,
                                           Command=command.replace("\n", ""))
                    self.info.append(instance)

        if self.status == STATUS_BAD:
            # TODO: try the failure command
            pass
        return self.status

    def __repr__(self):
        return """
            Process name: %s\n
            Desired running instances: %s\n
            Effective running instances: %s\n
            Status: %s\n
            PS AUX: %s\n
        """ % (self.name,
               self.instances,
               self.active_instances,
               self.status == STATUS_OK and "OK" or "DOWN",
               pretty(self.info))
