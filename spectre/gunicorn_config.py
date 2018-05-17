from spectre.settings import GUNICORN_SETTINGS as gsettings

# general
bind = "{}:{}".format(gsettings.get('bind_ip', '0.0.0.0'), gsettings.get('bind_port', '8042'))
workers = gsettings.get('workers', 1)
worker_class = gsettings.get('worker_class', "sync")
daemon = gsettings.get('daemon', False)
timeout = gsettings.get('timeout', 300)

# requires futures module for threads > 1
threads = gsettings.get('threads', 1)

# during development, this will cause the server to reload when the code changes
reload = gsettings.get('reload', True)

# logging
# accesslog = "/var/log/gunicorn/account_activator_access.log"
# errorlog = "/var/log/gunicorn/account_activator_error.log"
syslog = gsettings.get('syslog', False)
syslog_addr = gsettings.get('syslog_addr', "udp://localhost:514")
syslog_prefix = gsettings.get('syslog_prefix', None)
syslog_facility = gsettings.get('syslog_facility', "local")

# ssl
keyfile = gsettings.get('keyfile', '/spectre_certs/localhost.key')
certfile = gsettings.get('certfile', '/spectre_certs/localhost.crt')

# statsd
host = gsettings.get('statsd_host', None)
port = gsettings.get('statsd_port', None)
if host and port:
    statsd_host = "%s:%s" % (host, port)
else:
    statsd_host = None
statsd_prefix = gsettings.get('statsd_prefix', None)
