"""``atlas site``: build, serve, and clean the documentation site."""

from __future__ import annotations

import argparse
import contextlib
import functools
import http.server
import pathlib
import socketserver
import threading
import typing as t
import webbrowser

from ...errors import ExitCode
from ...site import build as build_site
from ...terminal import Style

if t.TYPE_CHECKING:  # pragma: no cover
    from .. import Context


def register(subparsers: t.Any, add_global_flags: t.Callable[..., None]) -> None:
    parser = subparsers.add_parser(
        "site",
        help="turn the docs into a website you can read",
        description=(
            "The site is generated from the Markdown every time. It is build output: ignored "
            "by git, rebuilt in CI, and never edited by hand. Where the site and the Markdown "
            "disagree, the Markdown is right and the site is stale."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_global_flags(parser)
    sub = parser.add_subparsers(dest="subcommand", metavar="<subcommand>")

    build = sub.add_parser(
        "build",
        help="render the site",
        description=(
            "Render every specification, document, workstream, prompt, and CLI page into a "
            "static site with client-side search, a sitemap, and a 404."
        ),
        epilog="atlas site build\natlas site build --out public --write-reference",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    build.add_argument("--out", default=None, metavar="DIR",
                       help="output directory (default: site/)")
    build.add_argument("--write-reference", action="store_true",
                       help="also regenerate docs/reference/cli.md from the parser")
    add_global_flags(build)
    build.set_defaults(handler=cmd_build)

    serve = sub.add_parser(
        "serve",
        help="build, then serve locally",
        description=(
            "Build the site and serve it on a local port, so links, search, and the 404 behave "
            "as they will in production. Ctrl-C to stop."
        ),
        epilog="atlas site serve\natlas site serve --port 8080 --no-open",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    serve.add_argument("--port", type=int, default=8000, help="port to listen on")
    serve.add_argument("--host", default="127.0.0.1", help="address to bind")
    serve.add_argument("--no-open", action="store_true", dest="no_open",
                       help="do not open a browser")
    serve.add_argument("--no-build", action="store_true", dest="no_build",
                       help="serve the existing build instead of rebuilding")
    serve.add_argument("--out", default=None, metavar="DIR", help="output directory")
    add_global_flags(serve)
    serve.set_defaults(handler=cmd_serve)

    clean = sub.add_parser(
        "clean",
        help="remove the build output",
        description="Delete the build directory. Nothing here is a source, so nothing is lost.",
    )
    clean.add_argument("--out", default=None, metavar="DIR", help="output directory")
    add_global_flags(clean)
    clean.set_defaults(handler=cmd_clean)

    parser.set_defaults(handler=lambda ctx: _default(ctx, parser))


def _default(ctx: Context, parser: argparse.ArgumentParser) -> ExitCode:
    if not getattr(ctx.args, "subcommand", None):
        parser.print_help()
        return ExitCode.OK
    return ExitCode.USAGE  # pragma: no cover


def _out_dir(ctx: Context) -> pathlib.Path:
    raw = getattr(ctx.args, "out", None)
    return (pathlib.Path(raw).expanduser().resolve() if raw else ctx.repo.site_out)


def cmd_build(ctx: Context) -> ExitCode:
    if getattr(ctx.args, "write_reference", False):
        from ..app import render_reference

        target = ctx.repo.docs / "reference" / "cli.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_reference(), encoding="utf-8")
        ctx.console.detail(f"wrote {ctx.repo.rel(target)}")

    result = build_site(ctx.repo, _out_dir(ctx))
    ctx.console.emit(
        {"pages": result.pages, "out": str(result.out),
         "indexed": result.indexed, "warnings": result.warnings}
    )
    for warning in result.warnings:
        ctx.console.status("warn", warning)
    ctx.console.status(
        "ok",
        f"built {result.pages} pages",
        f"{result.indexed} indexed → {ctx.repo.rel(result.out)}/",
    )
    return ExitCode.OK


def cmd_serve(ctx: Context) -> ExitCode:
    out = _out_dir(ctx)
    if not ctx.args.no_build:
        result = build_site(ctx.repo, out)
        ctx.console.status("ok", f"built {result.pages} pages", f"{result.indexed} indexed")
    if not out.is_dir():
        ctx.console.error(f"nothing to serve: {out} does not exist")
        return ExitCode.NOT_FOUND

    class Handler(http.server.SimpleHTTPRequestHandler):
        """Serves the build, with a real 404 page.

        The default handler returns a bare error body, which means the one page
        specifically written to help a reader who followed a stale link is the
        one page they never see.
        """

        def send_error(self, code: int, message: str | None = None,
                       explain: str | None = None) -> None:
            if code == 404 and (out / "404.html").exists():
                body = (out / "404.html").read_bytes()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                with contextlib.suppress(BrokenPipeError):
                    self.wfile.write(body)
                return
            super().send_error(code, message, explain)

        def log_message(self, fmt: str, *args: t.Any) -> None:
            if ctx.console.verbose:
                ctx.console.detail(fmt % args)

    socketserver.TCPServer.allow_reuse_address = True
    handler = functools.partial(Handler, directory=str(out))
    try:
        server = socketserver.TCPServer((ctx.args.host, ctx.args.port), handler)
    except OSError as error:
        ctx.console.error(f"cannot bind {ctx.args.host}:{ctx.args.port}: {error}")
        ctx.console.hint("Choose another port with --port.")
        return ExitCode.FAILURE

    url = f"http://{ctx.args.host}:{ctx.args.port}/"
    ctx.console.emit({"serving": str(out), "url": url})
    ctx.console.write()
    ctx.console.status("run", f"serving {ctx.repo.rel(out)}/", url)
    ctx.console.write(f"  {ctx.console.paint(url, Style.CYAN, Style.UNDER)}")
    ctx.console.write()
    ctx.console.detail("Ctrl-C to stop.")

    if not ctx.args.no_open:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        ctx.console.write()
        ctx.console.status("ok", "stopped")
    finally:
        server.server_close()
    return ExitCode.OK


def cmd_clean(ctx: Context) -> ExitCode:
    import shutil

    out = _out_dir(ctx)
    existed = out.is_dir()
    if existed:
        shutil.rmtree(out)
    ctx.console.emit({"removed": existed, "path": str(out)})
    ctx.console.status("ok" if existed else "skip",
                       f"removed {ctx.repo.rel(out)}/" if existed else "nothing to clean")
    return ExitCode.OK
