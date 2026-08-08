"""The CLI surface: parsing, exit codes, JSON output, and generated docs.

These tests exercise `main()` with argument lists rather than spawning
subprocesses. That keeps them fast enough to run on every save, and it means a
failure points at a line of Python rather than at a shell invocation.
"""

from __future__ import annotations

import io
import json
import pathlib

import pytest

from atlas import STANDARDS, __version__
from atlas.cli import main
from atlas.cli.app import build_parser, command_tree, render_reference
from atlas.core import specs as specs_mod
from atlas.errors import ExitCode

ROOT = pathlib.Path(__file__).resolve().parent.parent


def run(*argv: str, capsys=None) -> tuple[int, str]:
    """Invoke the CLI, returning its exit code and stdout."""
    buffer = io.StringIO()
    import contextlib

    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(io.StringIO()):
        code = main(["-C", str(ROOT), *argv])
    return code, buffer.getvalue()


# --------------------------------------------------------------------- basics

def test_help_exits_cleanly():
    with pytest.raises(SystemExit) as exit_info:
        main(["--help"])
    assert exit_info.value.code == 0


def test_version_matches_package():
    with pytest.raises(SystemExit):
        main(["--version"])
    assert __version__.count(".") == 2, "version must be SemVer"


def test_no_command_prints_help_and_succeeds():
    code, out = run()
    assert code == ExitCode.OK
    assert "atlas init" in out


def test_unknown_command_is_a_usage_error():
    with pytest.raises(SystemExit) as exit_info:
        main(["definitely-not-a-command"])
    assert exit_info.value.code == 2


# ---------------------------------------------------------------- exit codes

def test_check_passes_on_this_repository():
    """The suite is self-hosting: it must pass its own standard."""
    code, _ = run("check")
    assert code == ExitCode.OK


def test_missing_workstream_exits_not_found():
    code, _ = run("work", "show", "does-not-exist")
    assert code == ExitCode.NOT_FOUND


def test_outside_a_repository_exits_no_repository(tmp_path):
    import contextlib

    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        code = main(["-C", str(tmp_path), "status"])
    assert code == ExitCode.NO_REPOSITORY


def test_unknown_check_id_is_a_usage_error():
    code, _ = run("check", "--only", "no-such-gate")
    assert code == ExitCode.USAGE


# ---------------------------------------------------------------- json output

@pytest.mark.parametrize(
    "argv",
    [
        ("check",),
        ("status",),
        ("doctor",),
        ("spec", "list"),
        ("work", "list"),
        ("prompt", "categories"),
        ("library", "list"),
        ("template", "list"),
        ("validate", "--all"),
    ],
)
def test_json_output_is_valid_json(argv):
    """Every read command must emit parseable JSON under --json.

    Agents consume this; a command that prints a stray human line into the JSON
    stream breaks them silently.
    """
    code, out = run(*argv, "--json")
    assert code in (ExitCode.OK, ExitCode.FAILURE)
    parsed = json.loads(out)
    assert isinstance(parsed, (dict, list))


def test_check_json_reports_every_gate():
    _, out = run("check", "--json")
    payload = json.loads(out)
    from atlas.core import compliance

    assert {c["id"] for c in payload["checks"]} == set(compliance.check_ids())
    assert payload["ok"] is True


def test_quiet_suppresses_human_output():
    _, out = run("check", "--quiet")
    assert out.strip() == ""


# --------------------------------------------------------------- the tree

def test_every_command_has_a_description():
    """`--help` and the generated reference both read from these."""
    missing = [path for path, summary, _ in command_tree() if not summary]
    assert not missing, f"commands without a description: {missing}"


def test_every_subcommand_group_has_a_default_handler():
    """`atlas work` with no subcommand must do something useful, not crash."""
    for group in ("work", "spec", "prompt", "library", "template", "site"):
        code, _ = run(group)
        assert code == ExitCode.OK, f"`atlas {group}` with no subcommand failed"


def test_global_flags_accepted_before_and_after_the_subcommand():
    before, _ = run("--json", "spec", "list")
    after, _ = run("spec", "list", "--json")
    assert before == after == ExitCode.OK


def test_parser_builds_without_a_repository():
    """`atlas --help` must work outside a repository."""
    assert build_parser().prog == "atlas"


# ------------------------------------------------------- generated reference

def test_committed_cli_reference_is_current():
    """The reference is generated; a stale committed copy is a broken contract."""
    committed = (ROOT / "docs" / "reference" / "cli.md").read_text(encoding="utf-8")
    assert committed == render_reference(), (
        "docs/reference/cli.md is stale — run `atlas site build --write-reference`"
    )


def test_reference_documents_every_command():
    reference = render_reference()
    for path, _, _ in command_tree():
        assert f"`atlas {path}`" in reference, f"{path} is missing from the reference"


# ------------------------------------------------------------- completions

@pytest.mark.parametrize("shell", ["bash", "zsh", "fish"])
def test_completion_scripts_generate_and_mention_every_top_level_command(shell):
    code, out = run("completion", shell)
    assert code == ExitCode.OK
    top_level = [p for p, _, _ in command_tree() if " " not in p]
    for command in top_level:
        assert command in out, f"{shell} completion omits `{command}`"


# ------------------------------------------------------------------ metadata

def test_declared_standards_match_the_spec_directory():
    """The hard-coded tuple exists for use without a repository; keep it honest."""
    on_disk = {spec.id for spec in specs_mod.load_specs(ROOT / "spec")}
    assert set(STANDARDS) == on_disk
