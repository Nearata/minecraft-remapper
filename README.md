# Minecraft Remapper

> A Minecraft remapper for already deobfuscated source code.

## Requirements

- Python >=3.9

## Installation

```sh
pip install minecraft-remapper
```

## Usage

```sh
python -m minecraft_remapper --i <text> --o <text> --m <text>
```

### Example

```sh
python -m minecraft_remapper --i input_folder --o output_folder --m mappings_file.tsrg
```

## Parameters

- `--i`: Path to deobfuscated and decompiled mod source code.
- `--o`: Path to an existing directory where the script will save the source code remapped in a zip file named `sources.zip`.
- `--m`: Path to mappings file (`<filename>.tsrg`)

## Unlicense

See [UNLICENSE](UNLICENSE) for details.
