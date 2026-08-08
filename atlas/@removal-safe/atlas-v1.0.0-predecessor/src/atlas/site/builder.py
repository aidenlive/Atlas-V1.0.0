"""The site builder.

The site is *derived*: build output, gitignored, rebuilt in CI, never edited. If
it disagrees with the Markdown, the Markdown wins and the site is stale.

The build is one pass with a shared navigation model, so every page carries the
same sidebar, the same breadcrumbs, and correctly ordered previous/next links.
Building navigation per-page is how a documentation site ends up with three
different sidebars depending on which section you entered from.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import html
import pathlib
import re
import shutil
import typing as t

from .. import NAME, TAGLINE, __version__
from ..core import library as library_mod
from ..core import prompts as prompts_mod
from ..core import specs as specs_mod
from ..core import tokens as tokens_mod
from ..core import workstream as workstream_mod
from ..core.manifest import load_yaml
from ..paths import Repository
from . import search
from .layout import MARK_SVG, NavGroup, NavItem, Page, render_page
from .markdown import render, status_pill
from .theme import STYLESHEET

__all__ = ["BuildResult", "build"]

NAV_ITEMS = (
    ("spec/index.html", "Standards"),
    ("work/index.html", "Work"),
    ("docs/index.html", "Docs"),
    ("library/index.html", "Library"),
    ("cli/index.html", "CLI"),
)

FAVICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
    'stroke="#111" stroke-width="1.9" stroke-linejoin="round">'
    '<rect width="24" height="24" rx="5" fill="#fff" stroke="none"/>'
    '<path d="M12 4 4 8l8 4 8-4-8-4Z"/><path d="M4 12.5 12 16.5l8-4"/>'
    '<path d="M4 16.5 12 20.5l8-4"/></svg>'
)

DOC_SECTION_LABELS = {
    "reference": "Reference",
    "guides": "Guides",
    "architecture": "Architecture",
    "decisions": "Decisions",
}
#: Reading order for documentation sections: orient, then do, then understand.
DOC_SECTION_ORDER = ("reference", "guides", "architecture", "decisions")


#: What each workstream section is for. The skeleton is fixed by WORKSTREAM, so
#: these can be stated once rather than left to twelve near-empty generated
#: pages that show a file list and nothing else. A reader who lands on
#: `05_research/` should learn what belongs there without opening the standard.
SECTION_INTROS: dict[str, tuple[str, str]] = {
    "01_plan": ("Plan",
        "The approach and its milestones: what this workstream is changing, how, "
        "and by when. Written before the work starts and revised in the open."),
    "02_tasks": ("Tasks",
        "The canonical tracker. Every row carries an id, an owner, a status, and "
        "evidence once it is done. Progress on the dashboard is counted from this "
        "table, never asserted separately."),
    "03_requirements": ("Requirements",
        "What has to be true for this workstream to close, and the sources it "
        "draws on. Each requirement is stated so that someone else could check it."),
    "04_decisions": ("Decisions",
        "Choices made inside this workstream, with the options considered and the "
        "consequences accepted. Repository-wide decisions belong in docs/decisions/ "
        "as ADRs instead."),
    "05_research": ("Research",
        "Findings that shaped the plan: audits, measurements, and prior art. Dated, "
        "so a later reader can tell what was known at the time."),
    "06_deliverables": ("Deliverables",
        "What this workstream actually produced, and where it lives. Links to the "
        "artifacts rather than copies of them."),
    "07_validation": ("Validation",
        "Acceptance criteria and the evidence against each one: what was checked, "
        "by whom, when, and what the result was. An unattributed checkmark is not "
        "evidence."),
    "08_agents": ("Agents",
        "Who and what worked here. Assignments name each agent's role and scope; "
        "handoffs and logs record what was passed on. A handoff that exists only "
        "in a chat log did not happen."),
    "09_issues": ("Issues",
        "Open issues, blockers, and risks, with an owner and a severity for each. "
        "Kept with the work rather than in a separate tracker."),
    "handoffs": ("Handoffs",
        "One file per handoff: what was done, what was left, and what the next "
        "person needs to decide."),
    "logs": ("Logs",
        "Run notes kept for the next reader, not transcripts. Only the entries "
        "that would change someone's decisions."),
}


@dataclasses.dataclass
class BuildResult:
    pages: int
    out: pathlib.Path
    indexed: int
    warnings: list[str] = dataclasses.field(default_factory=list)


#: URL prefix to content domain. The accent for every surface follows from
#: this one mapping, so a page cannot be styled as one section while living in
#: another.
DOMAINS = (
    ("spec/", "spec"),
    ("work/", "work"),
    ("docs/", "docs"),
    ("library/", "library"),
    ("cli/", "cli"),
)


def _domain_of(url: str) -> str:
    for prefix, name in DOMAINS:
        if url.startswith(prefix):
            return name
    return ""


@dataclasses.dataclass
class Emitted:
    """One page, recorded so the sitemap and pager can be built afterwards."""

    url: str
    title: str


class Builder:
    def __init__(self, repo: Repository, out: pathlib.Path) -> None:
        self.repo = repo
        self.out = out
        self.index = search.Index()
        self.emitted: list[Emitted] = []
        self.warnings: list[str] = []
        self.build_date = dt.date.today().isoformat()
        self.specs = specs_mod.load_specs(repo.spec)
        self.workstreams = (
            workstream_mod.load_all(repo) if repo.has_workstreams() else []
        )
        self.docs = self._collect_docs()
        self.catalog = self._load_catalog()
        self.nav = self._build_nav()
        self.site_name = self._site_name()
        self.repository_url = self._repository_url()

    # ------------------------------------------------------------- discovery
    def _site_name(self) -> str:
        if self.repo.manifest.exists():
            data = load_yaml(self.repo.manifest) or {}
            return str(data.get("name") or NAME)
        return NAME

    def _repository_url(self) -> str:
        if self.repo.manifest.exists():
            data = load_yaml(self.repo.manifest) or {}
            metadata = data.get("metadata") or {}
            return str(metadata.get("website") or (data.get("links") or {}).get("tracker") or "#")
        return "#"

    def _collect_docs(self) -> list[pathlib.Path]:
        if not self.repo.docs.is_dir():
            return []
        found = [p for p in self.repo.docs.rglob("*.md") if p.is_file()]

        def key(path: pathlib.Path) -> tuple[int, str]:
            section = path.parent.name
            rank = (
                DOC_SECTION_ORDER.index(section)
                if section in DOC_SECTION_ORDER
                else len(DOC_SECTION_ORDER)
            )
            return (rank, path.stem)

        return sorted(found, key=key)

    def _load_catalog(self) -> prompts_mod.Catalog | None:
        if not (self.repo.prompts / "index.yaml").exists():
            return None
        try:
            return prompts_mod.load(self.repo)
        except Exception as exc:  # noqa: BLE001 - a broken catalog must not kill the build
            self.warnings.append(f"prompt catalog unreadable: {exc}")
            return None

    # -------------------------------------------------------------- navigation
    def _build_nav(self) -> list[NavGroup]:
        groups: list[NavGroup] = []

        if self.specs:
            groups.append(
                NavGroup(
                    "Standards",
                    [NavItem("spec/index.html", "Overview")]
                    + [
                        NavItem(f"spec/{spec.path.stem}.html", spec.title, number=str(spec.order))
                        for spec in self.specs
                    ],
                )
            )

        if self.workstreams:
            live = [w for w in self.workstreams if not w.archived]
            groups.append(
                NavGroup(
                    "Work",
                    [NavItem("work/index.html", "Dashboard")]
                    + [
                        NavItem(
                            f"work/{w.name}/index.html",
                            w.title,
                            number=w.id,
                            status=w.status,
                        )
                        for w in live
                    ],
                )
            )

        if self.docs:
            items = [NavItem("docs/index.html", "Overview")]
            for path in self.docs:
                items.append(NavItem(self._doc_url(path), self._doc_title(path)))
            groups.append(NavGroup("Documentation", items))

        library_items = [NavItem("library/index.html", "Overview")]
        if self.catalog:
            library_items.append(NavItem("library/prompts/index.html", "Prompts"))
            library_items += [
                NavItem(f"library/prompts/{c.name}/index.html", c.name.capitalize())
                for c in self.catalog.categories
            ]
        groups.append(NavGroup("Library", library_items))

        groups.append(
            NavGroup(
                "CLI",
                [
                    NavItem("cli/index.html", "Overview"),
                    NavItem("cli/reference.html", "Command reference"),
                ],
            )
        )
        return groups

    # ------------------------------------------------------------------ paths
    @staticmethod
    def _doc_url(path: pathlib.Path) -> str:
        return f"docs/{path.parent.name}/{path.stem}.html"

    @staticmethod
    def _doc_title(path: pathlib.Path) -> str:
        match = re.search(r"^#\s+(.+)$", path.read_text(encoding="utf-8"), re.M)
        if match:
            return re.sub(r"[`*]", "", match.group(1)).strip()
        stem = re.sub(r"^\d{4}-", "", path.stem).replace("-", " ")
        return stem[:1].upper() + stem[1:]

    # ------------------------------------------------------------------ emit
    def emit(
        self,
        url: str,
        title: str,
        markdown: str,
        *,
        subtitle: str = "",
        breadcrumbs: t.Sequence[tuple[str, str]] = (),
        prev: tuple[str, str] | None = None,
        next: tuple[str, str] | None = None,
        meta: t.Sequence[str] = (),
        link_rules: bool = False,
        index_it: bool = True,
        derived_note: bool = True,
        crumb_label: str = "",
        domain: str = "",
        eyebrow: str = "",
        tags: t.Sequence[str] = (),
    ) -> None:
        """Render one page from Markdown and record it."""
        # The shell renders the title; a leading H1 in the source would show it
        # twice at two different sizes.
        body_source = re.sub(r"\A(?:<!--.*?-->\s*)?#\s+.*?\n", "", markdown, count=1, flags=re.S)
        document = render(body_source, link_rules=link_rules)
        body = document.html
        # .page-head already draws a rule; a leading one renders as two lines
        # with nothing between them.
        body = re.sub(
            r'\A(<span[^>]*class="anchor-only"[^>]*></span>)?\s*<hr\s*/?>',
            lambda m: m.group(1) or "",
            body,
            count=1,
        )

        rel = pathlib.Path(url)
        page = Page(
            title=title,
            body=body,
            headings=[(h.level, h.slug, h.text) for h in document.headings],
            subtitle=subtitle,
            depth=len(rel.parent.parts) if rel.parent != pathlib.Path(".") else 0,
            breadcrumbs=list(breadcrumbs),
            nav=self.nav,
            active=url,
            prev=prev,
            next=next,
            meta=list(meta),
            derived_note=derived_note,
            domain=domain or _domain_of(url),
            eyebrow=eyebrow,
            tags=list(tags),
        )
        destination = self.out / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            render_page(
                page,
                site_name=self.site_name,
                tagline=TAGLINE,
                nav_items=NAV_ITEMS,
                repository_url=self.repository_url,
                build_date=self.build_date,
                version=f"v{__version__}",
            ),
            encoding="utf-8",
        )
        self.emitted.append(Emitted(url, title))
        if index_it:
            self.index.add(
                url,
                title,
                crumb=crumb_label or (breadcrumbs[0][0] if breadcrumbs else ""),
                headings=[h.text for h in document.headings],
                body=document.text,
            )

    # ============================================================= the sections
    def build_home(self) -> None:
        live = [w for w in self.workstreams if not w.archived]
        cards = "".join(
            f'<a class="card card-domain" data-domain="work" href="work/{w.name}/index.html">'
            f'<span class="card-eyebrow">Workstream {html.escape(w.id)}</span>'
            f"<h3>{html.escape(w.title)}</h3>"
            f"<p>{html.escape(w.summary)}</p>"
            f'<div class="card-meta">{status_pill(w.status)}'
            f'<div class="progress-track"><span style="width:{w.percent}%"></span></div>'
            f'<span class="progress-count">{w.done}/{w.total}</span></div></a>'
            for w in live
        )
        work_section = (
            f'## Live work\n\n<div class="cards">{cards}</div>\n'
            if cards
            else '## Live work\n\n<div class="empty-state"><p>No live workstreams. '
            "Open one with <code>atlas work new &lt;slug&gt;</code>.</p></div>\n"
        )

        spec_cards = "".join(
            f'<a class="card card-domain" data-domain="spec" href="spec/{spec.path.stem}.html">'
            f'<span class="card-eyebrow">{spec.order:02d} · {html.escape(spec.id)}</span>'
            f"<h3>{html.escape(spec.title)}</h3>"
            f'<p class="card-question">{html.escape(spec.question)}</p>'
            f'<div class="card-meta">{status_pill(spec.status)}'
            f'<span class="tag">v{html.escape(spec.version)}</span></div></a>'
            for spec in self.specs
        )

        stats = "".join(
            f'<div class="stat"><span class="stat-value">{value}</span>'
            f'<span class="stat-label">{html.escape(label)}</span></div>'
            for value, label in (
                (len(self.specs), "standards"),
                (len(live), "live workstreams"),
                (len(self.catalog.prompts) if self.catalog else 0, "prompts"),
                (len(self.docs), "documents"),
            )
        )

        home = f"""# {self.site_name}

