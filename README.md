# Minecraft Remapper

> A Minecraft remapper for already deobfuscated source code.

## Requirements

- Python 3.8

## Installation

```sh
pip install minecraft-remapper
```

## Usage

```sh
python -m mc_remapper
```

or

```sh
python -m mc_remapper -i <input_directory> -o <output_directory> -m <mappings_directory>
```

## Parameters

- `-i` / `--input`: Path to deobfuscated and decompiled mod source code.
- `-o` / `--output`: Path to an existing directory where the script will save the source code remapped in a zip file named `sources.zip`.
- `-m` / `--mappings`: Path to mcp mappings folder (`fields.csv`, `methods.csv` and `params.csv`).

## License

Distributed under the MIT license. See `LICENSE` for more information.

## Contributing

1. Fork it
2. Commit your changes
3. Push to the branch
4. Create a new Pull Request
