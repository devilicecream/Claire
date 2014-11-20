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
### Hosts file
Claire uses by default the hosts file in /etc/claire/hosts.
To use another path for the hosts file, simply type
```bash
    $ claire stats --hosts <path of the hosts file>
```
The hosts file is an *ini* file structured in this way:
```ini
    [group_name]
    host_name
    check="<check if process with this name is active>"
    faiulre="<run this command in case of failure and retry>"
```
## TODO
* Make server checks parallel
* Check service status