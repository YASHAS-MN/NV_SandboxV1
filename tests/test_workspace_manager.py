from sandbox.runtime.workspace import WorkspaceManager

manager = WorkspaceManager()

# Verify path property before create raises error
try:
    _ = manager.path
    assert False, "Should raise RuntimeError"
except RuntimeError:
    pass

# Create workspace
path = manager.create()

assert path.exists()

print(path)

# Verify path property works after create
assert manager.path == path

# Clean up
manager.cleanup()

assert manager._directory is None

# Cleanup again (should be idempotent and not throw)
manager.cleanup()
