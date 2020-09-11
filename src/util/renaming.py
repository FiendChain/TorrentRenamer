from .patterns import get_group
from .garbage import del_filter
from collections import Counter
import os, json, re

SEASON_FMT = "Season {season:02d}"
EPISODE_FMT = "{title}-S{season:02d}E{episode:02d}{name}.{extension}"

def parse_directory(base_dir, title=None):
    series_metapath = os.path.join(base_dir, "series.json")
    eps_metapath = os.path.join(base_dir, "episodes.json")

    with open(series_metapath, "r") as fp:
        series_data = json.load(fp)

    if title is None:
        p = re.compile(r"([\w\s\-\_]+)")
        title = series_data.get('seriesName')
        title = re.sub(r"[']", "", title)
        title = re.sub(r"[^a-zA-Z0-9\(\)]", " ", title)
        title = p.findall(title)[0]
    
    with open(eps_metapath, "r") as fp:
        eps_data = json.load(fp)
        ep_lookup = create_lookup(eps_data)

    mapper = recursive_map(base_dir)

    deletes = []

    filtered_mapper = {}
    for filepath, info in mapper.items():
        if del_filter(filepath):
            deletes.append(filepath)
            continue
        filtered_mapper[filepath] = info
    
    mapper = filtered_mapper

    counts = Counter()
    for filepath, info in mapper.items():
        if info is None:
            continue
        k = (info.season, info.episode, info.ext)
        counts[k] += 1

    conflicts = []
    renames = []
    ignores = []
    corrects = []

    for old_path, info in mapper.items():
        new_name = get_new_name(info, ep_lookup, title)
        if new_name is None:
            ignores.append(old_path)
            continue
        
        if os.path.realpath(old_path) == os.path.realpath(new_name):
            corrects.append(old_path)
            continue

        k = (info.season, info.episode, info.ext)
        if counts[k] > 1:
            conflicts.append((old_path, new_name))
        else:
            renames.append((old_path, new_name))
    
    return {"conflicts": conflicts, "renames": renames, "ignores": ignores, "deletes": deletes, "corrects": corrects}


def get_new_name(info, ep_lookup, title):
    if info is None:
        return None

    k = (info.season, info.episode)
    if k in ep_lookup:
        edata = ep_lookup.get(k)
        name = edata.get('episodeName')
        name = clean_string(name)
        name = f"-{name}"
    else:
        name = ''

    dirname = SEASON_FMT.format(season=info.season)
    filename = EPISODE_FMT.format(
        title=clean_string(title),
        season=info.season,
        episode=info.episode,
        name=name,
        extension=info.ext)
    
    return os.path.join(dirname, filename)

def clean_string(string):
    string = re.sub(r"[',\(\)\[\]]", "", string)
    string = re.sub(r"[^a-zA-Z0-9]", " ", string)
    string = string.strip()
    string = '.'.join(string.split())
    # p = re.compile(r"[\s+]")
    # string = p.sub(r".", string)
    return string

def recursive_map(base_dir):
    def func(base_dir, rel_dir, mapper):
        search_dir = os.path.join(base_dir, rel_dir) 
        for filename in os.listdir(search_dir):
            filepath = os.path.join(search_dir, filename)
            sub_filepath = os.path.join(rel_dir, filename)
            if os.path.isdir(filepath):
                func(base_dir, sub_filepath, mapper)
            elif os.path.isfile(filepath):
                mapper[sub_filepath] = get_group(filename)
        return mapper
    
    mapper = {}
    return func(base_dir, ".", mapper)

def create_lookup(episodes_data):
    ep_lookup = {}
    for edata in episodes_data:
        season = edata.get("airedSeason")
        episode = edata.get("airedEpisodeNumber")
        ep_lookup[(season, episode)] = edata
    return ep_lookup