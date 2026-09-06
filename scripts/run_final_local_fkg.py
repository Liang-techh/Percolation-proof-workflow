"""Compatibility alias for the generic manifest-driven Linux verifier.

The old file name is retained for existing notes, but it no longer contains a
target-specific bundle digest, state path, theorem name, or project layout.
Use ``verify_manifest_linux.py`` directly for new targets.
"""
from verify_manifest_linux import main


if __name__ == '__main__':
    raise SystemExit(main())
