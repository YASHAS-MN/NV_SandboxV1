"""
Nebula Labs
Standard Logging Configuration
"""

import logging
import sys

# Configure standard logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)

logger = logging.getLogger("nebula")
