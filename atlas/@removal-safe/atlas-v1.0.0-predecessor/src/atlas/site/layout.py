"""The page shell: chrome, navigation, and the small amount of client script.

One shell serves every page. Its structure is fixed: toolbar, sidebar,
content, inspector, and pages vary only by what they put in the content
region, which is what makes the site feel like one product rather than a
collection of generated files.

The client script is intentionally small and defensive: no framework, no build
step, no dependency that can break the docs. Everything it adds is an
*enhancement*: the page is fully readable and navigable with JavaScript
disabled, and the search dialog is the only feature that requires it.
"""

from __future__ import annotations

import dataclasses
import html
import typing as t

__all__ = ["Page", "NavGroup", "NavItem", "render_page", "SCRIPT"]

#: The brand mark: a stacked-plates glyph, drawn once and inlined everywhere so
#: it needs no request and inherits `currentColor` in both themes.
MARK_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linejoin="round" aria-hidden="true">'
    '<path d="M12 3 3 7.5 12 12l9-4.5L12 3Z"/>'
    '<path d="M3 12.5 12 17l9-4.5"/>'
    '<path d="M3 17.5 12 22l9-4.5"/></svg>'
)

ICONS: dict[str, str] = {
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4"/>',
    "moon": '<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5Z"/>',
    "spec": '<path d="M4 4h11l5 5v11H4z"/><path d="M15 4v5h5"/>',
    "work": '<path d="M3 7h18v12H3z"/><path d="M8 7V5h8v2"/>',
    "github": '<path d="M9 19c-4 1.4-4-2.5-6-3m12 5v-3.9a3.4 3.4 0 0 0-.9-2.6c3-.3 6.2-1.5 6.2-6.7A5.2 5.2 0 0 0 19 3.5a4.9 4.9 0 0 0-.1-3.6s-1.1-.3-3.6 1.4a12.3 12.3 0 0 0-6.6 0C6.2-.4 5.1-.1 5.1-.1A4.9 4.9 0 0 0 5 3.5 5.2 5.2 0 0 0 3.7 7.1c0 5.2 3.2 6.4 6.2 6.7a3.4 3.4 0 0 0-.9 2.6V20"/>',
}


def icon(name: str, *, stroke: float = 1.7) -> str:
    return (
        f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{stroke}" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
    )


@dataclasses.dataclass(frozen=True)
class NavItem:
    href: str
    label: str
    number: str = ""
    status: str = ""


@dataclasses.dataclass(frozen=True)
class NavGroup:
    label: str
    items: list[NavItem]


@dataclasses.dataclass
class Page:
    """Everything the shell needs to render one page."""

    title: str
    body: str
    #: (level, slug, text) for the contents rail.
    headings: list[tuple[int, str, str]] = dataclasses.field(default_factory=list)
    subtitle: str = ""
    #: Depth below the site root, for relative asset and nav links.
    depth: int = 0
    breadcrumbs: list[tuple[str, str]] = dataclasses.field(default_factory=list)
    nav: list[NavGroup] = dataclasses.field(default_factory=list)
    active: str = ""
    prev: tuple[str, str] | None = None
    next: tuple[str, str] | None = None
    meta: list[str] = dataclasses.field(default_factory=list)
    description: str = ""
    #: Suppress the generated-from-Markdown footer note (home, 404).
    derived_note: bool = True
    #: Content domain, which selects the accent used across every surface.
    domain: str = ""
    #: Short label shown above the title, naming the domain in words.
    eyebrow: str = ""
    #: Tag chips rendered under the title.
    tags: list[str] = dataclasses.field(default_factory=list)


