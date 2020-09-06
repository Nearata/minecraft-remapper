from pathlib import Path
from re import sub
from csv import DictReader
from argparse import ArgumentParser
from shutil import copytree, copyfile, make_archive, rmtree, move
from sys import exit as exit_script


def apply_map(find, replace, string, filename):
    print(f"{filename}: {find} >> {replace}")
    return sub(find, replace, string)


def remapper(i, o, m):
    sources_path = Path().joinpath(i)
    output_path = Path().joinpath(o)
    maps_path = Path().joinpath(m)

    if not sources_path.exists():
        exit_script("The --input path does not exists.")

    if not sources_path.is_dir():
        exit_script("The --input path must be a directory.")

    if not list(sources_path.glob("*")):
        exit_script("The --input path directory is empty.")

    if not output_path.exists():
        exit_script("The --output path does not exists.")

    if not output_path.is_dir():
        exit_script("The --output path must be a directory.")

    if list(output_path.glob("*")):
        exit_script("The --output path directory is not empty.")

    if not maps_path.exists():
        exit_script("The --mappings path does not exists.")

    if not list(maps_path.glob("*.csv")):
        exit_script("The --mappings path directory is empty.")

    if not list(sources_path.rglob("*.java")):
        exit_script("No sources to remap.")

    src_path = output_path.joinpath("src")
    if not src_path.exists():
        src_path.mkdir()

    for i in sources_path.glob("*"):
        if i.is_file():
            copyfile(i, src_path.joinpath(i.name))

        if i.is_dir():
            copytree(i, src_path.joinpath(i.name))

    src_files = list(output_path.joinpath("src").rglob("*.java"))
    maps = list(maps_path.glob("*.csv"))

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

    root_dir = output_path.joinpath("src")
    make_archive("sources", "zip", root_dir)
    rmtree(root_dir)
    move(str(Path().joinpath("sources.zip")), str(output_path))

    print("\nConversion complete. A zip file has been created in the output folder.")


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

    remapper(args.input, args.output, args.mappings)


if __name__ == "__main__":
    main()
