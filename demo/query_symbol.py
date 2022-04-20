import os
import click

ELF_FORMAT = ['.so', '.a', '.o']


def query_symbol(file, symbol):
    if os.path.isdir(file):
        for item in os.listdir(file):
            query_symbol(os.path.join(file, item), symbol)
    if os.path.isfile(file):
        suffix = os.path.splitext(file)[-1]
        if suffix in ELF_FORMAT:
            out = os.popen('nm -A {file} | grep "T {symbol}"'.format(file=file, symbol=symbol))
            with out:
                for item in out.readlines():
                    print(item[0:-1])


@click.command()
@click.option('--file', '-f', default='.', prompt='Please input file path: ')
@click.option('--symbol', '-s', prompt='Please input symbol: ')
def cli(file, symbol):
    query_symbol(file, symbol)


if __name__ == '__main__':
    cli()