import os
import re
import shutil
import sys


def fetch_link(f_path):
    reg_link = re.compile(r'!\[.*?\]\((.*)\)')
    with open(f_path, 'r', encoding='utf-8') as fp:
        content = fp.read()
    links = reg_link.findall(content)
    parent = os.path.dirname(f_path)
    links = [os.path.join(parent, item) for item in links]
    return links


def md_move(src_file, desc):
    print("MD_MOVE: (%s) to (%s) start ..." % (src_file, desc))
    if not os.path.isfile(src_file):
        print("MD_MOVE: src must be file")
    if not os.path.isdir(desc):
        print("MD_MOVE: desc must be directory")
    links = fetch_link(src_file)
    shutil.move(src_file, desc)
    for item in links:
        assets = os.path.join(desc, 'assets')
        if not os.path.exists(assets):
            print("MD_MOVE: assets(%s) dir not exists")
            os.mkdir(assets)
        shutil.move(item, assets)
    print("MD_MOVE: md move file end ...")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("MD_MOVE: arg format is error")
    else:
        md_move(sys.argv[1], sys.argv[2])
