"""Print a shell completion script.

Generated from the parser tree rather than hand-written, so a new command is
completable the moment it exists.
"""

from __future__ import annotations

import argparse

from ...errors import ExitCode
from ...terminal import Console

SUMMARY = "print a shell completion script"

_BASH = """\
# atlas completion for bash. Install with:
#   atlas completion bash > /etc/bash_completion.d/atlas
_atlas_complete() {{
    local commands="{commands}"
    if [ "$COMP_CWORD" -eq 1 ]; then
        COMPREPLY=( $(compgen -W "$commands" -- "${{COMP_WORDS[1]}}") )
    fi
}}
complete -F _atlas_complete atlas
"""

_ZSH = """\
# atlas completion for zsh. Install with:
#   atlas completion zsh > "${{fpath[1]}}/_atlas"
#compdef atlas
_arguments '1:command:({commands})'
"""

_FISH = """\
# atlas completion for fish. Install with:
#   atlas completion fish > ~/.config/fish/completions/atlas.fish
{lines}
"""


def configure(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("shell", choices=("bash", "zsh", "fish"), help="which shell")


def run(args: argparse.Namespace, console: Console) -> int:
    from ..app import MODULES

    names = " ".join(MODULES)
    if args.shell == "bash":
        script = _BASH.format(commands=names)
    elif args.shell == "zsh":
        script = _ZSH.format(commands=" ".join(MODULES))
    else:
        lines = "\n".join(
            f"complete -c atlas -n __fish_use_subcommand -a {name} -d '{module.SUMMARY}'"
            for name, module in MODULES.items()
        )
        script = _FISH.format(lines=lines)
    print(script)
    return int(ExitCode.OK)
