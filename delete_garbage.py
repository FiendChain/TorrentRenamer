from argparse import ArgumentParser
import os
import glob

from src.util import *

def main():
    parser = ArgumentParser()
    parser.add_argument("base_dir")

    args = parser.parse_args()

    root_dir = args.base_dir
    for filename in sorted(os.listdir(root_dir)):
        base_dir = os.path.join(root_dir, filename)
        if not os.path.isdir(base_dir):
            continue
            
        garbage = sorted(search_garbage(base_dir))
        # os.system('clear')
        if len(garbage) == 0:
            continue
        
        print(f"\n{base_dir}")
        print(">>> delete")
        print("\n".join(garbage))

        res = input("continue? (y/n)")
        res = res.lower()
        if not res == 'y':
            continue

        print(">>> deleting")
        for name in garbage:
            os.remove(os.path.join(base_dir, name))
        print(">>> cleaning")
        clean(base_dir)

def search_garbage(basedir):
    def func(basedir, reldir, files):
        absdir = os.path.join(basedir, reldir)
        for filename in os.listdir(absdir):
            filepath = os.path.join(absdir, filename)
            if os.path.isdir(filepath):
                subreldir = os.path.join(reldir, filename)
                func(basedir, subreldir, files)
            elif os.path.isfile(filepath):
                if del_filter(filename):
                    files.append(os.path.join(reldir, filename))
        return files
    files = []
    return func(basedir, ".", files)


if __name__ == '__main__':
    main()