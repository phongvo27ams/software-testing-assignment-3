# -*- coding: utf-8 -*-
import importlib
import sys
import unittest


GROUPED_TEST_MODULES = [
    "tc_001",
    "tc_003_001",
    "tc_003_002",
    "tc_003_003_005_006",
    "tc_003_004",
    "tc_003_007_010",
    "tc_003_011_013",
    "tc_003_014_020",
    "tc_003_021_024",
    "tc_003_025",
    "tc_003_026_027",
    "tc_003_028_029",
    "tc_003_030_039",
]


def build_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for module_name in GROUPED_TEST_MODULES:
        module = importlib.import_module(module_name)
        suite.addTests(loader.loadTestsFromModule(module))
    return suite


def main():
    result = unittest.TextTestRunner(verbosity=2).run(build_suite())
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
