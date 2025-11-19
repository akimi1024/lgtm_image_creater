import click

@click.command()
def cli():
  """LGTM画像生成ツール
  """
  lgtm()
  click.echo('lgtm')


def lgtm():
  pass