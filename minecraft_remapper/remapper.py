from pathlib import Path
from re import sub
from csv import DictReader
from shutil import copytree, copyfile, make_archive, rmtree, move
from sys import exit as exit_script

from colorama import Fore as colorama_fore


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
                        self.__apply_map(i["searge"], i["name"], s.read_text(), s.name)
                    )

            if params:
                for i in params:
                    s.write_text(
                        self.__apply_map(i["param"], i["name"], s.read_text(), s.name)
                    )

        root_dir = self.output.joinpath("src")
        make_archive("sources", "zip", root_dir)
        rmtree(root_dir)
        move(str(Path().joinpath("sources.zip")), str(self.output))

        print("\nConversion complete. A zip file has been created in the output folder.")

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
            self.__exit_script("The --mappings path does not exists.")

        if not list(self.mappings.glob("*.csv")):
            self.__exit_script("The --mappings path directory is empty.")

    def __exit_script(self, message):
        exit_script(f"{colorama_fore.LIGHTRED_EX}[ERROR] {colorama_fore.LIGHTYELLOW_EX + message}")

    def __apply_map(self, find: str, replace: str, string: str, filename: str) -> str:
        print(f"{colorama_fore.LIGHTGREEN_EX}[Minecraft Remapper] {colorama_fore.LIGHTYELLOW_EX}{filename}: {colorama_fore.LIGHTWHITE_EX}{find} {colorama_fore.LIGHTCYAN_EX}>> {colorama_fore.LIGHTWHITE_EX}{replace}")
        return sub(find, replace, string)
