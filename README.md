# FQF 2026 Schedule Builder

Personal schedule builder for French Quarter Festival 2026 (April 16–19, New Orleans).

Live at **https://festschedule.org**

## Setup

```bash
make setup && make dev
```

This installs backend and frontend dependencies and starts both dev servers with hot reload.

## Release

```bash
make test && make lint
git tag v<major>.<minor>.<patch>
git push --tags
```

GitHub Actions builds and deploys automatically on version tags. Verify at https://festschedule.org after the workflow completes.
