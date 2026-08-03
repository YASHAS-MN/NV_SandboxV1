# Nebula Acceptance Test Plan

## Acceptance Test Matrix

| Test ID | Asset | Expected Result | Category | Static Risk | Policy Decision | Runtime Exit Code | Transcript Hash Generated |
|---|---|---|---|---|---|---|---|
| AT-001 | hello.py | COMPLETE | SCRIPT | LOW | CONTINUE | 0 | Yes |
| AT-002 | infinite_loop.py | Timeout | SCRIPT | LOW | CONTINUE | -1 (Timeout) | Yes |
| AT-003 | sample.txt | Static only | UNKNOWN | UNKNOWN | REJECT | N/A | No |
| AT-004 | sample.png | Classified, no runtime | IMAGE | LOW | COMPLETE | N/A | No |
| AT-005 | malformed.py | Runtime failure | SCRIPT | LOW | CONTINUE | Non-zero | Yes |
| AT-006 | missing.py | Graceful error | N/A | N/A | N/A | N/A | No |

---

## Verification Execution Procedures

### AT-001: hello.py
- Command: `python nebula.py verify sandbox/samples/hello.py`
- Verify Classification: Category is `SCRIPT`.
- Verify Static: Risk is `LOW`.
- Verify Policy Decision: `CONTINUE`.
- Verify Sandbox: Exit code is `0`, duration is recorded.
- Verify Transcript: Validation passes, deterministic SHA-256 hash is generated.

### AT-002: infinite_loop.py
- Command: `python nebula.py verify sandbox/samples/infinite_loop.py`
- Verify Classification: Category is `SCRIPT`.
- Verify Policy Decision: `CONTINUE`.
- Verify Sandbox: Exit code is `-1`, `timed_out` is `True`.
- Verify Transcript: Clean exit, validation passes, deterministic hash is generated.

### AT-003: sample.txt
- Command: `python nebula.py verify sample.txt`
- Verify: Asset category is `UNKNOWN` and policy decision is `REJECT`, execution is gracefully skipped.

### AT-004: sample.png
- Command: `python nebula.py verify sample.png`
- Verify: Asset category is `IMAGE` and policy decision is `COMPLETE` (static asset does not require dynamic execution). No sandbox execution occurs.
