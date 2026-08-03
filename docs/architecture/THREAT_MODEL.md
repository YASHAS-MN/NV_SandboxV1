# Nebula Threat Model (v0.3.x)

## Scope

Nebula v0.3.x analyzes Python scripts only.

Native executables, APKs, drivers, and kernel-level malware are explicitly out of scope.

---

## Protected Assets

- Host operating system
- Workspace integrity
- Behavior transcript
- Validator correctness
- Consensus integrity

---

## Threats

### T1
Infinite loops

Mitigation

- Execution timeout

---

### T2
Filesystem abuse

Mitigation

- Isolated workspace
- Filesystem sensor

---

### T3
Process abuse

Mitigation

- Process sensor

---

### T4
Transcript tampering

Mitigation

- Canonical serialization

---

### T5
Non-deterministic observations

Mitigation

- Canonical Event
- Runtime metadata separation

---

## Out of Scope

- PE malware
- ELF malware
- APK analysis
- Kernel exploits
- VM escape
- Hypervisor attacks
- Hardware attacks
