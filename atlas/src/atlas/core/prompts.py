"""The prompt library: requests written once, then reused.

Every prompt is a plain text file under ``library/prompts/<stage>/<slug>.txt``.
The file is the original. ``library/prompts/index.yaml`` is generated from the
files by ``scripts/build_library.py``, so the catalogue cannot list a prompt
that does not exist, or miss one that does.

Three conventions hold, and they are checked:

* One request per prompt. A prompt that asks for three things gets one third of
  each.
* One to four sentences. Longer than that is a brief, and briefs live in ``work/``.
* Anything destructive proposes a plan first, so the reply is a diff to approve
  rather than a change to discover.
"""

from __future__ import annotations

import dataclasses
import pathlib
import typing as t

from ..errors import NotFoundError

__all__ = ["Prompt", "load_prompts", "find_prompt", "search_prompts", "stages", "build_index"]

MAX_SENTENCES = 4
#: Verbs that change files rather than producing text, and therefore mean a
#: prompt must propose before it acts. Asking for a rewritten *paragraph* in the
#: reply is not destructive; rewriting the file on disk is.
DESTRUCTIVE = ("delete", "overwrite", "purge", "archive", "retire ", "migrate", "drop")


@dataclasses.dataclass(frozen=True)
class Prompt:
    slug: str
    stage: str
    text: str
    path: pathlib.Path

    @property
    def summary(self) -> str:
        first = self.text.strip().split(". ")[0].strip()
        return first if first.endswith(".") else f"{first}."

    @property
    def sentences(self) -> int:
        return len([part for part in self.text.replace("\n", " ").split(". ") if part.strip()])

    @property
    def is_destructive(self) -> bool:
        lowered = self.text.lower()
        return any(verb in lowered for verb in DESTRUCTIVE)

    def as_dict(self, *, with_text: bool = False) -> dict[str, t.Any]:
        payload = {
            "slug": self.slug,
            "stage": self.stage,
            "summary": self.summary,
            "path": str(self.path.name),
        }
        if with_text:
            payload["text"] = self.text
        return payload


def load_prompts(prompts_dir: pathlib.Path) -> list[Prompt]:
    """Every prompt on disk, sorted by stage then slug."""
    if not prompts_dir.is_dir():
        return []
    found: list[Prompt] = []
    for path in sorted(prompts_dir.rglob("*.txt")):
        stage = path.parent.name
        found.append(
            Prompt(
                slug=path.stem.removeprefix("request-"),
                stage=stage,
                text=path.read_text(encoding="utf-8").strip(),
                path=path,
            )
        )
    return sorted(found, key=lambda p: (p.stage, p.slug))


def stages(prompts_dir: pathlib.Path) -> list[str]:
    return sorted({prompt.stage for prompt in load_prompts(prompts_dir)})


def find_prompt(prompts_dir: pathlib.Path, slug: str) -> Prompt:
    wanted = slug.strip().lower().removeprefix("request-").removesuffix(".txt")
    for prompt in load_prompts(prompts_dir):
        if prompt.slug.lower() == wanted:
            return prompt
    raise NotFoundError(
        f"no prompt named {slug!r}", hint="run `atlas prompt search <word>` to find one"
    )


def search_prompts(prompts_dir: pathlib.Path, query: str, *, stage: str | None = None) -> list[Prompt]:
    needle = query.strip().lower()
    results = []
    for prompt in load_prompts(prompts_dir):
        if stage and prompt.stage != stage:
            continue
        if not needle or needle in prompt.slug.lower() or needle in prompt.text.lower():
            results.append(prompt)
    return results


def build_index(prompts_dir: pathlib.Path) -> dict[str, t.Any]:
    """The catalogue, as data. Written to index.yaml by the build script."""
    prompts = load_prompts(prompts_dir)
    grouped: dict[str, list[dict[str, t.Any]]] = {}
    for prompt in prompts:
        grouped.setdefault(prompt.stage, []).append(
            {"slug": prompt.slug, "summary": prompt.summary, "file": prompt.path.name}
        )
    return {
        "generated_by": "scripts/build_library.py",
        "count": len(prompts),
        "stages": [
            {"name": stage, "count": len(items), "prompts": items}
            for stage, items in sorted(grouped.items())
        ],
    }