SCRIPT = r"""<script>
(function () {
  'use strict';
  var body = document.body;
  var qs = function (s, r) { return (r || document).querySelector(s); };
  var qsa = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---- theme ---------------------------------------------------------
     Three states, not two: light, dark, and "follow the system". A binary
     toggle silently overrides a system preference the reader deliberately
     set, and gives them no way back. */
  var THEMES = ['system', 'light', 'dark'];
  var themeBtn = qs('.theme-toggle');
  function currentTheme() {
    try { return localStorage.getItem('atlas-theme') || 'system'; } catch (e) { return 'system'; }
  }
  function applyTheme(name) {
    if (name === 'system') { document.documentElement.removeAttribute('data-theme'); }
    else { document.documentElement.setAttribute('data-theme', name); }
    try { localStorage.setItem('atlas-theme', name); } catch (e) {}
    if (themeBtn) {
      themeBtn.setAttribute('aria-label', 'Theme: ' + name + '. Click to change.');
      themeBtn.setAttribute('data-theme-state', name);
    }
  }
  applyTheme(currentTheme());
  themeBtn && themeBtn.addEventListener('click', function () {
    applyTheme(THEMES[(THEMES.indexOf(currentTheme()) + 1) % THEMES.length]);
  });

  /* ---- drawer --------------------------------------------------------- */
  var toggle = qs('.drawer-toggle'), shut = qs('.drawer-close'), scrim = qs('.scrim');
  function setDrawer(open) {
    body.classList.toggle('drawer-open', open);
    toggle && toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (scrim) scrim.hidden = !open;
    if (open) { (shut || toggle).focus(); }
  }
  toggle && toggle.addEventListener('click', function () {
    setDrawer(!body.classList.contains('drawer-open'));
  });
  shut && shut.addEventListener('click', function () { setDrawer(false); toggle.focus(); });
  scrim && scrim.addEventListener('click', function () { setDrawer(false); });

  /* ---- nav shadow: the islands do not move ---------------------------
     Past 8px the shadow deepens from float to popover and nothing else
     changes, so the layout underneath never shifts. */
  var nav = qs('.navrow');
  function onScroll() { nav && nav.classList.toggle('is-scrolled', window.scrollY > 8); }
  onScroll();
  addEventListener('scroll', onScroll, { passive: true });

  /* ---- overflow affordances ------------------------------------------
     Driven by scroll position, so the fade shows only on the edge that
     actually has content beyond it. */
  function edges(el) {
    var max = el.scrollWidth - el.clientWidth;
    el.classList.toggle('ovf-start', max > 1 && el.scrollLeft > 1);
    el.classList.toggle('ovf-end', max > 1 && el.scrollLeft < max - 1);
  }
  qsa('.scroller').forEach(function (el) {
    edges(el);
    el.addEventListener('scroll', function () { edges(el); }, { passive: true });
  });
  addEventListener('resize', function () { qsa('.scroller').forEach(edges); });

  /* ---- copy buttons --------------------------------------------------- */
  qsa('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var code = qs('code', btn.parentNode);
      if (!code || !navigator.clipboard) return;
      navigator.clipboard.writeText(code.innerText).then(function () {
        btn.textContent = 'Copied';
        btn.classList.add('is-copied');
        setTimeout(function () {
          btn.textContent = 'Copy';
          btn.classList.remove('is-copied');
        }, 1600);
      });
    });
  });

  /* ---- contents rail: highlight the section in view -------------------
     rootMargin pins the trigger line just below the fixed toolbar, so the
     highlighted entry is the heading a reader can actually see. */
  var tocLinks = qsa('.inspector .toclist a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var byId = {};
    tocLinks.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
    var seen = new Set();
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) seen.add(entry.target.id); else seen.delete(entry.target.id);
      });
      tocLinks.forEach(function (a) { a.classList.remove('is-current'); });
      var first = Object.keys(byId).filter(function (id) { return seen.has(id); })[0];
      if (first && byId[first]) byId[first].classList.add('is-current');
    }, { rootMargin: '-120px 0px -70% 0px' });
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) observer.observe(el);
    });
  }

  /* ---- search ---------------------------------------------------------
     The index is fetched on first open, not on page load. It is the largest
     asset the site ships and most visits never search. */
  var dialog = qs('#search-dialog');
  var input = qs('#search-input');
  var results = qs('#search-results');
  var openers = qsa('[data-search-open]');
  var index = null, loading = false, active = -1;

  function root() { return (document.documentElement.getAttribute('data-root') || ''); }

  function load() {
    if (index || loading) return Promise.resolve();
    loading = true;
    return fetch(root() + 'search-index.json')
      .then(function (r) { return r.json(); })
      .then(function (data) { index = data; loading = false; })
      .catch(function () { loading = false; });
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"]/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c];
    });
  }

  function snippet(text, terms) {
    var lower = text.toLowerCase();
    var at = -1;
    for (var i = 0; i < terms.length && at < 0; i++) at = lower.indexOf(terms[i]);
    if (at < 0) at = 0;
    var start = Math.max(0, at - 60);
    var slice = (start > 0 ? '\u2026' : '') + text.slice(start, start + 200) + '\u2026';
    return escapeHtml(slice).replace(new RegExp('(' + terms.map(function (t) {
      return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }).join('|') + ')', 'gi'), '<mark>$1</mark>');
  }

  /* Scoring is intentionally simple and explainable: a title hit outranks a
     heading hit outranks a body hit, and matching every term outranks
     matching one. A reader can predict the order, which matters more in
     documentation than relevance sophistication. */
  function score(entry, terms) {
    var title = entry.t.toLowerCase(), heads = (entry.h || '').toLowerCase(),
        text = (entry.b || '').toLowerCase(), total = 0;
    for (var i = 0; i < terms.length; i++) {
      var term = terms[i], hit = 0;
      if (title.indexOf(term) === 0) hit += 60;
      else if (title.indexOf(term) >= 0) hit += 40;
      if (heads.indexOf(term) >= 0) hit += 12;
      if (text.indexOf(term) >= 0) hit += 4;
      if (!hit) return 0;
      total += hit;
    }
    return total;
  }

  function render(query) {
    if (!index) return;
    var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) {
      results.innerHTML = '<li class="search-empty">Type to search the specifications, docs, work, and CLI.</li>';
      return;
    }
    var hits = index.map(function (entry) { return { e: entry, s: score(entry, terms) }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s; })
      .slice(0, 30);
    if (!hits.length) {
      results.innerHTML = '<li class="search-empty">No matches for \u201c' + escapeHtml(query) + '\u201d.</li>';
      return;
    }
    results.innerHTML = hits.map(function (hit, i) {
      var e = hit.e;
      return '<li><a href="' + root() + e.u + '"' + (i === 0 ? ' class="is-active"' : '') + '>' +
        '<span class="search-title">' + escapeHtml(e.t) + '</span>' +
        '<span class="search-crumb">' + escapeHtml(e.c || '') + '</span>' +
        '<span class="search-snippet">' + snippet(e.b || '', terms) + '</span></a></li>';
    }).join('');
    active = 0;
  }

  function move(delta) {
    var links = qsa('a', results);
    if (!links.length) return;
    links.forEach(function (a) { a.classList.remove('is-active'); });
    active = (active + delta + links.length) % links.length;
    links[active].classList.add('is-active');
    links[active].scrollIntoView({ block: 'nearest' });
  }

  function openSearch() {
    if (!dialog) return;
    load().then(function () { render(input.value); });
    if (typeof dialog.showModal === 'function' && !dialog.open) dialog.showModal();
    input.focus();
    input.select();
  }

  openers.forEach(function (el) {
    el.addEventListener('click', function (e) { e.preventDefault(); openSearch(); });
  });
  input && input.addEventListener('input', function () { render(input.value); });
  dialog && dialog.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
    else if (e.key === 'Enter') {
      var current = qs('a.is-active', results);
      if (current) { e.preventDefault(); window.location.href = current.href; }
    }
  });

  document.addEventListener('keydown', function (e) {
    var typing = /^(INPUT|TEXTAREA|SELECT)$/.test((e.target.tagName || '')) || e.target.isContentEditable;
    if (e.key === 'Escape') { setDrawer(false); return; }
    if (typing) return;
    if (e.key === '/' || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k')) {
      e.preventDefault(); openSearch();
    }
  });
})();
</script>"""

