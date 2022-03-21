import click


# 命令行
@click.command()
@click.option('--username', default='', prompt='Please input username: ')
@click.option('--password', default='', prompt='Please input password: ')
@click.option('--port', default=22, prompt='Please input port: ')
def cli(username, password, port):
    print(username, password, port)


if __name__ == '__main__':
    cli()