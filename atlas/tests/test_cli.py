"""The command line: the parser, the reference it generates, and the exit codes."""

from __future__ import annotations

import json

import pytest

from atlas.cli import run_argv
from atlas.cli.app import GROUPS, MODULES, build_parser, command_tree, render_reference
from atlas.errors import ExitCode


def test_every_command_is_in_exactly_one_group():
    grouped = [name for _title, names in GROUPS for name in names]
    assert sorted(grouped) == sorted(MODULES)
    assert len(grouped) == len(set(grouped))


def test_every_command_declares_a_summary_and_a_handler():
    for name, module in MODULES.items():
        assert module.SUMMARY and module.SUMMARY[0].islower(), name
        assert callable(module.run) and callable(module.configure)


def test_reference_matches_the_parser(root):
    generated = render_reference()
    on_disk = (root / "docs" / "reference" / "cli.md").read_text(encoding="utf-8")
    # The date line moves with regeneration; everything below it must not.
    assert generated.split("# CLI reference", 1)[1] == on_disk.split("# CLI reference", 1)[1]


def test_reference_documents_every_command(root):
    text = (root / "docs" / "reference" / "cli.md").read_text(encoding="utf-8")
    for name in MODULES:
        assert f"### `atlas {name}`" in text


def test_command_tree_is_data():
    tree = {entry["name"]: entry for entry in command_tree()}
    assert set(tree) == set(MODULES)
    assert tree["work"]["subcommands"]


def test_global_flags_work_in_either_order():
    parser = build_parser()
    assert parser.parse_args(["--json", "check"]).json_mode is True
    assert parser.parse_args(["check", "--json"]).json_mode is True


def test_directory_flag_survives_the_subparser(root):
    parser = build_parser()
    args = parser.parse_args(["-C", str(root), "check"])
    assert args.directory == str(root)


@pytest.mark.parametrize("argv", [["check"], ["status"], ["spec", "list"], ["lexicon", "list"]])
def test_commands_succeed_on_this_repository(root, argv):
    assert run_argv(["-C", str(root), *argv]) == ExitCode.OK


def test_json_output_is_parseable(root, capsys):
    run_argv(["-C", str(root), "--json", "check"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["summary"]["failed"] == 0


def test_not_a_repository_has_its_own_exit_code(tmp_path):
    assert run_argv(["-C", str(tmp_path), "check"]) == ExitCode.NOT_A_REPOSITORY


def test_unknown_check_is_not_found(root):
    assert run_argv(["-C", str(root), "check", "--only", "no-such-gate"]) == ExitCode.NOT_FOUND


def test_unknown_prompt_is_not_found(root):
    assert run_argv(["-C", str(root), "prompt", "show", "no-such-prompt"]) == ExitCode.NOT_FOUND


def test_bare_invocation_prints_help(capsys):
    assert run_argv([]) == ExitCode.OK
    assert "commands:" in capsys.readouterr().out


def test_prompt_show_prints_only_the_prompt(root, capsys):
    run_argv(["-C", str(root), "prompt", "show", "write-brief"])
    out = capsys.readouterr().out.strip()
    assert out.startswith("Write an editorial brief")
    assert "\n\n" not in out


def test_completion_scripts_render(root, capsys):
    for shell in ("bash", "zsh", "fish"):
        assert run_argv(["-C", str(root), "completion", shell]) == ExitCode.OK
    assert "atlas" in capsys.readouterr().out


def test_nested_subcommands_accept_global_flags(root, capsys):
    """`atlas spec rules --json` must work, not only `atlas --json spec rules`."""
    for argv in (
        ["spec", "rules", "--json"],
        ["--json", "spec", "rules"],
        ["work", "list", "--json"],
        ["prompt", "show", "write-brief", "--json"],
    ):
        assert run_argv(["-C", str(root), *argv]) == ExitCode.OK
        json.loads(capsys.readouterr().out)


def test_the_suite_defines_the_rules_the_docs_claim(root):
    from atlas.core import specs as specs_mod
    from atlas.paths import Repository

    rules = specs_mod.all_rules(Repository(root=root).spec_dir)
    assert len(rules) == 69


def test_output_counts_are_grammatical(root, capsys):
    """An editorial tool does not print "1 files"."""
    run_argv(["-C", str(root), "--no-color", "lint", "examples/needs-work.md"])
    out = capsys.readouterr().out
    assert "1 file" in out and "1 files" not in out

    run_argv(["-C", str(root), "--no-color", "check", "--only", "manifest-valid"])
    assert "1 gate passed" in capsys.readouterr().out


def test_lint_findings_state_their_severity(root, capsys):
    run_argv(["-C", str(root), "--no-color", "lint", "examples/needs-work.md"])
    out = capsys.readouterr().out
    assert "error" in out and "warn" in out
