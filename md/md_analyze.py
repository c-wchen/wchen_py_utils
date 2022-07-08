#!/bin/bash
import os.path
import pathlib
import pprint
import re
from file import encoding, replace_content
import glob
import json
from enum import Enum


class TypeMdLink(Enum):
    HTTP = 0
    ASSETS = 1
    ABS_PATH = 2
    REL_PATH = 3


def fetch_md_images_link(f_path):
    # 通过f_path获取文件的图片链接
    regex_link = '!\[.*?\]\((.*)\)'
    with open(f_path, 'r+', encoding=encoding(f_path)) as fp:
        context = fp.read()
    return re.findall(regex_link, context)


def organize_to_mds():
    # 将所有文件中图片链接提取下来
    files = glob.glob(r"D:\Documents\Typora\**\*.md", recursive=True)
    mds = []
    for f_path in files:
        res = fetch_md_images_link(f_path)
        if len(res) > 0:
            mds.append({
                'f_path': f_path,
                'links': res
            })
    return pre_links(mds)


def pre_links(mds):
    for md in mds:
        """
        以下路径情况说明
            1. assets开头
            2. http开头
            3. ./开头
            4. 绝对路径
            5. 相对路径非assets开头
        """
        for img_link in md['links']:
            links = []
            if img_link.startswith("assets/"):
                links.append({
                    'type': TypeMdLink.ASSETS,
                    'img_link': img_link
                })
            elif img_link.startswith('http'):
                links.append({
                    'type': TypeMdLink.HTTP,
                    'img_link': img_link
                })
            elif os.path.isabs(img_link):
                links.append({
                    'type': TypeMdLink.ABS_PATH,
                    'img_link': img_link
                })
            else:
                links.append({
                    'type': TypeMdLink.REL_PATH,
                    'img_link': img_link
                })
            md['links'] = links
    return mds


if __name__ == '__main__':
    mds = organize_to_mds()
    pprint.pprint(mds)
    #  将所有文件图片归档到assets中

    # 提取所有网络链接到本地

    # 归并之后删除所有无用链接
