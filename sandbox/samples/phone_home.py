"""
Nebula Network Test Fixture

This script attempts an outbound socket connection.
The NetworkSensor should record this in the transcript.
"""
import socket

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    s.connect(("93.184.216.34", 80))  # example.com IP — connection may fail but attempt is logged
    s.close()
except Exception:
    pass  # Connection may be blocked; attempt is still recorded by the sensor shim
