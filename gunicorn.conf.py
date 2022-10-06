import multiprocessing

# bind
bind = "0.0.0.0:8001"
# bind = "unix:/run/cgims.sock"

workers = multiprocessing.cpu_count() * 2 + 1
reload_engine = "inotify"
group = "realestkma"
user = "realestkma"
reload = True

# logs
loglevel = "debug"
accesslog = "logs/gunicorn/openuserdata.access"
errorlog = "logs/gunicorn/openuserdata.error"
