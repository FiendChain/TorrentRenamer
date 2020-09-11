import re
import os

SERIES_PATTERN = re.compile(r"([\w\s\-\_]+)")

def get_series_from_path(filepath):
    filename = os.path.basename(filepath)
    m = SERIES_PATTERN.findall(filename)
    if len(m) == 0:
        return None
            
    sname = m[0]
    sname = sname.strip()

    return sname
