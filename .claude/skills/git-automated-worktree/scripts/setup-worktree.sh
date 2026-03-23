#!/usr/bin/env bash
# Automated git worktree setup following git-using-worktrees skill
# Usage: setup-worktree.sh <scope> <feature>
# Example: setup-worktree.sh jact ast-refactor

set -euo pipefail

# Self-contained naming principles: clear error messages
usage() {
  echo "Usage: $0 <scope> <feature>"
  echo "Example: $0 jact ast-refactor"
  echo ""
  echo "Creates: repo.worktree.scope.feature in sibling directory"
  echo "Branch: scope/feature"
  exit 1
}

# Validate arguments
[[ $# -ne 2 ]] && usage

SCOPE="$1"
FEATURE="$2"

# Determine paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../../../.." && pwd)"
cd "$PROJECT_ROOT"

# Phase 1: Pre-flight Checks
echo "Phase 1: Pre-flight Checks"

# Check git status
if ! git diff-index --quiet HEAD --; then
  # Determine what's dirty: submodule vs other files
  DIRTY_FILES=$(git diff-index --name-only HEAD --)
  SUBMODULE_DIRTY=false
  OTHER_DIRTY=false

  while IFS= read -r file; do
    if [[ "$file" == ".claude" ]]; then
      SUBMODULE_DIRTY=true
    else
      OTHER_DIRTY=true
    fi
  done <<< "$DIRTY_FILES"

  # If non-submodule files are dirty, block regardless
  if [[ "$OTHER_DIRTY" == true ]]; then
    echo "ERROR: Working directory is not clean. Commit or stash changes first."
    git status
    exit 1
  fi

  # Only .claude submodule is dirty — offer safe sync
  if [[ "$SUBMODULE_DIRTY" == true ]]; then
    echo "⚠️  .claude submodule is out of sync (normal drift)"
    echo "  Current pointer: $(git -C .claude rev-parse --short HEAD 2>/dev/null || echo 'unknown')"

    read -rp "Sync .claude submodule before proceeding? [Y/n] " REPLY
    if [[ "${REPLY:-Y}" =~ ^[Yy]$ ]]; then
      if git -C .claude pull --ff-only origin main 2>/dev/null; then
        git add .claude
        git commit -m "chore(.claude): sync submodule with hub"
        echo "✓ .claude submodule synced and committed"
      else
        echo "ERROR: Cannot fast-forward .claude submodule. Manual resolution needed."
        echo "  cd .claude && git status"
        exit 1
      fi
    else
      echo "Aborting. Sync submodule manually before creating worktree."
      exit 1
    fi
  fi
fi

echo "✓ Git status clean"

# Check tests pass
echo "Running tests..."
if ! npm test; then
  echo "ERROR: Tests are failing. Fix tests before creating worktree."
  exit 1
fi

echo "✓ Tests passing"

# Phase 2: Determine Naming
echo ""
echo "Phase 2: Determine Naming"

REPO=$(basename "$(git rev-parse --show-toplevel)")
WORKTREE_DIR="${REPO}.worktree.${SCOPE}.${FEATURE}"
BRANCH_NAME="${SCOPE}/${FEATURE}"

echo "Repository: $REPO"
echo "Worktree directory: $WORKTREE_DIR"
echo "Branch name: $BRANCH_NAME"

# Phase 3: Clean Up Existing Worktree
echo ""
echo "Phase 3: Clean Up Existing Worktree"

PARENT_DIR="$(dirname "$PROJECT_ROOT")"
WORKTREE_PATH="${PARENT_DIR}/${WORKTREE_DIR}"

# Remove existing worktree if present
if git worktree list | grep -q "$WORKTREE_DIR"; then
  echo "Removing existing worktree: $WORKTREE_PATH"
  git worktree remove "$WORKTREE_PATH" --force 2>/dev/null || true
fi

# Delete branch if exists
if git branch --list "$BRANCH_NAME" | grep -q "$BRANCH_NAME"; then
  echo "Deleting existing branch: $BRANCH_NAME"
  git branch -D "$BRANCH_NAME" 2>/dev/null || true
fi

echo "✓ Cleanup complete"

# Phase 4: Create Worktree
echo ""
echo "Phase 4: Create Worktree"

git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"
cd "$WORKTREE_PATH"

echo "✓ Worktree created at: $WORKTREE_PATH"
echo "✓ Branch created: $BRANCH_NAME"

# Phase 4.5: Submodule — latest from local hub
if [[ -f .gitmodules ]] && grep -q '.claude' .gitmodules; then
  echo ""
  echo "Phase 4.5: Submodule — latest from local hub"
  if git submodule update --init --recursive; then
    git -C .claude pull --ff-only origin main
    echo "✓ .claude at $(git -C .claude rev-parse --short HEAD)"
  else
    echo "⚠️  submodule init failed, attempting fallback..."
    LOCAL_HUB=$(git config --file .gitmodules submodule..claude.url 2>/dev/null)
    rm -rf .claude
    git clone --branch main "${LOCAL_HUB}" .claude
    echo "✓ .claude cloned from local hub at $(git -C .claude rev-parse --short HEAD)"
  fi
fi

# Phase 5: Environment Setup
echo ""
echo "Phase 5: Environment Setup"

if [[ -f package.json ]]; then
  echo "Installing npm dependencies..."
  npm install --ignore-scripts
  echo "✓ Dependencies installed"
  if node -e "const p=require('./package.json'); process.exit(p.scripts?.build ? 0 : 1)" 2>/dev/null; then
    echo "Building project..."
    npm run build
    echo "✓ Build complete"
  fi
elif [[ -f Cargo.toml ]]; then
  echo "Building Rust project..."
  cargo build
  echo "✓ Cargo build complete"
elif [[ -f go.mod ]]; then
  echo "Downloading Go modules..."
  go mod download
  echo "✓ Go modules downloaded"
elif [[ -f requirements.txt ]] || [[ -f pyproject.toml ]]; then
  if [[ -f pyproject.toml ]]; then
    echo "Installing Python dependencies with poetry..."
    poetry install
  else
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
  fi
  echo "✓ Python dependencies installed"
fi

# Phase 6: Verify Dependencies
echo ""
echo "Phase 6: Verify Dependencies"

if [[ -f package.json ]]; then
  npm list --depth=0 || true
fi

# Phase 7: Test Validation
echo ""
echo "Phase 7: Test Validation"

if [[ -f package.json ]]; then
  echo "Running tests in worktree..."
  if ! npm test; then
    echo "ERROR: Tests failing in worktree. Debug and fix before proceeding."
    exit 1
  fi
  echo "✓ Tests passing in worktree"
fi

# Phase 8: Report Ready State
echo ""
echo "================================================================"
echo "Worktree setup complete:"
echo "  Location: $WORKTREE_PATH"
echo "  Branch: $BRANCH_NAME"
echo "  Dependencies: installed and verified"
echo "  Tests: passing"
echo ""
echo "Ready to begin implementation."
echo "================================================================"

exit 0