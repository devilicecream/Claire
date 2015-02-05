__author__ = 'walter'
from .group import Group
from .reporters import Reporters
from .daemon import Daemon
from time import sleep
import sys
import logging
import logging.config


DEFAULT_CONFIG = "/etc/claire/config"
DEFAULT_HOSTS = "/etc/claire/hosts"
DEFAULT_PIDFILE = "/etc/claire/claire.pid"
DEFAULT_INTERVAL = 30

Parser = None
try:
    import ConfigParser as Parser
except Exception:
    import configparser as Parser


def get_or_none(self, section, value, func_name=None, **kw):
    try:
        if func_name:
            return getattr(self, func_name)(section, value, **kw)
        return self.get(section, value, **kw)
    except Exception:
        return None

Parser.ConfigParser.get_or_none = get_or_none


def parse_config(conf, hosts):
    config = {}
    try:
        config_stream = file(conf, 'r')
        configuration = Parser.ConfigParser(allow_no_value=True)
        configuration.readfp(config_stream)
        reporter = Reporters.get(configuration.get('reporter', 'name'))
        config['pidfile'] = configuration.get_or_none('default', 'pidfile') or DEFAULT_PIDFILE
        config['interval'] = configuration.get_or_none('default', 'interval', func='getint') or DEFAULT_INTERVAL
        config['reporter'] = reporter(configuration)
    except Exception as e:
        print("Error in config file: %s" % str(e))
        sys.exit(1)

    try:
        hosts_stream = file(hosts, 'r')
        config['hosts'] = Parser.ConfigParser(allow_no_value=True)
        config['hosts'].readfp(hosts_stream)
    except Exception as e:
        print("Error in hosts file: %s" % str(e))
        sys.exit(1)

    return config


def stats_command(hosts=DEFAULT_HOSTS, conf=DEFAULT_CONFIG, group=None, daemon=False, stop_daemon=False):
    """Retrieves stats from servers in the hosts file.
    If a --group is specified, it retrieves stats only for the specified group.
    If --daemon, it executes as a daemon, using the timing specified in config file.
    Otherwise, it only executes once.
    If --stop-daemon, it kills the previously created daemon.
    """
    logging.config.fileConfig(conf)
    config = parse_config(conf, hosts)

    if daemon:
        def daemonized(config, group):
            while 1:
                do_stats(config, group, daemon=True)
                sleep(config['interval'])
        daemon = Daemon(config['pidfile'])
        daemon.func = daemonized
        daemon.args = {'config': config, 'group': group}
        print("Starting Claire as an angel...")
        daemon.start()
    elif stop_daemon:
        daemon = Daemon('/etc/claire/claire.pid')
        print("Killing the angel Claire...")
        daemon.stop()
    else:
        do_stats(config, group, daemon=False)


def do_stats(config, group_name, daemon):
    log = logging.getLogger('Claire')
    sections = config['hosts'].sections()

    if group_name:
        if group_name in sections:
            group = Group(config, group_name)
            group.test()
            if not daemon:
                print group
        else:
            log.critical("Group %s is not present in the hosts file" % group_name)
            sys.exit(1)
    else:
        for group_name in sections:
            group = Group(config, group_name)
            group.test()
            if not daemon:
                print group


def main():
    import scriptine
    try:
        scriptine.run()
    except KeyError:
        print "Unrecognized argument."
        sys.argv.append("--help")
        scriptine.run()

if __name__ == "__main__":
    main()