NO_SCRIPT_NOTE = (
    '<noscript><p class="visually-hidden">Search requires JavaScript; '
    "all pages remain browsable through the navigation.</p></noscript>"
)


def _toc(headings: list[tuple[int, str, str]]) -> tuple[str, str]:
    """Render the contents rail and its drawer copy.

    A single-entry contents list is noise: it tells the reader what they can
    already see. Below two entries, both renderings are suppressed.
    """
    entries = [h for h in headings if h[0] in (2, 3)]
    if len(entries) < 2:
        return "", ""
    items = "".join(
        f'<li class="lvl-{level}"><a href="#{slug}">{html.escape(text)}</a></li>'
        for level, slug, text in entries
    )
    rail = (
        '<aside class="inspector" aria-label="On this page">'
        '<div class="rail-label">On this page</div>'
        f'<ul class="toclist">{items}</ul></aside>'
    )
    drawer = (
        '<div class="nav-group"><div class="nav-label">On this page</div>'
        f'<ul class="toclist">{items}</ul></div>'
    )
    return rail, drawer


def _sidebar(groups: list[NavGroup], active: str, up: str) -> str:
    parts: list[str] = []
    for group in groups:
        items = []
        for item in group.items:
            classes = "active" if item.href == active else ""
            number = f'<span class="nav-num">{html.escape(item.number)}</span>' if item.number else ""
            # Only states that need a reader's attention get a mark (see theme).
            dot = (
                f'<span class="nav-dot is-{item.status}" title="{item.status}"></span>'
                if item.status in ("blocked", "review")
                else ""
            )
            aria = ' aria-current="page"' if item.href == active else ""
            items.append(
                f'<li><a class="{classes}" href="{up}{item.href}"{aria}>{number}{dot}'
                f'<span class="nav-text">{html.escape(item.label)}</span></a></li>'
            )
        parts.append(
            f'<div class="nav-group"><div class="nav-label">{html.escape(group.label)}</div>'
            f'<ul>{"".join(items)}</ul></div>'
        )
    return "".join(parts)


