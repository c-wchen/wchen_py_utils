import sys

import click
import getopt
import argparse


# 命令行
@click.command()
@click.option('--username', default='', prompt='Please input username: ')
@click.option('--password', default='', prompt='Please input password: ')
@click.option('--port', default=22, prompt='Please input port: ')
def cli1(username, password, port):
    print(username, password, port)


def cli2():
    """
    https://docs.python.org/zh-cn/3/library/getopt.html
    缺省参数 -h-a-f: => help all
    """
    opts, args = getopt.getopt(sys.argv[1:], '-h-a-f:', ['help', 'all', 'format='])
    for opt_key, opt_value in opts:
        if opt_key in ('-a', '--all'):
            print('show all info')
            sys.exit(0)
        elif opt_key in ('-h', '--help'):
            print('show help info')
            sys.exit(0)
        elif opt_key in ('-f', '--format'):
            print('format [%s]' % opt_value)
            sys.exit(0)
        else:
            print('arg err')
            sys.exit(0)


def cli3():
    """
    https://geek-docs.com/python/python-tutorial/python-argparse.html
    """
    parser = argparse.ArgumentParser(description='this is cli3 info')
    parser.add_argument('-o', '--output', dest='output', help='output file path')
    args = parser.parse_args()
    print(f'args {args}')


if __name__ == '__main__':
    cli1()
