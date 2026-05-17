# -*- coding: utf-8 -*-
import importlib
import sys
import unittest


NF_TEST_MODULES = [
    "nf_tc_001",
    "nf_tc_002",
    "nf_tc_003",
    "nf_tc_004_001",
    "nf_tc_004_002",
]


def build_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for module_name in NF_TEST_MODULES:
        module = importlib.import_module(module_name)
        suite.addTests(loader.loadTestsFromModule(module))
    return suite


def main():
    result = unittest.TextTestRunner(verbosity=2).run(build_suite())
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
