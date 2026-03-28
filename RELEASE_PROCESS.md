# Release Process

## Overview

Releases are tag-driven. The version comes from `git describe --tags` and flows into the
container image build. Deployment is manual via `make deploy` (Cloud Run).

## Pre-Release Checklist

### 1. Review Dependabot Alerts

Check GitHub for open Dependabot PRs and security alerts:

```bash
gh pr list --label dependencies
gh api repos/:owner/:repo/dependabot/alerts --jq '.[].security_advisory.summary'
```

For each alert/PR, decide:
- **Merge** — update is safe, tests pass
- **Dismiss** — false positive or not applicable (document reason)
- **Defer** — breaking change that needs its own branch; create an issue to track it

### 2. Run Full Test Suite

```bash
make test        # backend + frontend
make lint        # backend + frontend linting
```

All tests must pass. All lint must be clean.

### 3. Update Version Tag

```bash
git tag v<MAJOR>.<MINOR>.<PATCH>
```

Follow semver:
- **PATCH** — bug fixes, dependency updates, cosmetic changes
- **MINOR** — new features, new endpoints, new pages
- **MAJOR** — breaking API changes, schema changes requiring data migration

### 4. Build and Deploy

```bash
make deploy
```

This builds the container image, pushes to both registries (GHCR + GCR), and deploys to Cloud Run.

### 5. Verify Deployment

After deploy completes:
- Visit the app URL and confirm it loads
- Check Cloud Run logs for startup errors
- Verify the version reported matches the tag

## Hotfix Process

For urgent fixes on a deployed version:

1. Branch from the release tag: `git checkout -b hotfix/description v<version>`
2. Fix, test, commit
3. Merge to main
4. Tag with incremented patch version
5. `make deploy`