def _breadcrumbs(crumbs: list[tuple[str, str]], up: str) -> str:
    if not crumbs:
        return ""
    parts: list[str] = []
    for i, (label, href) in enumerate(crumbs):
        last = i == len(crumbs) - 1
        if last or not href:
            parts.append(f'<span aria-current="page">{html.escape(label)}</span>')
        else:
            parts.append(f'<a href="{up}{href}">{html.escape(label)}</a>')
        if not last:
            parts.append('<span class="breadcrumb-sep" aria-hidden="true">/</span>')
    return f'<nav class="breadcrumb" aria-label="Breadcrumb">{"".join(parts)}</nav>'


def _pager(page: Page, up: str) -> str:
    if not page.prev and not page.next:
        return ""
    parts = ['<nav class="pager" aria-label="Pagination">']
    if page.prev:
        label, href = page.prev
        parts.append(
            f'<a class="pager-prev" href="{up}{href}" rel="prev">'
            f'<span class="pager-label">Previous</span>'
            f'<span class="pager-title">{html.escape(label)}</span></a>'
        )
    else:
        parts.append("<span></span>")
    if page.next:
        label, href = page.next
        parts.append(
            f'<a class="pager-next" href="{up}{href}" rel="next">'
            f'<span class="pager-label">Next</span>'
            f'<span class="pager-title">{html.escape(label)}</span></a>'
        )
    parts.append("</nav>")
    return "".join(parts)


