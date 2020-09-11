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

def clean(base_dir):
    for filename in os.listdir(base_dir):
        filepath = os.path.join(base_dir, filename)
        if os.path.isdir(filepath):
            clean(filepath)
    
    n = len(os.listdir(base_dir))
    if n == 0:
        print(f"removing {base_dir}")
        os.rmdir(base_dir)