import paramiko, os


class Client(paramiko.SSHClient):
    def __init__(self, *args, **kw):
        super(Client, self).__init__(*args, **kw)
        self._policy = paramiko.WarningPolicy()
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.ssh_config = paramiko.SSHConfig()
        user_config_file = os.path.expanduser("~/.ssh/config")
        if os.path.exists(user_config_file):
            with open(user_config_file) as f:
                self.ssh_config.parse(f)

    def connect(self, host):
        cfg = {'hostname': host}

        user_config = self.ssh_config.lookup(cfg['hostname'])
        for k in ('hostname', 'user', 'port'):
            if k in user_config:
                key = k
                if k == 'user':
                    key = 'username'
                cfg[key] = user_config[k] if k != 'port' else int(user_config[k])
        return super(Client, self).connect(**cfg)
