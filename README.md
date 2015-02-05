# Claire
Claire is an open source *CLI* cluster management tool that works over SSH.
It provides a fast and clear interface to the state of your servers.

## Install
To install Claire clone this repository in your personal folder and type:
```bash
$ cd claire && python setup.py install
```

## How to use
To use Claire simply type in your shell:
```bash
$ claire stats
```
## Daemon
To run Claire as a daemon, you need to have super user privileges:
```bash
$ sudo claire stats --daemon
```
To stop the daemon:
```bash
$ sudo claire stats --stop-daemon
```
### Config file
Claire uses by default the config file in **/etc/claire/config**.
To use another file as config, type:
```bash
$ claire stats --conf <path of the config file>
```
The config file is an *ini* file structured in this way:
```ini
[default]
pidfile=<pid file location> DEFAULT=/etc/claire/claire.pid
interval=<check interval (only for daemon mode)> DEFAULT=300

[reporter]
name=<reporter name>
<reporter configuration key>=<reporter configuration value>

[loggers]
...

[handlers]
...

[formatters]
...
```
The config file contains also the logging configuration, 
in the standard python logging config [format](https://docs.python.org/2/howto/logging.html#configuring-logging).

An example of the config file can be found in the `config_example` folder.
### Reporter
The reporter is the object in charge of reporting the errors.
It inherits from the class **Reporter**, defined in `reporter.py`,
which methods **report_server** and **report_process** are called
when an error occours reaching a server or checking for a process.
### Hosts file
Claire uses by default the hosts file in **/etc/claire/hosts**.
To use another file as hosts, type:
```bash
$ claire stats --hosts <path of the hosts file>
```
The hosts file is an *ini* file structured in this way:
```ini
[group_name]
host_name
check=<check if process with this name is active>
instances=<desired number of running instances of the process>
failure=<run this command in case of failure and retry>
```

An example of the hosts file can be found in the `config_example` folder.
### Single group
To only make Claire check for a single hosts group:
```bash
$ claire stats --group <group name>
```
## TODO
* Make server checks parallel
* Check service status