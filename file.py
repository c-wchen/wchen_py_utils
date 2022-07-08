import os
import shutil
import pathlib
import chardet


# 静默创建文件夹
def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


#  删除文件目录
def remove_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=False)


# 递归遍历文件夹
def iter_dir(path, callback):
    for file in os.listdir(path):
        cur_path = os.path.join(path, file)
        if os.path.isdir(cur_path):
            iter_dir(cur_path, callback)
        else:
            callback(file)


# 解压
def extract(path):
    ext_map = {
        'zip': '.zip',
        'tar': '.tar',
        'gztar': '.tar.gz',
        'bztar': '.tar.bz'
    }
    if os.path.exists(path) and os.path.isfile(path):
        ext = ''.join(pathlib.Path(path).suffixes)
        extract_dir = path[0:-len(ext)]
        if ext not in ext_map.values():
            print("file does not conform to the format (.zip, .tar.gz, .tar.bz, .tar), cur format = {}".format(ext))
        else:
            os.makedirs(extract_dir)
            shutil.unpack_archive(path, extract_dir)


# 获取文件编码
def encoding(path):
    # 二进制方式读取，获取字节数据，检测类型
    with open(path, 'rb') as f:
        return chardet.detect(f.read())['encoding']


# 替换文件中内容
def replace_content(file, src_str, dest_str):
    content = ""
    with open(file=file, mode='r+', encoding=encoding(file)) as fp:
        for line in fp.readlines():
            line = line.replace(src_str, dest_str)
            content += line
        fp.seek(0)
        fp.truncate(0)
        fp.write(content)
