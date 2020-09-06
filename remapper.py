from pathlib import Path
from re import sub
from csv import DictReader
from argparse import ArgumentParser
from shutil import copytree, copyfile, make_archive, rmtree, move
from sys import exit as exit_script


def apply_map(find, replace, string, filename):
    print(f"{filename}: {find} >> {replace}")
    return sub(find, replace, string)


class Remapper:
    def __init__(self, i, o, m) -> None:
        self.input = Path().joinpath(i)
        self.output = Path().joinpath(o)
        self.mappings = Path().joinpath(m)

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

        src_files = list(self.output.joinpath("src").rglob("*.java"))
        maps = list(self.mappings.glob("*.csv"))

        for s in src_files:
            file_src = s.read_text()
            searges = []
            params = []

            for m in maps:
                with m.open() as csv:
                    csv_content = DictReader(csv)

                    for row in csv_content:
                        if "searge" in row and row["searge"] in file_src:
                                searges.append({
                                    "searge": row["searge"],
                                    "name": row["name"]
                                })
                        if "param" in row and row["param"] in file_src:
                                params.append({
                                    "param": row["param"],
                                    "name": row["name"]
                                })

            if searges:
                for i in searges:
                    s.write_text(
                        apply_map(i["searge"], i["name"], s.read_text(), s.name)
                    )

            if params:
                for i in params:
                    s.write_text(
                        apply_map(i["param"], i["name"], s.read_text(), s.name)
                    )

        root_dir = self.output.joinpath("src")
        make_archive("sources", "zip", root_dir)
        rmtree(root_dir)
        move(str(Path().joinpath("sources.zip")), str(self.output))

        print("\nConversion complete. A zip file has been created in the output folder.")

    def __check_sources_path(self) -> None:
        if not self.input.exists():
            exit_script("The --input path does not exists.")

        if not self.input.is_dir():
            exit_script("The --input path must be a directory.")

        if not list(self.input.glob("*")):
            exit_script("The --input path directory is empty.")

        if not list(self.input.rglob("*.java")):
            exit_script("No sources to remap.")

    def __check_output_path(self) -> None:
        if not self.output.exists():
            exit_script("The --output path does not exists.")

        if not self.output.is_dir():
            exit_script("The --output path must be a directory.")

        if list(self.output.glob("*")):
            exit_script("The --output path directory is not empty.")

    def __check_mappings_path(self) -> None:
        if not self.mappings.exists():
            exit_script("The --mappings path does not exists.")

        if not list(self.mappings.glob("*.csv")):
            exit_script("The --mappings path directory is empty.")


def main():
    arg_parser = ArgumentParser(
        "Minecraft Remapper",
        description="Remap a deobfuscated minecraft mod code."
    )

    arg_parser.add_argument(
        "--input", "-i",
        help="Path to mod source files directory.",
        required=True
    )
    arg_parser.add_argument(
        "--output", "-o",
        help="Path to where you want to save the converted source code.",
        required=True, default=""
    )
    arg_parser.add_argument(
        "--mappings", "-m",
        help="Path to where the program can find mappings.",
        required=True
    )

    args = arg_parser.parse_args()

    remapper = Remapper(args.input, args.output, args.mappings)
    remapper()


if __name__ == "__main__":
    main()
