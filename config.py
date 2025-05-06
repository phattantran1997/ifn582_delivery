import os

def load_env_file(path='.env'):
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            if '=' in line:
                key, val = line.strip().split('=', 1)
                os.environ[key] = val
