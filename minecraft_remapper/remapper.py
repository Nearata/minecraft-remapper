from pathlib import Path
from re import sub as re_sub
from shutil import copyfile, copytree, make_archive, move, rmtree

import typer


class Remapper:
    def __init__(self, input: str, output: str, mappings: str) -> None:
        self.input = Path().joinpath(input)
        self.output = Path().joinpath(output)
        self.mappings = Path(mappings)

    def __call__(self) -> None:
        self.__check_sources_path()
        self.__check_output_path()
        self.__check_mappings_path()

        src_path = self.output.joinpath("src")
        if not src_path.exists():
            src_path.mkdir()

        for i in self.input.glob("*"):
            if i.is_file():
                copyfile(i, src_path.joinpath(i.name))

            if i.is_dir():
                copytree(i, src_path.joinpath(i.name))

        files = list(self.output.joinpath("src").rglob("*.java"))

        for f in files:
            content = f.read_text()
            subs: list[dict[str, str]] = []

            for k, v in self.__read_tsrg(self.mappings).items():
                if k in content:
                    subs.append({"find": k, "replace": v})

            if subs:
                for s in subs:
                    f.write_text(
                        self.__apply_map(s["find"], s["replace"], f.read_text(), f.name)
                    )

        root_dir = self.output.joinpath("src")
        make_archive("sources", "zip", root_dir)
        rmtree(root_dir)
        move(str(Path().joinpath("sources.zip")), str(self.output))

        typer.echo(
            "\nConversion complete. A zip file has been created in the output folder."
        )

    def __check_sources_path(self) -> None:
        if not self.input.exists():
            self.__exit_script("The --input path does not exists.")

        if not self.input.is_dir():
            self.__exit_script("The --input path must be a directory.")

        if not list(self.input.glob("*")):
            self.__exit_script("The --input path directory is empty.")

        if not list(self.input.rglob("*.java")):
            self.__exit_script("No sources to remap.")

    def __check_output_path(self) -> None:
        if not self.output.exists():
            self.__exit_script("The --output path does not exists.")

        if not self.output.is_dir():
            self.__exit_script("The --output path must be a directory.")

        if list(self.output.glob("*")):
            self.__exit_script("The --output path directory is not empty.")

    def __check_mappings_path(self) -> None:
        if not self.mappings.exists():
            self.__exit_script("The --mappings file does not exists.")

        if not self.mappings.is_file():
            self.__exit_script("--mappings argument doesn't point to a file.")

    def __exit_script(self, message: str) -> None:
        typer.secho(f"[ERROR:] {message}", fg=typer.colors.BRIGHT_RED)
        raise typer.Abort()

    def __apply_map(self, find: str, replace: str, string: str, filename: str) -> str:
        typer.secho(
            f"[INFO:] {filename}: {find} >> {replace}", fg=typer.colors.BRIGHT_GREEN
        )
        return re_sub(find, replace, string)

    def __read_tsrg(self, file: Path) -> dict[str, str]:
        dct: dict[str, str] = {}

        with file.open() as f:
            lines = f.readlines()

        for l in lines:
            curr = l.strip().split(" ")

            if not curr[0].startswith(("f_", "field_", "m_", "func_")):
                continue

            if len(curr) < 3:
                curr.insert(1, "")

            dct[curr[0]] = curr[2]

        return dct
