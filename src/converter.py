import click
from CSVReader import CSVReader


@click.command()
@click.option('--csv', help='The ABSOLUTE PATH to the CSV')
def run(csv):
    print(csv)
    reader = CSVReader(csv)
    reader.run()


if __name__ == '__main__':
    run()