<div class="hero">
<p class="dek">Eight short specifications state what must be true about a piece of
work. One command checks a repository against all of them and prints what is missing.</p>
<div class="hero-actions">
<a class="btn btn-primary" href="docs/guides/install.html">Get started</a>
<a class="btn btn-secondary" href="spec/index.html">Read the standards</a>
</div>
</div>

<div class="stat-row">{stats}</div>

## The eight standards

<div class="cards">{spec_cards}</div>

{work_section}

## Start here

- [Install and first run](docs/guides/install.md): the CLI in five minutes
- [Glossary](docs/reference/glossary.md): every term in plain language, no code assumed
- [Command reference](cli/reference.md): every `atlas` command and flag
- [Work dashboard](work/index.md): every initiative, its owner, its progress
"""
        self.emit(
            "index.html",
            self.site_name,
            home,
            subtitle=f"{TAGLINE}.",
            derived_note=False,
            crumb_label="Home",
        )

    def build_specs(self) -> None:
        if not self.specs:
            return
        rows = "\n".join(
            f"| [{spec.title}]({spec.path.stem}.md) | {spec.question} | `{spec.version}` | {spec.status} |"
            for spec in self.specs
        )
        self.emit(
            "spec/index.html",
            "Standards",
            "# Standards\n\nThe prose here is the standard. The JSON Schemas in "
            "`spec/schemas/` encode the parts a machine can check, and a set of consistency "
            "tests compares the two, so a value added to one has to be added to the other.\n\n"
            "| Standard | Answers | Version | Status |\n|---|---|---|---|\n" + rows + "\n",
            subtitle=f"{len(self.specs)} specifications. Each is versioned, and CI checks "
            f"every repository against them.",
            eyebrow="The standard",
            breadcrumbs=[("Standards", "spec/index.html")],
            crumb_label="Standards",
        )
        for i, spec in enumerate(self.specs):
            prev = (
                (self.specs[i - 1].title, f"spec/{self.specs[i - 1].path.stem}.html")
                if i
                else None
            )
            nxt = (
                (self.specs[i + 1].title, f"spec/{self.specs[i + 1].path.stem}.html")
                if i + 1 < len(self.specs)
                else None
            )
            meta = [
                status_pill(spec.status),
                f'<span class="pill">v{html.escape(spec.version)}</span>',
            ]
            if spec.companions:
                meta.append(
                    f'<span class="pill">{len(spec.companions)} companions</span>'
                )
            self.emit(
                f"spec/{spec.path.stem}.html",
                spec.title,
                spec.path.read_text(encoding="utf-8"),
                eyebrow=f"Standard {spec.order:02d} of {len(self.specs)}",
                tags=[f"{spec.id} {spec.version}"] + [f"with {c}" for c in spec.companions],
                subtitle=spec.tagline,
                breadcrumbs=[("Standards", "spec/index.html"), (spec.title, "")],
                prev=prev,
                next=nxt,
                meta=meta,
                link_rules=True,
                crumb_label="Standards",
            )

    def build_docs(self) -> None:
        if not self.docs:
            return
        sections: dict[str, list[pathlib.Path]] = {}
        for path in self.docs:
            sections.setdefault(path.parent.name, []).append(path)
        body = ["# Documentation", ""]
        for name in [*DOC_SECTION_ORDER, *sorted(set(sections) - set(DOC_SECTION_ORDER))]:
            if name not in sections:
                continue
            body += [f"## {DOC_SECTION_LABELS.get(name, name.capitalize())}", ""]
            body += [
                f"- [{self._doc_title(p)}]({p.parent.name}/{p.stem}.md)" for p in sections[name]
            ]
            body.append("")
        self.emit(
            "docs/index.html",
            "Documentation",
            "\n".join(body),
            subtitle="Guides, reference, architecture, and the decision record.",
            eyebrow="Documentation",
            breadcrumbs=[("Docs", "docs/index.html")],
            crumb_label="Docs",
        )
        for i, path in enumerate(self.docs):
            prev = (
                (self._doc_title(self.docs[i - 1]), self._doc_url(self.docs[i - 1]))
                if i
                else None
            )
            nxt = (
                (self._doc_title(self.docs[i + 1]), self._doc_url(self.docs[i + 1]))
                if i + 1 < len(self.docs)
                else None
            )
            section = DOC_SECTION_LABELS.get(path.parent.name, path.parent.name.capitalize())
            self.emit(
                self._doc_url(path),
                self._doc_title(path),
                path.read_text(encoding="utf-8"),
                eyebrow=section,
                breadcrumbs=[("Docs", "docs/index.html"), (section, ""), (self._doc_title(path), "")],
                prev=prev,
                next=nxt,
                crumb_label=f"Docs / {section}",
            )

    def build_library(self) -> None:
        classes = library_mod.load(self.repo)
        rows = "\n".join(
            f"| {c.name.capitalize()} | {c.holds} | {c.count if c.present else '—'} |"
            for c in classes
        )
        body = [
            "# Library",
            "",
            "Things written once and used many times, in four kinds. That list is closed: "
            "adding a fifth means amending the specification, which is the difference between "
            "a library and a second downloads folder.",
            "",
            "| Class | Holds | Assets |",
            "|---|---|---|",
            rows,
            "",
            "Every asset lives in exactly one place, appears in its index, and is named for "
            "what it is rather than where it came from. Anything derived from another asset, or "
            "brought in from outside, also carries its source and its license.",
            "",
        ]
        if self.catalog:
            body += [
                "## Prompt categories",
                "",
                "| Category | Prompts | Covers |",
                "|---|---|---|",
                *[
                    f"| [{c.name}](prompts/{c.name}/index.md) | {len(c.prompts)} | {c.description} |"
                    for c in self.catalog.categories
                ],
                "",
            ]
        self.emit(
            "library/index.html",
            "Library",
            "\n".join(body),
            subtitle="Prompts, icons, typefaces, and media, each versioned and checked.",
            eyebrow="Shared assets",
            breadcrumbs=[("Library", "library/index.html")],
            crumb_label="Library",
        )

        if not self.catalog:
            return

        readme = self.repo.prompts / "README.md"
        self.emit(
            "library/prompts/index.html",
            "Prompts",
            readme.read_text(encoding="utf-8")
            if readme.exists()
            else "# Prompts\n\nReusable request prompts.\n",
            subtitle=f"{len(self.catalog.prompts)} reusable requests across "
            f"{len(self.catalog.categories)} lifecycle categories.",
            eyebrow="Library / prompts",
            breadcrumbs=[("Library", "library/index.html"), ("Prompts", "")],
            crumb_label="Library / Prompts",
        )

        flat = [(c, p) for c in self.catalog.categories for p in c.prompts]
        for category in self.catalog.categories:
            rows = "\n".join(
                f"| [{p.stem}]({p.stem}.md) | {p.objective} |" for p in category.prompts
            )
            self.emit(
                f"library/prompts/{category.name}/index.html",
                category.name.capitalize(),
                f"# {category.name.capitalize()}\n\n{category.description}\n\n"
                f"| Prompt | Objective |\n|---|---|\n{rows}\n",
                subtitle=f"{len(category.prompts)} prompts.",
                eyebrow=f"Prompts / {category.name}",
                breadcrumbs=[
                    ("Library", "library/index.html"),
                    ("Prompts", "library/prompts/index.html"),
                    (category.name, ""),
                ],
                crumb_label=f"Prompts / {category.name}",
            )
        for i, (category, prompt) in enumerate(flat):
            prev = (
                (flat[i - 1][1].stem, f"library/prompts/{flat[i - 1][0].name}/{flat[i - 1][1].stem}.html")
                if i
                else None
            )
            nxt = (
                (flat[i + 1][1].stem, f"library/prompts/{flat[i + 1][0].name}/{flat[i + 1][1].stem}.html")
                if i + 1 < len(flat)
                else None
            )
            self.emit(
                f"library/prompts/{category.name}/{prompt.stem}.html",
                prompt.stem,
                f"# {prompt.stem}\n\n{prompt.objective}.\n\n```text\n{prompt.text}\n```\n\n"
                f"Paste this into any AI assistant, or send it to a colleague. "
                f"From the terminal: `atlas prompt show {prompt.id}`.\n",
                subtitle=prompt.objective,
                eyebrow=f"Prompt / {category.name}",
                tags=[f"{prompt.words} words", prompt.id],
                breadcrumbs=[
                    ("Library", "library/index.html"),
                    ("Prompts", "library/prompts/index.html"),
                    (category.name, f"library/prompts/{category.name}/index.html"),
                    (prompt.stem, ""),
                ],
                prev=prev,
                next=nxt,
                crumb_label=f"Prompts / {category.name}",
            )

    def build_work(self) -> None:
        if not self.workstreams:
            return
        dashboard = self.repo.work / "README.md"
        live = [w for w in self.workstreams if not w.archived]
        self.emit(
            "work/index.html",
            "Work Dashboard",
            dashboard.read_text(encoding="utf-8")
            if dashboard.exists()
            else "# Work Dashboard\n\nNo dashboard generated yet.\n",
            subtitle=f"{len(live)} live workstream{'s' if len(live) != 1 else ''}. Every "
            "initiative, who owns it, and how far along its tasks say it is.",
            eyebrow="Work",
            breadcrumbs=[("Work", "work/index.html")],
            crumb_label="Work",
        )
        for workstream in self.workstreams:
            base = f"work/{workstream.name}"
            crumbs = [("Work", "work/index.html"), (f"{workstream.id} {workstream.title}", "")]
            readme = workstream.directory / "README.md"
            meta = [
                status_pill(workstream.status),
                f'<span class="pill">{html.escape(workstream.owner)}</span>',
                f'<span class="pill">{workstream.done}/{workstream.total} tasks</span>',
            ]
            self.emit(
                f"{base}/index.html",
                f"{workstream.id}: {workstream.title}",
                readme.read_text(encoding="utf-8") if readme.exists() else f"# {workstream.title}\n",
                subtitle=workstream.summary,
                eyebrow=f"Workstream {workstream.id}",
                tags=list(workstream.data.get("tags") or []),
                breadcrumbs=crumbs,
                meta=meta,
                crumb_label="Work",
            )
            for markdown in sorted(workstream.directory.rglob("*.md")):
                if markdown.name == "README.md" and markdown.parent == workstream.directory:
                    continue
                rel = markdown.relative_to(workstream.directory)
                target = (
                    rel.with_name("index.html")
                    if markdown.name == "README.md"
                    else rel.with_suffix(".html")
                )
                section_name = rel.parts[0] if len(rel.parts) > 1 else ""
                section_title = SECTION_INTROS.get(section_name, (section_name, ""))[0]
                # A section's own README is that section's page. Titling it
                # "Readme" throws away the one word the reader needs.
                if markdown.name == "README.md":
                    page_title = SECTION_INTROS.get(
                        markdown.parent.name,
                        (markdown.parent.name.replace("_", " ").title(), ""))[0]
                else:
                    page_title = markdown.stem.replace("-", " ").replace("_", " ").capitalize()
                self.emit(
                    f"{base}/{target.as_posix()}",
                    page_title,
                    markdown.read_text(encoding="utf-8"),
                    subtitle=f"{workstream.id} {workstream.title}",
                    eyebrow=f"Workstream {workstream.id}"
                            + (f" / {section_title}" if section_title else ""),
                    breadcrumbs=[
                        ("Work", "work/index.html"),
                        (workstream.title, f"{base}/index.html"),
                        (markdown.stem, ""),
                    ],
                    crumb_label=f"Work / {workstream.id}",
                )
            # A section index for every section directory, so the skeleton browses.
            for section in sorted(d for d in workstream.directory.rglob("*") if d.is_dir()):
                if (section / "README.md").exists():
                    continue
                rel = section.relative_to(workstream.directory)
                title, intro = SECTION_INTROS.get(
                    section.name, (section.name.replace("_", " ").title(), ""))
                files = sorted(f for f in section.iterdir() if f.suffix == ".md")
                subdirs = sorted(
                    d for d in section.iterdir()
                    if d.is_dir() and any(d.glob("*.md")))
                body = [f"# {title}", ""]
                if intro:
                    body += [intro, ""]
                if files:
                    body += ["| Document | |", "|---|---|"]
                    body += [f"| [{f.stem}]({f.stem}.md) | |" for f in files]
                    body.append("")
                for sub in subdirs:
                    sub_title, sub_intro = SECTION_INTROS.get(sub.name, (sub.name.title(), ""))
                    body += [f"## {sub_title}", ""]
                    if sub_intro:
                        body += [sub_intro, ""]
                    body += [f"- [{f.stem}]({sub.name}/{f.stem}.md)"
                             for f in sorted(sub.glob("*.md"))]
                    body.append("")
                if not files and not subdirs:
                    body += [
                        '<div class="empty-state"><p>Nothing recorded here yet. Every '
                        "workstream carries the same nine sections whether or not each one "
                        "has entries, so a reader always finds the same thing in the same "
                        "place.</p></div>",
                        "",
                    ]
                self.emit(
                    f"{base}/{rel.as_posix()}/index.html",
                    title,
                    "\n".join(body),
                    subtitle=f"{workstream.id} {workstream.title}",
                    eyebrow=f"Workstream {workstream.id} / {section.name}",
                    breadcrumbs=[
                        ("Work", "work/index.html"),
                        (workstream.title, f"{base}/index.html"),
                        (title, ""),
                    ],
                    index_it=False,
                )
            for manifest in workstream.directory.glob("*.yaml"):
                destination = self.out / base / manifest.name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(manifest, destination)

    def build_cli(self) -> None:
        """CLI pages, generated from the parser itself.

        Reference documentation written by hand drifts from the tool the moment
        a flag is added. Generating it from the same parser that serves
        ``--help`` means the two cannot disagree.
        """
        from ..cli.app import command_tree, render_reference

        tree = command_tree()
        rows = "\n".join(
            f"| [`atlas {name}`](reference.md#atlas-{name.replace(' ', '-')}) | {summary} |"
            for name, summary, _ in tree
        )
        overview = f"""# The `atlas` CLI

