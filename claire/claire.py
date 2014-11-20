__author__ = 'walter'
import sys
from .config import Client
from clint.textui import colored, indent, puts

Parser = None
try:
    import ConfigParser as Parser
except:
    import configparser as Parser


def cprint(string, color=colored.clean, indentation=0, quote=""):
    with indent(indentation, quote=color(quote)):
        puts(color(string))


def check_section(config, section):
    cprint("Group %s" % section, colored.clean, 2, quote=" - ")
    items = config.items(section)
    success = retry = fail = 0
    servers = [i[0] for i in items if i[1] is None]
    check = dict(items).get('check')
    failure = dict(items).get('failure', None)

    def check_server(server, failures=0):
        client = Client()
        try:
            client.connect(host=server)
            stdin, stdout, stderr = client.exec_command('ps aux | grep %s' % check)
        except Exception as e:
            cprint('unreachable', colored.red, 4, quote='    [%s] ' % server)
            return 0, 0, 1

        if len(stdout.readlines()) > 2:
            cprint('active', colored.green, 4, quote='    [%s] (%s) ' % (server, check))
            return 1, failures, 0
        else:
            cprint('non active', colored.red, 4, quote='    [%s] (%s) ' % (server, check))
            failures += 1
            if failure is not None and failures < 3:
                try:
                    client.exec_command(failure)
                except Exception as e:
                    cprint('unreachable', colored.red, 4, quote='    [%s] ' % server)
                    return 0, 0, 1
                cprint("Failure command retry #%s" % str(failures), colored.yellow, 4, quote='    [%s] ' % server)
                return check_server(server, failures)
            return 0, failures, 1

    for srv in servers:
        success, retry, fail = check_server(srv, failures=0)
    return len(servers), success, retry, fail


def stats_command(hosts="/etc/claire/hosts", group=None):
    """Retrieves stats from servers in the hosts file.
    If a --group is specified, it retrieves stats only for the specified group"""
    groups = servers = success = fail = retry = 0
    try:
        stream = file(hosts, 'r')
        config = Parser.ConfigParser(allow_no_value=True)
        config.readfp(stream)
        sections = config.sections()
    except Exception as e:
        cprint("Error in hosts file: %s" % str(e), colored.red, 1)
        sys.exit(1)

    if group is not None and group in sections:
        groups = 1
        servers, success, retry, fail = check_section(config, group)
    else:
        for section in sections:
            groups += 1
            _servers, _success, _retry, _fail = check_section(config, section)
            servers += _servers
            success += _success
            retry += _retry
            fail += _fail

    result_string = "Results:     groups=%s     servers=%s     success=%s     fail=%s     retry=%s\n" \
                    % (groups, servers, success, fail, retry)
    cprint("-" * len(result_string), indentation=1)
    if fail > 0:
        color = colored.red
    elif retry > 0:
        color = colored.yellow
    else:
        color = colored.green
    cprint(result_string, color, 1)


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