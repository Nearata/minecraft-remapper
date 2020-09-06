from click import command as click_command
from click import option as click_option
from colorama import init as colorama_init
from colorama import Fore as colorama_fore

from minecraft_remapper import Remapper


def prompt(message: str) -> str:
    return f"{colorama_fore.LIGHTGREEN_EX}[Minecraft Remapper] {colorama_fore.LIGHTMAGENTA_EX + message + colorama_fore.LIGHTWHITE_EX}"

@click_command()
@click_option("-i", "--input", prompt=prompt("Input (Path to mod source files directory)"), type=str, required=True)
@click_option("-o", "--output", prompt=prompt("Output (Path to where you want to save the converted source code)"), type=str, required=True)
@click_option("-m", "--mappings", prompt=prompt("Mappings (The path where the script will find the mappings)"), type=str, required=True)
def main(input, output, mappings):
    remapper = Remapper(input, output, mappings)
    remapper()


if __name__ == "__main__":
    colorama_init()
    main()
