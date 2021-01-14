#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tests/test_runner.py

import unittest
import numpy as np

"""Convenience wrapper for running tests."""

from tests import test_editor

if __name__ == '__main__':
#    test_editor()
#    unittest.main()
    test_editor.TestEditor()
    print("run tests ")