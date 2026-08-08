"""``python -m atlas`` behaves exactly like the ``atlas`` script."""

from __future__ import annotations

from .cli import main

if __name__ == "__main__":  # pragma: no cover
    main()
