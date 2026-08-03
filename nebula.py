import argparse
import json
import sys
from pathlib import Path

from sandbox.orchestration import NebulaVerifier


def main():
    parser = argparse.ArgumentParser(description="Nebula Verification CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    verify_parser = subparsers.add_parser("verify", help="Verify an asset")
    verify_parser.add_argument("asset", type=str, help="Path to the asset file")
    verify_parser.add_argument("--json", action="store_true", help="Print result as JSON")

    args = parser.parse_args()

    if args.command == "verify":
        asset_path = Path(args.asset)
        if not asset_path.exists():
            print(f"Error: Asset file does not exist: {args.asset}", file=sys.stderr)
            sys.exit(1)

        verifier = NebulaVerifier()
        result = verifier.verify(asset_path)
        result_dict = result.to_dict()

        if args.json:
            print(json.dumps(result_dict, indent=2))
        else:
            print("=========================================")
            print("Nebula Verification Report")
            print("=========================================")
            print(f"Asset: {asset_path.name}")
            print(f"Category: {result_dict['classification']['category']}")
            print(f"Intake Confidence: {result_dict['classification']['confidence']}")
            print(f"Static Analysis Risk: {result_dict['static_analysis']['risk_level']}")
            print(f"Static Analysis Confidence: {result_dict['static_analysis']['confidence']}")
            print(f"Policy Decision: {result_dict['decision']}")
            print("-----------------------------------------")

            if "execution" in result_dict:
                print("Dynamic Sandbox Execution:")
                print(f"  Exit Code: {result_dict['execution']['exit_code']}")
                print(f"  Timed Out: {result_dict['execution']['timed_out']}")
                print(f"  Duration: {result_dict['execution']['duration_ms']} ms")
            
            if "hash" in result_dict:
                print(f"Consensus Transcript Hash: {result_dict['hash']}")
            
            print("=========================================")


if __name__ == "__main__":
    main()
