from argparse import ArgumentParser
import os, json, re

from api import Api

def main():
    parser = ArgumentParser()
    parser.add_argument("base_dir")
    parser.add_argument("--cred", default="credentials.json")

    args = parser.parse_args()
    api = Api.load_api(args.cred)

    metaname = "series.json"
    ep_metaname = "episodes.json"
    base_dir = args.base_dir

    for filename in sorted(os.listdir(base_dir)):
        filepath = os.path.join(base_dir, filename)
        if not os.path.isdir(filepath):
            continue
        
        metapath = os.path.join(filepath, metaname)
        ep_metapath = os.path.join(filepath, ep_metaname)

        if not os.path.exists(metapath):
            continue

        if os.path.exists(ep_metapath):
            continue
        
        with open(metapath, "r") as fp:
            sdata = json.load(fp)

        sid = sdata.get("id") 

        edata = api.get_series_episodes(sid)
        if edata is None:
            edata = []

        with open(ep_metapath, "w+") as fp:
            json.dump(edata, fp, indent=1)
        print(f"{filename} => {len(edata)}")


if __name__ == '__main__':
    main()