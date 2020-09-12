from argparse import ArgumentParser
import os
import sys
sys.path.insert(0, "./src/main/python/")

from util import parse_directory, clean

def main():
    parser = ArgumentParser()
    parser.add_argument("base_dir")
    parser.add_argument("--title", default=None)

    args = parser.parse_args()

    root_dir = args.base_dir
    for filename in sorted(os.listdir(root_dir)):
        base_dir = os.path.join(root_dir, filename)
        if not os.path.isdir(base_dir):
            continue

        p = parse_directory(base_dir)

        ignores = p.get('ignores')
        conflicts = p.get('conflicts')
        renames = p.get('renames')

        # os.system('clear')
        if len(renames) == 0:
            continue

        print(f"{base_dir}")
        print(">>> ignores")
        print("\n".join(ignores)) 
        print()
        print(">>> conflicts")
        print("\n".join((f"{k} => {v}" for k, v in conflicts)))
        print()
        print(">>> renames")
        print("\n".join((f"{k} => {v}" for k, v in renames)))

        res = input("continue? (y/n)")
        res = res.lower()
        if not res == 'y':
            continue

        print(">>> renaming")
        for old_name, new_name in p.get('renames'):
            old_name = os.path.join(base_dir, old_name)
            new_name = os.path.join(base_dir, new_name)
            dirname = os.path.dirname(new_name)
            os.makedirs(dirname, exist_ok=True)
            os.rename(old_name, new_name)

        print(">>> cleaning")
        clean(base_dir)

if __name__ == '__main__':
    main()