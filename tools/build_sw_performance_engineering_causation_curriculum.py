#!/usr/bin/env python3
"""Author the quantum causation world (standalone, 2026-10-02 sweep)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from causation_world_lib import build_cli  # noqa: E402
from causation_worlds import sw_performance_engineering as quantum  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(build_cli(quantum))
