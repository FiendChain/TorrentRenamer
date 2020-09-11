from argparse import ArgumentParser
import os
import json
import re

from src.api import Api

def main():
    parser = ArgumentParser()
    parser.add_argument("base_dir")
    parser.add_argument("--cred", default="credentials.json")

    args = parser.parse_args()
    api = Api.load_api(args.cred)
    # api = None

    metaname = "series.json"

    base_dir = args.base_dir

    p = re.compile(r"([\w\s\-\_]+)")

    for filename in sorted(os.listdir(base_dir)):
        filepath = os.path.join(base_dir, filename)
        if not os.path.isdir(filepath):
            continue

        m = p.findall(filename)
        if len(m) == 0:
            print(f"format err {filename}")
            continue

        sname = m[0]

        metapath = os.path.join(filepath, metaname)
        if os.path.exists(metapath):
            with open(metapath, "r") as fp:
                meta = json.load(fp)
            api_id = meta.get("id")
            print(f"meta exists {filename} => {sname} (id={api_id})")
            continue


        res = api.search_series(sname)
        if res is None or len(res) == 0:
            print(f"no matches {filename} => {sname}")
            continue

        i = select_series(res)
        if i is None:
            print(f"skipping {filename} => {sname}")
            continue

        series = res[i]

        print(f"writing {filename} => {sname}")
        with open(metapath, "w+") as fp:
            json.dump(series, fp, indent=1)

def select_series(res, max_list=15):
    for i, series in enumerate(res[:max_list]):
        print("{}: {} - {} (id={}, status={})".format(
            i+1,
            series.get('seriesName'),
            series.get('firstAired', None),
            series.get('id'),
            series.get('status', '?')))
    
    while True:
        try:
            rv = input("select: ")
            rv = rv.strip()
            rv = rv.lower()
            if rv in ('s', 'skip'):
                return None

            i = int(rv)-1
            if i < 0 or i >= len(res):
                print('out of range')
                continue
            return i
        except KeyboardInterrupt:
            exit()
        except:
            print(f'invalid selection ({rv})')
            continue

if __name__ == '__main__':
    main()