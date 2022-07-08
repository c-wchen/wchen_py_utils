#!/usr/bin/env python3

import glob
import re
import dateutil.parser
import sys
import yaml

sys.path.append('..')
from file import encoding

front_matter_regex = re.compile('^\n*---([\s\S]*?)\n*---')


class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        """
        修改yaml dump之后列表缩进问题
        :param flow:
        :param indentless:
        :return:
        """
        return super(MyDumper, self).increase_indent(flow, False)


def del_front_matter(f):
    try:
        with open(f, 'r+', encoding='utf-8') as fp:
            content = fp.read()
            fp.seek(0)
            fp.truncate()
            fp.write(front_matter_regex.sub('', content))
    except UnicodeDecodeError:
        print("DEL file(%s) not decode" % f)


def load_front_matter(f):
    try:
        with open(f, 'r', encoding=encoding(f)) as fp:
            content = fp.read()
            front_matter_match = front_matter_regex.match(content)
            if front_matter_match:
                return yaml.safe_load(front_matter_match.group(1).strip())
            else:
                print("file(%s) not front matter" % f)
    except UnicodeDecodeError:
        print("LOAD file(%s) not decode" % f)
    return {}


def dump_front_matter(f, fm_dict):
    del_front_matter(f)
    try:
        with open(f, 'r+', encoding=encoding(f)) as fp:
            content = fp.read()
            fm_yaml = yaml.dump(fm_dict, sort_keys=False, Dumper=MyDumper, default_flow_style=False)
            fp.seek(0)
            fp.truncate()
            fp.write('---\n%s---' % fm_yaml)
            fp.write(content)
    except UnicodeDecodeError:
        print("DUMP file(%s) not decode" % f)


if __name__ == '__main__':
    # del_front_matter('D:/Workspace/HTML/VSCode/vue_blog/docs/_posts/**/*.md')
    md_files = glob.glob('D:/Workspace/HTML/VSCode/vue_blog/docs/_posts/**/*.md', recursive=True)
    for item in md_files:
        fm_dict = load_front_matter(item)
        fm_dict['title'] = '12121212'
        dump_front_matter(item, fm_dict)
