#!/usr/bin/env bash
# Test: setup-worktree.sh Phase 5 runs `npm run build` when package.json has a build script
# Usage: bash test-setup-worktree-build.sh
# Exit 0 = all tests pass, Exit 1 = failure

set -euo pipefail

PASS=0
FAIL=0

cleanup() {
  [[ -n "${TMPDIR_TEST:-}" ]] && rm -rf "$TMPDIR_TEST"
}
trap cleanup EXIT

assert_eq() {
  local label="$1" expected="$2" actual="$3"
  if [[ "$expected" == "$actual" ]]; then
    echo "  PASS: $label"
    PASS=$((PASS + 1))
  else
    echo "  FAIL: $label (expected '$expected', got '$actual')"
    FAIL=$((FAIL + 1))
  fi
}

# ---------- helpers ----------

# Extract the Phase 5 npm branch from setup-worktree.sh verbatim
# so the test proves the ACTUAL script behavior, not a copy.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_UNDER_TEST="${SCRIPT_DIR}/setup-worktree.sh"

# Extract lines 113-134 (the Phase 5 npm/cargo/go/python block)
# and run just that block in a temp dir.
run_phase5_in() {
  local dir="$1"
  # Source only the package.json branch of Phase 5 — verbatim from the script
  # We use sed to extract the exact npm branch (lines 113-116 in current script)
  bash -c "
    set -euo pipefail
    cd '$dir'
    $(sed -n '/^# Phase 5: Environment Setup$/,/^# Phase 6:/{ /^# Phase 6:/d; p; }' "$SCRIPT_UNDER_TEST")
  " 2>&1
}

# ---------- Test 1: build runs when package.json has build script ----------

echo "Test 1: runs npm run build when package.json has a build script"

TMPDIR_TEST="$(mktemp -d)"
cat > "$TMPDIR_TEST/package.json" <<'PKGJSON'
{
  "name": "test-project",
  "version": "1.0.0",
  "scripts": {
    "build": "node -e \"require('fs').writeFileSync('build-ran.marker', 'yes')\""
  }
}
PKGJSON

run_phase5_in "$TMPDIR_TEST" || true

if [[ -f "$TMPDIR_TEST/build-ran.marker" ]]; then
  assert_eq "build-ran.marker exists" "yes" "$(cat "$TMPDIR_TEST/build-ran.marker")"
else
  assert_eq "build-ran.marker exists" "file exists" "file missing"
fi

rm -rf "$TMPDIR_TEST"

# ---------- Test 2: build skipped when no build script ----------

echo "Test 2: skips build when package.json has no build script"

TMPDIR_TEST="$(mktemp -d)"
cat > "$TMPDIR_TEST/package.json" <<'PKGJSON'
{
  "name": "test-project",
  "version": "1.0.0",
  "scripts": {
    "test": "echo test"
  }
}
PKGJSON

run_phase5_in "$TMPDIR_TEST" || true

assert_eq "no build-ran.marker" "file missing" "$(if [[ -f "$TMPDIR_TEST/build-ran.marker" ]]; then echo 'file exists'; else echo 'file missing'; fi)"

rm -rf "$TMPDIR_TEST"

# ---------- Summary ----------

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
