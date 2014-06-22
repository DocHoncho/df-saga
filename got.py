import click
import os


class Repo(object):
    def __init__(self, home=None, debug=False):
        self.home = home or os.path.abspath(home or '.')
        self.debug = debug
pass_repo = click.make_pass_decorator(Repo)


@click.group()
@click.option('--repo-home', envvar='REPO', default='.repo')
@click.option('--debug/--no-debug', default=False, envvar='REPO_DEBUG')
@click.pass_context
def cli(ctx, repo_home, debug):
    ctx.obj = Repo(repo_home, debug)

@cli.group()
@click.option('-f', '--foo', envvar='FOO', default='bkasdfdsdfajbk')
@pass_repo
def frotz(repo, foo):
    print('Frotz said {}'.format(foo))


@frotz.command()
@pass_repo
def bloort(repo):
    print('Fuckin bloort!')


@cli.command()
@click.argument('src')
@click.argument('dest', required=False)
@pass_repo
def clone(repo, src, dest):
    print(repo, src, dest)
    pass


if __name__ == '__main__':
    cli()

