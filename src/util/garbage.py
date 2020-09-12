import os

BANNED_EXTS = ("txt", "nfo")
WHITELIST = ("series.json", "episodes.json")

def del_filter(name):
    filename = os.path.basename(name)
    if filename in WHITELIST:
        return False

    tokens = name.split(".")
    if len(tokens) == 1:
        return True
    ext = tokens[-1]
    if ext in BANNED_EXTS:
        return True
    return False

def clean(base_dir, root=True, debug=None):
    for filename in os.listdir(base_dir):
        filepath = os.path.join(base_dir, filename)
        if os.path.isdir(filepath):
            clean(filepath, root=False)
    
    if root:
        return
    
    n = len(os.listdir(base_dir))
    if n == 0:
        if debug is not None:
            debug(base_dir)
        os.rmdir(base_dir)
