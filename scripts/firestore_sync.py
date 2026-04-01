#!/usr/bin/env python3
"""Dump production Firestore to JSON, or load JSON into the local emulator.

Usage:
    # Dump prod schedules collection to JSON (uses gcloud default credentials)
    python scripts/firestore_sync.py --dump

    # Dump to a specific file
    python scripts/firestore_sync.py --dump -o backup.json

    # Load JSON into local Firestore emulator (must be running on :8081)
    python scripts/firestore_sync.py --load-dev

    # Load from a specific file
    python scripts/firestore_sync.py --load-dev -i backup.json
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

DEFAULT_DUMP_FILE = "firestore_dump.json"
SCHEDULES_COLLECTION = "schedules"
EMULATOR_HOST = "localhost:8081"
EMULATOR_PROJECT = "fqf2026-local"
EMULATOR_HOST_ENV = "FIRESTORE_EMULATOR_HOST"


def get_prod_client():  # type: ignore[no-untyped-def]
    """Connect to production Firestore using default gcloud credentials."""
    if os.environ.get(EMULATOR_HOST_ENV):
        print(
            f"ERROR: {EMULATOR_HOST_ENV} is set — unset it to connect to prod.",
            file=sys.stderr,
        )
        sys.exit(1)

    from google.cloud import firestore  # type: ignore[import-untyped]

    project = os.environ.get("GCP_PROJECT")
    if not project:
        result = subprocess.run(
            ["gcloud", "config", "get-value", "project"],
            capture_output=True,
            text=True,
            check=False,
        )
        project = result.stdout.strip()
    if not project:
        print("ERROR: No GCP project found. Set GCP_PROJECT or run `gcloud config set project`.", file=sys.stderr)
        sys.exit(1)

    print(f"Connecting to prod Firestore (project: {project})")
    return firestore.Client(project=project)


def get_emulator_client():  # type: ignore[no-untyped-def]
    """Connect to the local Firestore emulator."""
    from google.cloud import firestore  # type: ignore[import-untyped]

    os.environ[EMULATOR_HOST_ENV] = EMULATOR_HOST
    print(f"Connecting to Firestore emulator at {EMULATOR_HOST} (project: {EMULATOR_PROJECT})")
    return firestore.Client(project=EMULATOR_PROJECT)


def dump(output_path: str) -> None:
    """Read all documents from prod schedules collection and write JSON."""
    client = get_prod_client()
    docs = client.collection(SCHEDULES_COLLECTION).stream()

    data: dict[str, dict] = {}  # type: ignore[type-arg]
    count = 0
    for doc in docs:
        data[doc.id] = doc.to_dict()
        count += 1

    client.close()

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2, default=str)

    print(f"Dumped {count} documents to {output_path}")


def load_dev(input_path: str) -> None:
    """Load JSON into the local Firestore emulator."""
    if not Path(input_path).exists():
        print(f"ERROR: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path) as f:
        data: dict[str, dict] = json.load(f)  # type: ignore[type-arg]

    client = get_emulator_client()
    collection = client.collection(SCHEDULES_COLLECTION)

    count = 0
    for doc_id, doc_data in data.items():
        collection.document(doc_id).set(doc_data)
        count += 1

    client.close()
    print(f"Loaded {count} documents into emulator")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Firestore data between prod and local emulator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dump", action="store_true", help="Dump prod Firestore to JSON")
    group.add_argument("--load-dev", action="store_true", help="Load JSON into local emulator")
    parser.add_argument("-o", "--output", default=DEFAULT_DUMP_FILE, help=f"Output file for --dump (default: {DEFAULT_DUMP_FILE})")
    parser.add_argument("-i", "--input", default=DEFAULT_DUMP_FILE, help=f"Input file for --load-dev (default: {DEFAULT_DUMP_FILE})")

    args = parser.parse_args()

    if args.dump:
        dump(args.output)
    elif args.load_dev:
        load_dev(args.input)


if __name__ == "__main__":
    main()
