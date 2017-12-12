#!/bin/python3
import argparse
import os
import sys

def add_prefix(file_dir,file_name,prefix,prefix_rem,is_dry_run):
    old_path = os.path.join(file_dir,file_name)
    if not file_name.startswith(prefix_rem):
        print(old_path+" does not contain the replacement prefix "+prefix_rem)
        return
    new_name = prefix+file_name[len(prefix_rem):]
    new_path = os.path.join(file_dir,new_name)
    if os.path.exists(new_path):
        print("Not modifying "+old_path)
    else:
        if is_dry_run:
            print(old_path+" => "+new_path)
        else:
            os.rename(old_path,new_path)


def recurse_dir(path,prefix,prefix_rem,is_dry_run):
    if os.path.isdir(path):
        for dirpath, dirnames, files in os.walk(path):
            for name in files:
                add_prefix(dirpath,name,prefix,prefix_rem,is_dry_run)
    else:
        print("Given path is not a directory")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Recursively add prefix to a folder')
    parser.add_argument('path', metavar='F',
                    help='path to the target folder')
    parser.add_argument('prefix', metavar='P',
                    help='Prefix to be inserted')
    parser.add_argument('--replace', default='',
                    help='Prefix to be removed')
    parser.add_argument('--dryrun', action="store_true",
                    help='Print a list of changes that will be made')
    args = parser.parse_args()
    path=args.path
    prefix=args.prefix
    prefix_rem=args.replace
    is_dry_run = args.dryrun
    recurse_dir(path,prefix,prefix_rem,is_dry_run)
