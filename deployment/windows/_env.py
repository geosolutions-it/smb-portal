import sys, re

kvre = re.compile(r"([a-zA-Z0-9_\\-]+)=(.+)")

run = False
try:
    env_file = sys.argv[1]
    if env_file == '':
        raise()
    with (open(env_file, 'r')) as f:
        for l in f:
            kv = kvre.match(l)
            if kv:
                print("SET {}={}".format(*kv.groups()))
except Exception:
    exit(1)
