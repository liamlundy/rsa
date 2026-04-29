#!/bin/bash
set -e

echo "=== Python benchmarks (pytest-benchmark) ==="
uv run pytest bench/ --benchmark-only --benchmark-sort=mean "$@"

echo ""
echo "=== Rust benchmarks (criterion) ==="
cargo bench "$@"
