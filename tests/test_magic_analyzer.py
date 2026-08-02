from pathlib import Path
import tempfile

from sandbox.intake.analyzers.magic_analyzer import MagicAnalyzer

analyzer = MagicAnalyzer()

test_cases = {
    "sample.exe": "4D5A",
    "sample.png": "89504E47",
    "sample.pdf": "25504446",
    "sample.zip": "504B0304",
    "sample.txt": "48656c6c6f", # "Hello" in hex
}

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    for filename, hex_data in test_cases.items():
        filepath = root / filename
        with open(filepath, "wb") as f:
            f.write(bytes.fromhex(hex_data))

        result = analyzer.analyze(filepath)
        print(f"--- {filename} ---")
        print(result.to_dict())
