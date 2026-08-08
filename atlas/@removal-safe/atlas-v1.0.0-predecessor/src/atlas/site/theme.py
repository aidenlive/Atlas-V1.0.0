"""The site stylesheet.

Every value here resolves to a design token. There are no literal colors, no
literal type sizes, and no literal spacing steps outside a handful of hairline
optical corrections, which is what makes re-theming a token edit rather than a
search-and-replace across a stylesheet.

Two axes govern layout, and conflating them is the most common way a
documentation site ends up broken on a laptop with a sidebar open:

* **Container** size classes decide *structure*: how many tracks the shell
  has, whether the contents rail survives, whether navigation is docked.
* **Viewport** breakpoints decide *page chrome* only: gutters, the shell cap,
  and the fluid type ceilings.

Status color is never load-bearing on its own. Every pill, callout, and
progress bar pairs its hue with a glyph and a word, so meaning survives
greyscale, color-blindness, and a screen reader.
"""

from __future__ import annotations

__all__ = ["STYLESHEET"]

SANS = '"DM Sans",ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif'
MONO = '"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace'

STYLESHEET = f"""
/* ==========================================================================
   Atlas documentation site
   Structure resolves from the CONTAINER; page chrome from the VIEWPORT.
   ========================================================================== */

*,*::before,*::after{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%;scroll-behavior:smooth}}
/* No horizontal page scroll, ever. A safety net, not a strategy: every wide
   child owns its own .scroller. */
html,body{{overflow-x:clip}}
body{{margin:0;background:var(--background);color:var(--on-surface);
  font-family:{SANS};
  font-size:var(--font-body-md);line-height:var(--lh-body-md);
  letter-spacing:var(--ls-body-md);font-weight:var(--fw-body-md);
  -webkit-font-smoothing:antialiased;
  padding-top:var(--space-nav-stack)}}
code,pre,.mono,.rail-label,.nav-label,.caption,.kbd{{font-family:{MONO}}}

a{{color:inherit;text-decoration:none;border-bottom:1px solid var(--outline-strong);
  transition:border-color var(--motion-duration-fast) var(--motion-ease)}}
a:hover{{border-bottom-color:var(--on-surface)}}

:where(a,button,summary,input,[tabindex]):focus-visible{{
  outline:2px solid var(--focus);outline-offset:2px;border-radius:var(--radius-xs)}}

.skip-link{{position:fixed;top:var(--space-s-3);left:var(--space-s-3);z-index:80;
  transform:translateY(-200%);background:var(--primary);color:var(--on-primary);
  padding:var(--space-s-3) var(--space-s-5);border-radius:var(--radius-pill);border:0;
  font-size:var(--font-label-md);font-weight:var(--fw-label-md);box-shadow:var(--elev-popover)}}
.skip-link:focus{{transform:none}}
.visually-hidden{{position:absolute;width:1px;height:1px;margin:-1px;padding:0;
  overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}}

/* ==========================================================================
   Navigation: one row, three islands (1fr auto 1fr)
   ========================================================================== */
.navrow{{position:fixed;top:0;left:0;right:0;z-index:50;
  display:grid;grid-template-columns:1fr auto 1fr;align-items:center;
  gap:var(--space-s-4);
  max-width:var(--space-shell);margin-inline:auto;
  padding:var(--space-nav-top) var(--space-gutter) 0;
  pointer-events:none}}
.island{{pointer-events:auto;display:flex;align-items:center;gap:var(--space-s-1);
  height:var(--space-nav-h);padding:var(--space-s-2);
  background:color-mix(in oklab, var(--surface) 88%, transparent);
  border:var(--space-hairline) solid var(--outline);border-radius:var(--radius-pill);
  box-shadow:var(--elev-float);
  transition:box-shadow var(--motion-duration-normal) var(--motion-ease)}}
@supports (backdrop-filter:blur(1px)){{.island{{backdrop-filter:blur(12px) saturate(1.4)}}}}
.navrow.is-scrolled .island{{box-shadow:var(--elev-popover)}}
.island-brand{{grid-column:1;justify-self:start;min-width:0}}
.island-nav{{grid-column:2;justify-self:center}}
.island-actions{{grid-column:3;justify-self:end}}

.brand{{display:flex;align-items:center;gap:var(--space-s-2);border:0;min-width:0;
  padding-inline:var(--space-s-3) var(--space-s-4);
  font-size:var(--font-label-lg);font-weight:var(--fw-label-lg)}}
.brand-word{{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.mark{{width:16px;height:16px;flex:none;color:var(--on-surface)}}
.mark svg{{display:block;width:100%;height:100%}}

.navlink{{display:inline-flex;align-items:center;height:var(--space-control-h-sm);
  padding:0 var(--space-s-4);border:0;border-radius:var(--radius-pill);
  font-size:var(--font-label-sm);font-weight:var(--fw-label-sm);color:var(--on-surface-2);
  white-space:nowrap}}
.navlink:hover{{background:var(--surface-3);color:var(--on-surface)}}
.navlink[aria-current="page"]{{background:var(--primary);color:var(--on-primary)}}

/* Icon-only controls hold the full pointer target; the glyph is centered inside
   the target, not the target sized to the glyph. */
.iconbtn{{display:inline-flex;align-items:center;justify-content:center;
  width:var(--space-control-h-sm);height:var(--space-control-h-sm);
  padding:0;border:0;border-radius:var(--radius-pill);
  background:transparent;color:var(--on-surface-2);cursor:pointer;flex:none}}
.iconbtn:hover{{background:var(--surface-3);color:var(--on-surface)}}
.iconbtn svg{{width:var(--space-icon-md);height:var(--space-icon-md)}}
@media (pointer:coarse){{.iconbtn{{min-width:var(--space-target-coarse);min-height:var(--space-target-coarse)}}}}

/* Search trigger: a control, so it reads as one, with its shortcut visible. */
.searchbtn{{display:inline-flex;align-items:center;gap:var(--space-s-2);
  height:var(--space-control-h-sm);padding:0 var(--space-s-2) 0 var(--space-s-3);
  border:var(--space-hairline) solid var(--outline);border-radius:var(--radius-pill);
  background:var(--surface-2);color:var(--on-surface-3);cursor:pointer;
  font-family:inherit;font-size:var(--font-label-sm)}}
.searchbtn:hover{{color:var(--on-surface);border-color:var(--outline-strong)}}
.searchbtn svg{{width:var(--space-icon-xs);height:var(--space-icon-xs)}}
.searchbtn .kbd{{display:none}}
@media (min-width:768px){{.searchbtn .kbd{{display:inline-flex}}}}
.kbd{{display:inline-flex;align-items:center;height:20px;padding:0 var(--space-s-2);
  border:var(--space-hairline) solid var(--outline);border-radius:var(--radius-xs);
  background:var(--surface);font-size:var(--font-mono-xs);color:var(--on-surface-3)}}

/* ==========================================================================
   Shell: three tracks, both rails one token
   ========================================================================== */
.shell{{display:grid;gap:var(--space-s-10);
  max-width:var(--space-shell);margin-inline:auto;
  padding-inline:var(--space-gutter);padding-block:var(--space-s-8) var(--space-s-12);
  grid-template-columns:minmax(0,1fr)}}

@media (min-width:1024px){{
  .shell{{padding-inline:var(--space-gutter-lg);justify-content:center;
    grid-template-columns:
      minmax(var(--space-rail-min),var(--space-rail))
      /* min(100%,content) is what makes the RAILS compress first: the content
         track claims its measure, so between lg and the shell cap the rails
         sit between rail-min and rail rather than squeezing the prose. */
      minmax(min(100%,var(--space-content)),var(--space-content))
      minmax(var(--space-rail-min),var(--space-rail))}}
}}

.content{{container:content / inline-size;min-width:0}}
.content .inner{{min-width:0}}

/* ---- sidebar: docked at lg, drawer below ---- */
.sidebar{{grid-column:1;min-width:0}}
.rail-label,.nav-label{{font-size:var(--font-mono-xs);line-height:var(--lh-mono-xs);
  letter-spacing:var(--ls-mono-xs);font-weight:var(--fw-mono-xs);
  text-transform:uppercase;color:var(--on-surface-3);
  padding:var(--space-s-4) var(--space-s-3) var(--space-s-2)}}
.nav-group ul,.toclist{{list-style:none;margin:0;padding:0}}
.sidebar a,.toclist a{{display:flex;align-items:center;gap:var(--space-s-2);
  min-height:var(--space-control-h-sm);
  padding:var(--space-s-2) var(--space-s-3);border:0;border-radius:var(--radius-sm);
  font-size:var(--font-body-xs);line-height:var(--lh-body-xs);color:var(--on-surface-2)}}
.sidebar a:hover,.toclist a:hover{{background:var(--surface-2);color:var(--on-surface)}}
.nav-num{{font-family:{MONO};font-size:var(--font-mono-xs);
  color:var(--on-surface-3);flex:none}}
.nav-text{{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
/* Status marks appear on EXCEPTION only. A dot beside every item makes a
   healthy list look like a dashboard in distress and buries the one entry that
   needs attention. Blocked and in-review get a mark; everything else is quiet. */
.nav-dot{{width:6px;height:6px;flex:none;border-radius:var(--radius-full)}}
.nav-dot.is-blocked{{background:var(--error)}}
.nav-dot.is-review{{background:var(--warning)}}
.drawer-head{{display:none}}

@media (min-width:1024px){{
  .sidebar{{position:sticky;top:var(--space-nav-stack);align-self:start;
    max-height:calc(100dvh - var(--space-nav-stack) - var(--space-s-6));
    overflow-y:auto;scrollbar-width:thin;overscroll-behavior:contain}}
}}
@media (max-width:1023px){{
  .sidebar{{position:fixed;inset-block:0;inset-inline-start:0;z-index:60;
    width:min(88vw,380px);background:var(--surface);
    border-inline-end:var(--space-hairline) solid var(--outline);
    box-shadow:var(--elev-modal);
    padding:var(--space-s-6) var(--space-s-5);
    padding-bottom:calc(var(--space-s-10) + env(safe-area-inset-bottom));
    overflow-y:auto;overscroll-behavior:contain;
    transform:translateX(-100%);visibility:hidden;
    transition:transform var(--motion-duration-normal) var(--motion-ease),
               visibility 0s linear var(--motion-duration-normal)}}
  body.drawer-open .sidebar{{transform:none;visibility:visible;transition-delay:0s}}
  .drawer-head{{display:flex;align-items:center;justify-content:space-between;
    font-size:var(--font-mono-xs);letter-spacing:var(--ls-mono-xs);text-transform:uppercase;
    color:var(--on-surface-3);padding-bottom:var(--space-s-3);margin-bottom:var(--space-s-3);
    border-bottom:var(--space-hairline) solid var(--outline)}}
  .scrim{{position:fixed;inset:0;z-index:55;background:var(--overlay);border:0}}
}}
@media (min-width:1024px){{.drawer-toggle,.scrim{{display:none}}}}

/* ---- inspector rail: the contents list ---- */
.inspector{{grid-column:3;display:none;min-width:0}}
@media (min-width:1280px){{
  .inspector{{display:block;position:sticky;top:var(--space-nav-stack);align-self:start;
    max-height:calc(100dvh - var(--space-nav-stack) - var(--space-s-6));
    overflow-y:auto;scrollbar-width:thin;overscroll-behavior:contain}}
}}
.inspector .toclist{{border-inline-start:var(--space-hairline) solid var(--outline)}}
.inspector .toclist a{{margin-inline-start:-1px;border-radius:0;
  border-inline-start:2px solid transparent}}
.inspector .toclist a:hover{{background:transparent;border-inline-start-color:var(--on-surface-3)}}
.inspector .toclist a.is-current{{border-inline-start-color:var(--primary);color:var(--on-surface)}}
.inspector .lvl-3 a{{padding-inline-start:var(--space-s-6)}}

/* ==========================================================================
   Reading column
   ========================================================================== */
:where(.page-head,.prose) :is(h1,h2,h3,h4){{font-weight:500;text-wrap:balance}}
.breadcrumb{{display:flex;flex-wrap:wrap;align-items:center;gap:var(--space-s-2);
  margin-bottom:var(--space-s-4);font-size:var(--font-body-xs);color:var(--on-surface-3)}}
.breadcrumb a{{border:0;color:var(--on-surface-3)}}
.breadcrumb a:hover{{color:var(--on-surface)}}
.breadcrumb-sep{{opacity:.5}}
.breadcrumb [aria-current="page"]{{color:var(--on-surface-2)}}

.page-head{{padding-bottom:var(--space-s-5);margin-bottom:var(--space-s-7);
  border-bottom:var(--space-hairline) solid var(--outline)}}
.page-title{{margin:0;font-size:var(--font-headline-md);line-height:var(--lh-headline-md);
  letter-spacing:var(--ls-headline-md)}}
.dek{{margin:var(--space-s-3) 0 0;max-width:var(--space-measure);
  font-size:var(--font-body-lg);line-height:var(--lh-body-lg);
  letter-spacing:var(--ls-body-lg);color:var(--on-surface-2)}}
.page-meta{{display:flex;flex-wrap:wrap;gap:var(--space-s-2);margin-top:var(--space-s-4)}}

.prose{{max-width:var(--space-measure)}}
.prose>*{{margin-block:0 var(--space-s-5)}}
.prose h2{{margin-block:var(--space-s-10) var(--space-s-4);
  font-size:var(--font-headline-sm);line-height:var(--lh-headline-sm);
  letter-spacing:var(--ls-headline-sm);
  padding-bottom:var(--space-s-3);border-bottom:var(--space-hairline) solid var(--outline)}}
.prose h3{{margin-block:var(--space-s-8) var(--space-s-3);
  font-size:var(--font-headline-xs);line-height:var(--lh-headline-xs);
  letter-spacing:var(--ls-headline-xs)}}
.prose h4{{margin-block:var(--space-s-6) var(--space-s-2);font-size:var(--font-label-lg)}}
:target,.anchor-only{{scroll-margin-top:var(--space-scroll-offset)}}
.anchor-only{{display:block;height:0}}

/* The anchor appears on hover and on keyboard focus: a hover-only affordance
   is unreachable from a keyboard. */
.heading-anchor{{border:0;margin-inline-start:var(--space-s-2);
  color:var(--on-surface-3);opacity:0;font-weight:400;
  transition:opacity var(--motion-duration-fast) var(--motion-ease)}}
:is(h2,h3,h4):hover .heading-anchor,.heading-anchor:focus-visible{{opacity:1}}

.prose ul,.prose ol{{padding-inline-start:var(--space-s-6)}}
.prose li{{margin-block:var(--space-s-2)}}
.prose li>:is(ul,ol){{margin-top:var(--space-s-2)}}
.prose blockquote{{margin-inline:0;padding-inline-start:var(--space-s-5);
  border-inline-start:2px solid var(--outline-strong);color:var(--on-surface-2)}}
.prose hr{{border:0;border-top:var(--space-hairline) solid var(--outline);margin-block:var(--space-s-9)}}
.prose img,.prose svg{{max-width:100%;height:auto}}

.checklist{{list-style:none;padding-inline-start:0}}
.checklist li{{display:flex;gap:var(--space-s-3);align-items:flex-start}}
.task-box{{display:inline-flex;align-items:center;justify-content:center;flex:none;
  width:18px;height:18px;margin-top:3px;border-radius:var(--radius-xs);
  border:var(--space-hairline) solid var(--outline-strong);
  background:var(--surface);font-size:11px;line-height:1}}
.task-box.is-checked{{background:var(--success);border-color:var(--success);color:var(--on-primary)}}

.rule-ref{{border:0;font-family:{MONO};font-size:.92em;
  color:var(--on-surface-2);background:var(--surface-2);
  padding:1px 4px;border-radius:var(--radius-xs)}}
.rule-ref:hover{{color:var(--on-surface);background:var(--surface-3)}}
.rule-ref:target{{background:var(--warning-surface);color:var(--warning);outline:2px solid var(--warning)}}

/* Long identifiers break; code never does: a token name broken mid-string
   reads as two different identifiers. */
.prose{{overflow-wrap:anywhere}}
.prose :is(pre,code){{overflow-wrap:normal;word-break:normal;hyphens:none}}
.prose p>code,.prose li>code,.prose td>code,.prose h2>code,.prose h3>code{{
  background:var(--surface-2);border:var(--space-hairline) solid var(--outline);
  border-radius:var(--radius-xs);padding:1px 5px;
  font-size:var(--font-mono-md);white-space:nowrap}}

/* ---- the wide break-out: only where the CONTAINER has room ----
   A wide table or a long code sample may exceed the reading measure, but only
   once the content region itself is expanded. Driven by a container query, not
   a media query: a 905px viewport with a docked sidebar has nothing like 905px
   of content, and breaking out there pushes the page sideways. */
@container content (min-width: 905px){{
  .prose .scroller.wide{{width:min(var(--space-wide),calc(100cqi + 2 * var(--space-s-10)));
    margin-inline:calc((100cqi - min(var(--space-wide),100cqi + 2 * var(--space-s-10))) / 2)}}
}}

/* ==========================================================================
   Overflow: horizontal scrolling is a component, not an accident
   ========================================================================== */
.scroller{{position:relative;overflow-x:auto;overscroll-behavior-x:contain;
  scrollbar-width:thin;-webkit-overflow-scrolling:touch}}
.scroller:focus-visible{{outline:2px solid var(--focus);outline-offset:2px}}
.scroller.ovf-start{{
  -webkit-mask-image:linear-gradient(to right,transparent,#000 var(--space-s-6));
          mask-image:linear-gradient(to right,transparent,#000 var(--space-s-6))}}
.scroller.ovf-end{{
  -webkit-mask-image:linear-gradient(to left,transparent,#000 var(--space-s-6));
          mask-image:linear-gradient(to left,transparent,#000 var(--space-s-6))}}
.scroller.ovf-start.ovf-end{{
  -webkit-mask-image:linear-gradient(to right,transparent,#000 var(--space-s-6),
     #000 calc(100% - var(--space-s-6)),transparent);
          mask-image:linear-gradient(to right,transparent,#000 var(--space-s-6),
     #000 calc(100% - var(--space-s-6)),transparent)}}

/* ---- tables ---- */
.prose table{{border-collapse:collapse;min-width:max-content;
  font-size:var(--font-body-xs);line-height:var(--lh-body-xs)}}
.prose th,.prose td{{text-align:start;padding:var(--space-s-3) var(--space-s-4);
  border-bottom:var(--space-hairline) solid var(--outline);vertical-align:top}}
.prose th{{font-family:{MONO};
  font-size:var(--font-mono-sm);letter-spacing:var(--ls-mono-sm);
  text-transform:uppercase;color:var(--on-surface-3);
  background:var(--surface-2);white-space:nowrap;position:sticky;top:0;z-index:1}}
.prose tbody tr:last-child td{{border-bottom:0}}
.prose tbody tr:nth-child(even){{background:color-mix(in oklab,var(--surface-2) 55%,transparent)}}
.prose tbody tr:hover{{background:var(--surface-2)}}
.table-wrap{{border:var(--space-hairline) solid var(--outline);
  border-radius:var(--radius-md);background:var(--surface);overflow:hidden}}
.table-wrap>.scroller{{border-radius:inherit;max-height:min(70dvh,820px)}}

/* ---- code ---- */
.codeblock{{margin-block:var(--space-s-5);position:relative;
  border:var(--space-hairline) solid var(--outline);border-radius:var(--radius-md);
  background:var(--code-surface);color:var(--code-plain)}}
.code-lang{{position:absolute;top:0;right:0;z-index:2;
  font-family:{MONO};
  font-size:var(--font-mono-xs);letter-spacing:var(--ls-mono-xs);text-transform:uppercase;
  color:var(--on-surface-3);padding:var(--space-s-1) var(--space-s-2);
  background:var(--surface);
  border-inline-start:var(--space-hairline) solid var(--outline);
  border-block-end:var(--space-hairline) solid var(--outline);
  border-start-end-radius:var(--radius-md);border-end-start-radius:var(--radius-md)}}
.code-copy{{position:absolute;top:var(--space-s-2);right:var(--space-s-2);z-index:3;
  height:26px;padding:0 var(--space-s-3);cursor:pointer;
  border:var(--space-hairline) solid var(--outline);border-radius:var(--radius-xs);
  background:var(--surface);color:var(--on-surface-2);
  font-family:{MONO};font-size:var(--font-mono-xs);
  opacity:0;transition:opacity var(--motion-duration-fast) var(--motion-ease)}}
.codeblock:hover .code-copy,.code-copy:focus-visible{{opacity:1}}
.codeblock:hover .code-lang{{opacity:0}}
.code-copy.is-copied{{color:var(--success);border-color:var(--success)}}
.codeblock pre{{margin:0;padding:var(--space-s-4) var(--space-s-5);background:transparent;
  font-size:var(--font-mono-md);line-height:var(--lh-mono-md);tab-size:2;
  white-space:pre}}                 /* never wraps, never truncates: it scrolls */

/* Syntax roles map to the code-* tokens, which ship light and dark values at
   >=4.5:1 on code-surface. */
.t-c{{color:var(--code-comment);font-style:italic}}
.t-s{{color:var(--code-string)}}
.t-k{{color:var(--code-keyword);font-weight:500}}
.t-a{{color:var(--code-attr);font-weight:500}}
.t-n{{color:var(--code-number)}}
.t-v{{color:var(--code-tag)}}
.t-f{{color:var(--code-punctuation)}}
.t-b{{color:var(--code-function);font-weight:500}}
.t-d{{color:var(--code-function)}}
.t-t{{color:var(--code-tag);font-weight:500}}
.t-p{{color:var(--code-punctuation)}}
.t-added{{color:var(--code-added)}}
.t-removed{{color:var(--code-removed)}}

/* ==========================================================================
   Status: hue is the third channel, never the only one
   ========================================================================== */
.pill{{display:inline-flex;align-items:center;gap:var(--space-s-1);
  padding:2px var(--space-s-2);border-radius:var(--radius-pill);
  border:var(--space-hairline) solid var(--outline);background:var(--surface-2);
  font-family:{MONO};font-size:var(--font-mono-xs);
  letter-spacing:var(--ls-mono-xs);color:var(--on-surface-2);white-space:nowrap}}
.pill-glyph{{font-size:10px;line-height:1;opacity:.9}}
.pill-done,.pill-stable,.pill-pass,.pill-resolved{{
  background:var(--success-surface);border-color:var(--success);color:var(--success)}}
.pill-active,.pill-open{{background:var(--info-surface);border-color:var(--info);color:var(--info)}}
.pill-blocked,.pill-fail{{background:var(--error-surface);border-color:var(--error);color:var(--error)}}
.pill-review,.pill-beta,.pill-mitigated{{
  background:var(--warning-surface);border-color:var(--warning);color:var(--warning)}}
.pill-planned,.pill-todo,.pill-draft,.pill-experimental{{
  background:var(--surface-2);border-color:var(--outline);color:var(--on-surface-2)}}
.pill-cancelled,.pill-dropped,.pill-superseded,.pill-deprecated{{
  background:var(--surface-2);border-color:var(--outline);
  color:var(--on-surface-3);text-decoration:line-through}}

.progress{{display:flex;align-items:center;gap:var(--space-s-2);min-width:120px}}
.progress-track{{height:4px;border-radius:var(--radius-pill);background:var(--chart-track);
  overflow:hidden;flex:1;min-width:56px}}
.progress-track>span{{display:block;height:100%;background:var(--on-surface);
  transition:width var(--motion-duration-normal) var(--motion-ease)}}
.progress-track.is-complete>span{{background:var(--success)}}
.progress-count{{font-family:{MONO};
  font-size:var(--font-mono-xs);color:var(--on-surface-3);white-space:nowrap}}

/* ---- callouts ---- */
.callout{{display:flex;gap:var(--space-s-3);align-items:flex-start;
  margin-block:var(--space-s-5);padding:var(--space-s-4) var(--space-s-5);
  border-radius:var(--radius-md);
  border:var(--space-hairline) solid var(--outline);background:var(--surface-2)}}
.callout-body{{min-width:0}}
.callout p{{margin:0;max-width:var(--space-measure-narrow)}}
.callout p+p{{margin-top:var(--space-s-2)}}
.callout-title{{font-size:var(--font-label-lg);font-weight:var(--fw-label-lg);
  letter-spacing:var(--ls-label-lg)}}
.callout p:not(.callout-title){{font-size:var(--font-body-sm);line-height:var(--lh-body-sm);
  color:var(--on-surface-2)}}
.callout-icon{{display:flex;align-items:center;justify-content:center;flex:none;
  width:20px;height:20px;margin-top:2px;border-radius:var(--radius-full);
  font-family:{SANS};font-size:12px;font-weight:500;line-height:1}}
.callout-info{{background:var(--info-surface);border-color:var(--info)}}
.callout-info .callout-icon{{background:var(--info);color:var(--on-primary)}}
.callout-info .callout-title{{color:var(--info)}}
.callout-success{{background:var(--success-surface);border-color:var(--success)}}
.callout-success .callout-icon{{background:var(--success);color:var(--on-primary)}}
.callout-success .callout-title{{color:var(--success)}}
.callout-warning{{background:var(--warning-surface);border-color:var(--warning)}}
.callout-warning .callout-icon{{background:var(--warning);color:var(--on-primary)}}
.callout-warning .callout-title{{color:var(--warning)}}
.callout-error{{background:var(--error-surface);border-color:var(--error)}}
.callout-error .callout-icon{{background:var(--error);color:var(--on-primary)}}
.callout-error .callout-title{{color:var(--error)}}
.callout-neutral .callout-icon{{background:var(--on-surface-3);color:var(--surface)}}

/* ---- sidebar ----
   Structure is achromatic. An earlier version tinted each group's rail and put
   a coloured dot beside every label; with five groups on screen the sidebar
   read as a legend for a chart that was not there. Hue moved to the places
   where it carries information (eyebrows, tags, badges, status) and navigation
   went back to weight and position, which is what it was using to communicate
   all along. */
.nav-group + .nav-group{{margin-top:var(--space-s-5)}}
.nav-group>ul{{border-inline-start:var(--space-hairline) solid var(--outline);
  padding-inline-start:var(--space-s-2);margin-inline-start:var(--space-s-3)}}
.sidebar a{{position:relative}}
.sidebar a.active{{background:var(--surface-3);color:var(--on-surface);font-weight:500}}
/* The marker sits ON the group rule, replacing that segment of it, so the
   active item reads as a position in the list rather than a decoration. */
.sidebar a.active::before{{content:"";position:absolute;
  inset-block:2px;inset-inline-start:calc(-1 * var(--space-s-2) - 1px);
  width:2px;border-radius:1px;background:var(--primary)}}

.prose p a,.prose li a,.prose td a{{color:var(--primary);
  border-bottom-color:var(--outline-strong)}}
.prose p a:hover,.prose li a:hover,.prose td a:hover{{border-bottom-color:var(--primary)}}

/* ==========================================================================
   Content accents: one hue per DOMAIN, identical on every surface
   ==========================================================================
   A section sets --accent once on the shell; the eyebrow, tags, and section
   markers below read it. Adding a domain is two token lines and one selector,
   not a new component. */
[data-domain]{{--accent:var(--on-surface-2);
  --accent-soft:var(--surface-2);--accent-line:var(--outline)}}
[data-domain="spec"]{{--accent:var(--accent-spec);
  --accent-soft:var(--accent-spec-soft);--accent-line:var(--accent-spec-line)}}
[data-domain="work"]{{--accent:var(--accent-work);
  --accent-soft:var(--accent-work-soft);--accent-line:var(--accent-work-line)}}
[data-domain="docs"]{{--accent:var(--accent-docs);
  --accent-soft:var(--accent-docs-soft);--accent-line:var(--accent-docs-line)}}
[data-domain="library"]{{--accent:var(--accent-library);
  --accent-soft:var(--accent-library-soft);--accent-line:var(--accent-library-line)}}
[data-domain="cli"]{{--accent:var(--accent-cli);
  --accent-soft:var(--accent-cli-soft);--accent-line:var(--accent-cli-line)}}

/* The eyebrow names the domain above the title. It is the one place the
   accent appears at full strength, and it always carries the domain's NAME,
   so the hue is reinforcement and never the only signal. */
.eyebrow{{display:flex;align-items:center;gap:var(--space-s-2);
  margin-bottom:var(--space-s-3);
  font-family:{MONO};font-size:var(--font-mono-xs);
  letter-spacing:var(--ls-mono-xs);text-transform:uppercase;color:var(--accent)}}
.eyebrow::before{{content:"";width:14px;height:2px;border-radius:1px;
  background:var(--accent);flex:none}}

/* ---- tags: soft ground, saturated text, hairline of the same hue ---- */
.taglist{{display:flex;flex-wrap:wrap;gap:var(--space-s-2);margin-top:var(--space-s-4)}}
.tag{{display:inline-flex;align-items:center;gap:var(--space-s-1);
  padding:2px var(--space-s-3);border-radius:var(--radius-pill);
  border:var(--space-hairline) solid var(--tag-line);background:var(--tag-surface);
  font-family:{MONO};font-size:var(--font-mono-xs);
  letter-spacing:var(--ls-mono-xs);color:var(--tag-ink);white-space:nowrap}}
.tag-accent{{border-color:var(--accent-line);background:var(--accent-soft);color:var(--accent)}}
a.tag{{border-bottom-width:var(--space-hairline)}}
a.tag:hover{{border-color:var(--accent);color:var(--accent)}}

/* A card in a domain grid carries a 2px accent edge, nothing more. Tinting the
   whole card would make eight standards read as eight warnings. */
.card-domain{{border-inline-start:2px solid var(--accent-line)}}
.card-domain:hover{{border-inline-start-color:var(--accent)}}
.card-eyebrow{{font-family:{MONO};font-size:var(--font-mono-xs);
  letter-spacing:var(--ls-mono-xs);text-transform:uppercase;color:var(--accent)}}

/* ==========================================================================
   Cards, hero, grids
   ========================================================================== */
.cards{{display:grid;gap:var(--space-s-4);margin-block:var(--space-s-6);
  grid-template-columns:repeat(auto-fill,minmax(248px,1fr))}}
.cards.cards-wide{{grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}}
.card{{container:card / inline-size;display:flex;flex-direction:column;
  gap:var(--space-s-2);padding:var(--space-s-5);border-radius:var(--radius-md);
  border:var(--space-hairline) solid var(--outline);background:var(--surface);
  transition:border-color var(--motion-duration-fast) var(--motion-ease),
             box-shadow var(--motion-duration-fast) var(--motion-ease)}}
a.card{{border-bottom:var(--space-hairline) solid var(--outline)}}
a.card:hover{{border-color:var(--outline-strong);box-shadow:var(--elev-raised)}}
.card-num{{font-family:{MONO};font-size:var(--font-mono-xs);
  letter-spacing:var(--ls-mono-xs);color:var(--on-surface-3)}}
.card h3{{margin:0;font-size:var(--font-headline-xs);line-height:var(--lh-headline-xs);
  letter-spacing:var(--ls-headline-xs);font-weight:500;text-wrap:balance}}
.card p{{margin:0;font-size:var(--font-body-sm);line-height:var(--lh-body-sm);
  color:var(--on-surface-2)}}
.card-meta{{display:flex;align-items:center;gap:var(--space-s-3);
  margin-top:auto;padding-top:var(--space-s-3)}}
.card-question{{font-size:var(--font-body-sm);color:var(--on-surface-2);font-style:italic}}

.hero{{margin-bottom:var(--space-s-9)}}
.hero h1{{margin:0;font-size:var(--font-headline-lg);line-height:var(--lh-headline-lg);
  letter-spacing:var(--ls-headline-lg);font-weight:500;text-wrap:balance}}
.hero .dek{{font-size:var(--font-body-lg)}}
.hero-actions{{display:flex;flex-wrap:wrap;gap:var(--space-s-3);margin-top:var(--space-s-6)}}
.btn{{display:inline-flex;align-items:center;gap:var(--space-s-2);
  height:var(--space-control-h);padding:0 var(--space-s-5);
  border-radius:var(--radius-pill);border:var(--space-hairline) solid transparent;
  font-size:var(--font-label-lg);font-weight:var(--fw-label-lg);cursor:pointer}}
.btn-primary{{background:var(--primary);color:var(--on-primary)}}
.btn-primary:hover{{background:var(--primary-hover);border-color:transparent}}
.btn-secondary{{background:var(--surface);color:var(--on-surface);
  border-color:var(--outline-strong)}}
.btn-secondary:hover{{background:var(--surface-2);border-color:var(--primary)}}

.stat-row{{display:grid;gap:var(--space-s-4);margin-block:var(--space-s-6);
  grid-template-columns:repeat(auto-fit,minmax(140px,1fr))}}
.stat{{padding:var(--space-s-4);border-radius:var(--radius-md);
  border:var(--space-hairline) solid var(--outline);background:var(--surface)}}
.stat-value{{display:block;font-size:var(--font-headline-sm);
  line-height:var(--lh-headline-sm);letter-spacing:var(--ls-headline-sm);font-weight:500}}
.stat-label{{display:block;margin-top:var(--space-s-1);font-family:{MONO};
  font-size:var(--font-mono-xs);letter-spacing:var(--ls-mono-xs);
  text-transform:uppercase;color:var(--on-surface-3)}}

.empty-state{{padding:var(--space-s-9) var(--space-s-5);text-align:center;
  border:var(--space-hairline) dashed var(--outline-strong);border-radius:var(--radius-md);
  color:var(--on-surface-2)}}
.empty-state p{{max-width:var(--space-measure-narrow);margin-inline:auto}}

/* ==========================================================================
   Search
   ========================================================================== */
.searchdlg{{width:min(92vw,620px);max-height:min(76dvh,640px);padding:0;
  border:var(--space-hairline) solid var(--outline);border-radius:var(--radius-lg);
  background:var(--surface);color:var(--on-surface);box-shadow:var(--elev-modal);
  overflow:hidden}}
.searchdlg::backdrop{{background:var(--overlay)}}
.searchdlg form{{display:flex;align-items:center;gap:var(--space-s-3);
  padding:var(--space-s-4) var(--space-s-5);
  border-bottom:var(--space-hairline) solid var(--outline)}}
.searchdlg input{{flex:1;min-width:0;height:var(--space-control-h);border:0;
  background:transparent;color:inherit;font-family:inherit;
  font-size:var(--font-body-md);outline:0}}
.searchdlg input::placeholder{{color:var(--on-surface-3)}}
.search-results{{list-style:none;margin:0;padding:var(--space-s-2);
  overflow-y:auto;max-height:min(60dvh,520px);overscroll-behavior:contain}}
.search-results li a{{display:block;border:0;padding:var(--space-s-3) var(--space-s-4);
  border-radius:var(--radius-sm)}}
.search-results li a:hover,.search-results li a.is-active{{background:var(--surface-3)}}
.search-title{{display:block;font-size:var(--font-label-lg);font-weight:500}}
.search-crumb{{display:block;font-family:{MONO};
  font-size:var(--font-mono-xs);color:var(--on-surface-3);margin-top:2px}}
.search-snippet{{display:block;margin-top:var(--space-s-1);
  font-size:var(--font-body-xs);color:var(--on-surface-2);
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.search-snippet mark{{background:var(--warning-surface);color:inherit;
  padding:0 2px;border-radius:2px}}
.search-empty{{padding:var(--space-s-8) var(--space-s-5);text-align:center;
  color:var(--on-surface-3);font-size:var(--font-body-sm)}}
.search-foot{{display:flex;gap:var(--space-s-4);justify-content:flex-end;
  padding:var(--space-s-2) var(--space-s-4);
  border-top:var(--space-hairline) solid var(--outline);
  font-size:var(--font-body-xs);color:var(--on-surface-3)}}

/* ==========================================================================
   Pager and footer
   ========================================================================== */
.pager{{display:grid;gap:var(--space-s-3);margin-top:var(--space-s-10);
  grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}}
.pager a{{display:flex;flex-direction:column;gap:2px;padding:var(--space-s-4);
  border:var(--space-hairline) solid var(--outline);border-radius:var(--radius-md);
  background:var(--surface)}}
.pager a:hover{{border-color:var(--outline-strong);background:var(--surface-2)}}
.pager .pager-next{{text-align:end}}
.pager-label{{font-family:{MONO};font-size:var(--font-mono-xs);
  letter-spacing:var(--ls-mono-xs);text-transform:uppercase;color:var(--on-surface-3)}}
.pager-title{{font-size:var(--font-label-lg);font-weight:500}}

.pagefoot{{display:flex;flex-wrap:wrap;gap:var(--space-s-3);justify-content:space-between;
  margin-top:var(--space-s-10);padding-top:var(--space-s-5);
  border-top:var(--space-hairline) solid var(--outline);
  color:var(--on-surface-3);font-size:var(--font-body-xs)}}
.pagefoot a{{border-bottom-color:var(--outline)}}

/* ==========================================================================
   Universal rules
   ========================================================================== */
/* Type does not scale down: no token drops below its stated size on mobile. */
@media (max-width:600px){{
  .shell{{padding-block:var(--space-s-6) var(--space-s-10);gap:var(--space-s-8)}}
  .brand-word{{display:none}}
  .codeblock pre{{padding:var(--space-s-3) var(--space-s-4)}}
  .code-copy{{opacity:1}}
}}
@media (max-width:1023px){{.island-nav{{display:none}}}}

@media (prefers-reduced-motion:reduce){{
  html{{scroll-behavior:auto}}
  *,*::before,*::after{{animation-duration:.01ms !important;transition-duration:.01ms !important}}
}}
@media (forced-colors:active){{
  .island,.card,.table-wrap,.codeblock{{border:1px solid CanvasText}}
  .pill,.progress-track{{forced-color-adjust:none}}
}}
@media print{{
  .navrow,.sidebar,.inspector,.scrim,.skip-link,.code-copy,.pager,.searchdlg{{display:none !important}}
  body{{padding:0;font-size:11pt;background:#fff;color:#000}}
  .shell{{display:block;max-width:none;padding:0}}
  .codeblock,.table-wrap,.prose h2,.prose h3,.card{{break-inside:avoid}}
  .prose a[href^="http"]::after{{content:" (" attr(href) ")";font-size:9pt;color:#555}}
}}
"""
