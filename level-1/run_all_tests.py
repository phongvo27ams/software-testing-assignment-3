# -*- coding: utf-8 -*-
import argparse
import importlib
import re
import sys
import unittest
from pathlib import Path


TEST_FILE_PATTERN = re.compile(r"^tc_003_(\d{3})\.py$")


def iter_test_modules(start=None, end=None):
    level_dir = Path(__file__).resolve().parent
    module_names = []

    for path in level_dir.glob("tc_003_*.py"):
        match = TEST_FILE_PATTERN.match(path.name)
        if not match:
            continue

        test_number = int(match.group(1))
        if start is not None and test_number < start:
            continue
        if end is not None and test_number > end:
            continue

        module_names.append((test_number, path.stem))

    for _, module_name in sorted(module_names):
        yield module_name


def build_suite(start=None, end=None):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for module_name in iter_test_modules(start=start, end=end):
        module = importlib.import_module(module_name)
        suite.addTests(loader.loadTestsFromModule(module))

    return suite


def parse_args():
    parser = argparse.ArgumentParser(description="Run Moodle Level 1 data-driven test cases in order.")
    parser.add_argument("--start", type=int, help="First TC number to run, for example 1 or 25.")
    parser.add_argument("--end", type=int, help="Last TC number to run, for example 39.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose unittest output.")
    return parser.parse_args()


def main():
    args = parse_args()
    suite = build_suite(start=args.start, end=args.end)
    verbosity = 2 if args.verbose else 1
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
