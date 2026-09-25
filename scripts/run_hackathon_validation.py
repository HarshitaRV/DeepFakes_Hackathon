import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_step(label: str, command: list[str]):
    print(f"\n=== {label} ===")
    result = subprocess.run(command, cwd=str(ROOT), text=True)
    if result.returncode != 0:
        print(f"FAILED: {label}")
        raise SystemExit(result.returncode)
    print(f"PASSED: {label}")


def main():
    print("Running hackathon validation workflow...\n")
    run_step("Generate synthetic test data", [sys.executable, "scripts/generate_test_media.py"])
    run_step("Run evaluation checks", [sys.executable, "scripts/evaluate_test_cases.py"])
    print("\nAll hackathon validation checks passed.")


if __name__ == "__main__":
    main()