def render_page(
    page: Page,
    *,
    site_name: str,
    tagline: str,
    nav_items: t.Sequence[tuple[str, str]],
    repository_url: str,
    build_date: str,
    version: str,
) -> str:
    up = "../" * page.depth
    rail, drawer_toc = _toc(page.headings)
    links = "".join(
        f'<a class="navlink" href="{up}{href}"'
        + (' aria-current="page"' if page.active.startswith(href.rsplit("/", 1)[0]) else "")
        + f">{html.escape(label)}</a>"
        for href, label in nav_items
    )
    description = html.escape(page.description or page.subtitle or tagline, quote=True)
    meta_pills = (
        f'<div class="page-meta">{"".join(page.meta)}</div>' if page.meta else ""
    )
    eyebrow = (
        f'<p class="eyebrow">{html.escape(page.eyebrow)}</p>' if page.eyebrow else ""
    )
    tags = (
        '<div class="taglist">'
        + "".join(f'<span class="tag tag-accent">{html.escape(x)}</span>' for x in page.tags)
        + "</div>"
        if page.tags
        else ""
    )
    footer_note = (
        "Generated from Markdown \u2014 <strong>the Markdown is canonical</strong>; this page is derived."
        if page.derived_note
        else f"{html.escape(site_name)} \u00b7 {html.escape(tagline)}"
    )

    return f"""<!DOCTYPE html>
<html lang="en" data-root="{up}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<meta name="description" content="{description}">
<meta name="generator" content="{html.escape(site_name)} {html.escape(version)}">
<meta property="og:title" content="{html.escape(page.title)}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="article">
<title>{html.escape(page.title)} \u00b7 {html.escape(site_name)}</title>
<link rel="stylesheet" href="{up}assets/site.css">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<script>
/* Applied before first paint: reading the stored theme after the stylesheet
   has painted produces a flash of the wrong theme on every navigation. */
(function(){{try{{var t=localStorage.getItem('atlas-theme');
if(t&&t!=='system')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();
</script>
</head>
<body data-shell="reading" data-domain="{html.escape(page.domain)}">
<a class="skip-link" href="#content">Skip to content</a>

<div class="navrow">
  <div class="island island-brand">
    <button class="iconbtn drawer-toggle" aria-controls="drawer" aria-expanded="false"
            aria-label="Open navigation">{icon("menu")}</button>
    <a class="brand" href="{up}index.html">
      <span class="mark" aria-hidden="true">{MARK_SVG}</span>
      <span class="brand-word">{html.escape(site_name)}</span></a>
  </div>
  <nav class="island island-nav" aria-label="Sections">{links}</nav>
  <div class="island island-actions">
    <button class="searchbtn" type="button" data-search-open>
      {icon("search", stroke=1.8)}<span>Search</span>
      <span class="kbd" aria-hidden="true">/</span>
    </button>
    <button class="iconbtn theme-toggle" type="button" data-theme-state="system"
            aria-label="Theme: system. Click to change.">{icon("sun", stroke=1.6)}</button>
    <a class="iconbtn" href="{html.escape(repository_url, quote=True)}"
       aria-label="Source repository">{icon("spec", stroke=1.6)}</a>
  </div>
</div>

<div class="shell">
  <aside class="sidebar" id="drawer" aria-label="Contents">
    <div class="drawer-head">
      <span>Contents</span>
      <button class="iconbtn drawer-close" aria-label="Close navigation">{icon("close")}</button>
    </div>
    {_sidebar(page.nav, page.active, up)}
    {drawer_toc}
  </aside>
  <div class="scrim" hidden></div>

  <main class="content" id="content">
    <div class="inner">
      {_breadcrumbs(page.breadcrumbs, up)}
      <div class="page-head">
        {eyebrow}
        <h1 class="page-title">{html.escape(page.title)}</h1>
        {f'<p class="dek">{html.escape(page.subtitle)}</p>' if page.subtitle else ''}
        {meta_pills}
        {tags}
      </div>
      <article class="prose">{page.body}</article>
      {_pager(page, up)}
      <footer class="pagefoot">
        <span>{footer_note}</span>
        <span>Built {html.escape(build_date)} \u00b7 {html.escape(version)}</span>
      </footer>
    </div>
  </main>

  {rail}
</div>

<dialog id="search-dialog" class="searchdlg" aria-label="Search">
  <form method="dialog" role="search">
    {icon("search", stroke=1.8)}
    <label class="visually-hidden" for="search-input">Search</label>
    <input id="search-input" type="search" placeholder="Search specifications, docs, work\u2026"
           autocomplete="off" spellcheck="false">
    <button class="iconbtn" type="submit" aria-label="Close search">{icon("close")}</button>
  </form>
  <ul id="search-results" class="search-results">
    <li class="search-empty">Type to search the specifications, docs, work, and CLI.</li>
  </ul>
  <div class="search-foot">
    <span><span class="kbd">\u2191</span> <span class="kbd">\u2193</span> navigate</span>
    <span><span class="kbd">\u21b5</span> open</span>
    <span><span class="kbd">esc</span> close</span>
  </div>
</dialog>
{NO_SCRIPT_NOTE}
{SCRIPT}
</body>
</html>
"""
