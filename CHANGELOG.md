# Nebula Changelog

# Nebula v1.0.0

## Features

- **Intake Gateway**: Formulates classifications from extensions and magic byte headers.
- **Static Analysis**: Identifies hash details, entropy thresholds, and YARA matches.
- **Execution Policy**: Determines runtime access permissions based on categories.
- **Python Runtime**: Coordinates read-only workspace containment and timeouts.
- **Process & Filesystem Sensors**: Stateless, priority-ordered behavior collection.
- **Observation Bus**: Pure transport layer connecting sensors to transcript assembly.
- **Behavior Transcript**: Immutable, validation-ready execution reports.
- **Canonical Hashing**: Deterministic SHA-256 validation excluding runtime metadata.
- **CLI**: Standard commands to verify assets with human-readable and structured outputs.

## Supported Assets

- Python scripts (`.py`).
- Passive classification for `EXE`, `PNG`, `PDF`, and `ZIP` files.

## Limitations

- Native executables are not dynamic-sandbox executed.
- Network and registry sensors are not implemented.
- Secure environment isolation (e.g., container/hypervisor backends) is deferred to future work.
