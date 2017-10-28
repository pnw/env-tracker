import click

@click.group()
def et():
    click.echo('Running an et command!!')

@et.command()
def init():
    click.echo('Running init command')

@et.command()
def track():
    click.echo('Running track command')

@et.command()
def untrack():
    click.echo('Running untrack command')
