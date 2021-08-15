import typer

from minecraft_remapper import Remapper


def main(i: str = typer.Option(...), o: str = typer.Option(...), m: str = typer.Option(...)) -> None:
    remapper = Remapper(i, o, m)
    remapper()


if __name__ == "__main__":
    typer.run(main)