One command operates every part of a repository: the standards, the work, the
library, the checks, and this site. Everything it does can also be imported from
the `atlas` Python package, because the CLI is a thin shell over a library rather
than the other way round.

## Install

```bash
pip install atlas-standard        # or: pipx install atlas-standard
atlas --version
```

## First run

```bash
atlas init my-service ../my-service   # a new repository that already passes
cd ../my-service
atlas check                           # what does the standard still want?
atlas work new migrate-the-fleet --owner person:you
atlas site serve                      # read the docs in a browser
```

## Commands

| Command | Does |
|---|---|
{rows}

## Conventions

Every command accepts `--json` for output a script can read, `-C <dir>` to work
on a repository other than the current one, and `--no-color` to drop the styling.
The exit codes are stable, and they distinguish outcomes a script needs to tell
apart: `0` success, `1` violations found, `2` bad usage, `3` not found, `4` not
an Atlas repository.

Shell completion is available for bash, zsh, and fish:

```bash
atlas completion zsh > ~/.zsh/completions/_atlas
```
"""
        self.emit(
            "cli/index.html",
            "The atlas CLI",
            overview,
            subtitle="One command for the whole standard, discoverable from its own help.",
            eyebrow="Command line",
            breadcrumbs=[("CLI", "cli/index.html")],
            crumb_label="CLI",
        )
        self.emit(
            "cli/reference.html",
            "Command reference",
            render_reference(),
            subtitle="Every command, argument, and flag, generated from the parser itself.",
            eyebrow="Command line / reference",
            breadcrumbs=[("CLI", "cli/index.html"), ("Reference", "")],
            crumb_label="CLI",
        )

    def build_extras(self) -> None:
        self.emit(
            "404.html",
            "Page not found",
            "# Page not found\n\n"
            '<div class="empty-state"><p>Nothing lives at that address in this build. '
            "The site is generated from Markdown, so a link that used to work usually means a "
            "document was renamed or moved.</p></div>\n\n"
            "Try the [standards](spec/index.md) or the [documentation](docs/index.md), or press "
            "<kbd>/</kbd> to search.\n",
            index_it=False,
            derived_note=False,
        )

        (self.out / "search-index.json").write_text(self.index.to_json(), encoding="utf-8")

        urls = "\n".join(
            f"  <url><loc>{html.escape(page.url, quote=True)}</loc>"
            f"<lastmod>{self.build_date}</lastmod></url>"
            for page in self.emitted
        )
        (self.out / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}\n</urlset>\n",
            encoding="utf-8",
        )
        (self.out / "robots.txt").write_text(
            "User-agent: *\nAllow: /\nSitemap: sitemap.xml\n", encoding="utf-8"
        )
        # GitHub Pages serves this repository's files verbatim; without it,
        # Jekyll silently drops any path beginning with an underscore.
        (self.out / ".nojekyll").write_text("", encoding="utf-8")

    def build_assets(self) -> None:
        assets = self.out / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        css = tokens_mod.css_variables(tokens_mod.load(self.repo.tokens)) + STYLESHEET
        (assets / "site.css").write_text(css, encoding="utf-8")
        (assets / "favicon.svg").write_text(FAVICON, encoding="utf-8")
        (assets / "mark.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{MARK_SVG[MARK_SVG.index(">") + 1:]}',
            encoding="utf-8",
        )
        for source in sorted(self.repo.assets.glob("*.svg")) if self.repo.assets.is_dir() else []:
            shutil.copy2(source, assets / source.name)

    def run(self) -> BuildResult:
        if self.out.exists():
            shutil.rmtree(self.out)
        self.out.mkdir(parents=True)
        self.build_assets()
        self.build_home()
        self.build_specs()
        self.build_work()
        self.build_docs()
        self.build_library()
        self.build_cli()
        self.build_extras()
        return BuildResult(
            pages=len(self.emitted),
            out=self.out,
            indexed=len(self.index),
            warnings=self.warnings,
        )


def build(repo: Repository, out: pathlib.Path | None = None) -> BuildResult:
    """Render the whole site into ``out`` (default ``site/``)."""
    return Builder(repo, out or repo.site_out).run()
