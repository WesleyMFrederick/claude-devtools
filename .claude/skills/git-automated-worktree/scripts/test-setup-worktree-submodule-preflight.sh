#!/usr/bin/env bash
# Test: setup-worktree.sh Phase 1 handles stale submodule distinctly from dirty files
# Usage: bash test-setup-worktree-submodule-preflight.sh
# Exit 0 = all tests pass, Exit 1 = failure

set -euo pipefail

PASS=0
FAIL=0
ALL_TMPDIRS=()

cleanup() {
  for d in "${ALL_TMPDIRS[@]}"; do
    [[ -d "$d" ]] && rm -rf "$d"
  done
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

assert_contains() {
  local label="$1" expected="$2" actual="$3"
  if echo "$actual" | grep -qF "$expected"; then
    echo "  PASS: $label"
    PASS=$((PASS + 1))
  else
    echo "  FAIL: $label (expected output to contain '$expected')"
    FAIL=$((FAIL + 1))
  fi
}

assert_not_contains() {
  local label="$1" unexpected="$2" actual="$3"
  if echo "$actual" | grep -qF "$unexpected"; then
    echo "  FAIL: $label (output should NOT contain '$unexpected')"
    FAIL=$((FAIL + 1))
  else
    echo "  PASS: $label"
    PASS=$((PASS + 1))
  fi
}

make_tmpdir() {
  local d
  d="$(mktemp -d)"
  ALL_TMPDIRS+=("$d")
  echo "$d"
}

# ---------- helpers ----------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_UNDER_TEST="${SCRIPT_DIR}/setup-worktree.sh"

# Allow local file:// clones (git 2.38+ blocks by default)
export GIT_CONFIG_GLOBAL=""
export GIT_CONFIG_SYSTEM=""

# Extract Phase 1 pre-flight check from the script
extract_phase1() {
  sed -n '/^# Phase 1: Pre-flight Checks$/,/^# Phase 2:/{ /^# Phase 2:/d; p; }' "$SCRIPT_UNDER_TEST"
}

# Create a git repo with a .claude submodule where the submodule is stale (behind)
setup_stale_submodule_repo() {
  local dir="$1"

  # Create the "hub" repo (upstream for .claude submodule)
  local hub_dir="${dir}/hub"
  mkdir -p "$hub_dir"
  git -C "$hub_dir" init -b main >/dev/null 2>&1
  echo "initial" > "$hub_dir/README.md"
  git -C "$hub_dir" add .
  git -C "$hub_dir" commit -m "initial commit" >/dev/null 2>&1

  # Create the main repo with .claude as submodule
  local repo_dir="${dir}/repo"
  mkdir -p "$repo_dir"
  git -C "$repo_dir" init -b main >/dev/null 2>&1
  echo "project" > "$repo_dir/README.md"
  git -C "$repo_dir" add .
  git -C "$repo_dir" commit -m "initial project" >/dev/null 2>&1

  # Add submodule (allow local file transport)
  git -c protocol.file.allow=always -C "$repo_dir" submodule add "$hub_dir" .claude >/dev/null 2>&1
  git -C "$repo_dir" commit -m "add .claude submodule" >/dev/null 2>&1

  # Advance the hub by 2 commits (making submodule stale)
  echo "update1" > "$hub_dir/file1.md"
  git -C "$hub_dir" add .
  git -C "$hub_dir" commit -m "hub commit 1" >/dev/null 2>&1
  echo "update2" > "$hub_dir/file2.md"
  git -C "$hub_dir" add .
  git -C "$hub_dir" commit -m "hub commit 2" >/dev/null 2>&1

  # Pull new commits into submodule (makes it ahead of committed pointer = dirty)
  git -c protocol.file.allow=always -C "$repo_dir/.claude" fetch origin >/dev/null 2>&1
  git -C "$repo_dir/.claude" checkout origin/main >/dev/null 2>&1

  echo "$repo_dir"
}

# Create a git repo with genuinely dirty (non-submodule) files
setup_dirty_files_repo() {
  local dir="$1"

  local repo_dir="${dir}/repo"
  mkdir -p "$repo_dir"
  git -C "$repo_dir" init -b main >/dev/null 2>&1
  echo "project" > "$repo_dir/README.md"
  git -C "$repo_dir" add .
  git -C "$repo_dir" commit -m "initial" >/dev/null 2>&1

  # Make a tracked file dirty
  echo "modified" >> "$repo_dir/README.md"

  echo "$repo_dir"
}

# Create a repo where BOTH submodule is stale AND other files are dirty
setup_stale_submodule_and_dirty_files_repo() {
  local dir="$1"

  # Reuse stale submodule setup
  setup_stale_submodule_repo "$dir" >/dev/null

  local repo_dir="${dir}/repo"
  # Also make a tracked file dirty
  echo "modified" >> "$repo_dir/README.md"

  echo "$repo_dir"
}

# Run Phase 1 in a repo, auto-answering sync prompt
# $1 = repo dir, $2 = answer to prompt (y/n), or empty for no input
run_phase1_in() {
  local dir="$1"
  local answer="${2:-}"
  local exit_code=0

  local phase1_code
  phase1_code=$(extract_phase1)

  # Strip the "Running tests..." block — we only test Phase 1 pre-flight, not test execution
  phase1_code=$(echo "$phase1_code" | sed '/^echo "Running tests/,/echo "✓ Tests passing"/d')

  if [[ -n "$answer" ]]; then
    echo "$answer" | bash -c "
      set -euo pipefail
      export GIT_CONFIG_COUNT=1
      export GIT_CONFIG_KEY_0=protocol.file.allow
      export GIT_CONFIG_VALUE_0=always
      cd '$dir'
      $phase1_code
    " 2>&1 || exit_code=$?
  else
    bash -c "
      set -euo pipefail
      export GIT_CONFIG_COUNT=1
      export GIT_CONFIG_KEY_0=protocol.file.allow
      export GIT_CONFIG_VALUE_0=always
      cd '$dir'
      $phase1_code
    " 2>&1 || exit_code=$?
  fi
  return "$exit_code"
}

# ---------- Test 1: stale submodule detected distinctly ----------

echo "Test 1: detects stale submodule as distinct from dirty files"

TMPDIR_TEST="$(make_tmpdir)"
REPO_DIR=$(setup_stale_submodule_repo "$TMPDIR_TEST")

OUTPUT=$(run_phase1_in "$REPO_DIR" "y") || true

assert_contains "mentions submodule" "submodule" "$OUTPUT"
assert_not_contains "no generic dirty error" "Commit or stash changes first" "$OUTPUT"

# ---------- Test 2: dirty non-submodule files still blocked ----------

echo "Test 2: dirty non-submodule files still show generic error"

TMPDIR_TEST="$(make_tmpdir)"
REPO_DIR=$(setup_dirty_files_repo "$TMPDIR_TEST")

OUTPUT=$(run_phase1_in "$REPO_DIR" "") || true

assert_contains "shows generic dirty error" "Commit or stash changes first" "$OUTPUT"

# ---------- Test 3: stale submodule + dirty files = blocked ----------

echo "Test 3: stale submodule AND dirty files blocks with generic error"

TMPDIR_TEST="$(make_tmpdir)"
REPO_DIR=$(setup_stale_submodule_and_dirty_files_repo "$TMPDIR_TEST")

OUTPUT=$(run_phase1_in "$REPO_DIR" "") || true

assert_contains "shows generic dirty error" "Commit or stash changes first" "$OUTPUT"

# ---------- Test 4: user approves sync, ff-only succeeds ----------

echo "Test 4: user approves sync and ff-only succeeds"

TMPDIR_TEST="$(make_tmpdir)"
REPO_DIR=$(setup_stale_submodule_repo "$TMPDIR_TEST")

EXIT_CODE=0
OUTPUT=$(run_phase1_in "$REPO_DIR" "y") || EXIT_CODE=$?

assert_eq "exits successfully" "0" "$EXIT_CODE"
assert_contains "confirms sync" "synced" "$OUTPUT"

# ---------- Test 5: user declines sync = abort ----------

echo "Test 5: user declines sync and script aborts"

TMPDIR_TEST="$(make_tmpdir)"
REPO_DIR=$(setup_stale_submodule_repo "$TMPDIR_TEST")

EXIT_CODE=0
OUTPUT=$(run_phase1_in "$REPO_DIR" "n") || EXIT_CODE=$?

assert_eq "exits with error" "1" "$EXIT_CODE"

# ---------- Summary ----------

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
