# Nebula Changelog

# Nebula v1.1.0

## New Features

- **Network Sensor**: `NetworkSensor` intercepts `socket.connect()` calls via
  workspace-injected `sitecustomize.py` shim. Produces `NETWORK_CONNECT` events
  in the behavior transcript. No OS privileges required.
- **JavaScript Runner**: Executes `.js`, `.ts`, `.mjs` files via Node.js.
- **Shell Runner**: Executes `.sh`, `.bash`, `.ps1`, `.bat` via platform interpreter.
- **Java Runner**: Executes `.jar`, `.class`, `.war` files via JVM.
- **Archive Runner**: Recursively unpacks `.zip`, `.tar`, `.gz`, `.tgz` and
  applies full NebulaVerifier to each extracted asset.
- **Expanded Classification**: 22 new extension mappings across SCRIPT, IMAGE,
  DOCUMENT, AUDIO, VIDEO, ARCHIVE, and DATA categories.
- **Expanded Policy Routing**: AUDIO/VIDEO/DATA → static-only; ARCHIVE → runtime.

## Supported Assets (v1.1.0)

- Python `.py`
- JavaScript `.js` / `.ts` / `.mjs` (requires Node in PATH)
- Shell `.sh` / `.bash` / `.ps1` / `.bat`
- JVM `.jar` / `.class` (requires Java in PATH)
- Archives `.zip` / `.tar` / `.gz` / `.tgz` (recursive scan)
- Static: IMAGE, DOCUMENT, AUDIO, VIDEO, DATA (classification + static analysis only)

---

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
