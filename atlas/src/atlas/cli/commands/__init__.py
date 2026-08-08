"""One module per command.

Each module declares a ``SUMMARY`` (one line, shown in grouped help), a
``configure(parser)`` that adds its arguments, and a ``run(args, console)`` that
returns an exit code. Nothing here prints outside ``console``, and nothing here
calls ``sys.exit``.
"""
